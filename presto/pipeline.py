import pathlib
import tensorflow as tf

def build_pipeline(pipeline_spec
                 , compress_map=True
                 , compressed_parallelism=None):
    '''Convert pipeline specification into a tf.data.Dataset

    :param pipeline_spec: Pipeline specification.
    :param compress_map: Pack all data conversions into a single TF map stage.
    :param compressed_parallelism: If compress_map is true, execute compressed map stage with parallel calls.
    :return: tf.data.Dataset
    '''
    src, *rest = pipeline_spec
    ds = src["op"]

    def get_compressed_mapper(ops):
        def map_fn(x):
            for seg in ops:
                x = seg["op"](x)
            return x
        return {
            "name": " > ".join([op["name"] for op in ops]),
            "type": "op",
            "op": map_fn,
            "input_schema": ops[0]["input_schema"],
            "output_schema": ops[-1]["output_schema"]
        }

    # optimize, compress
    if compress_map:
        grouped = []
        # group map ops for compression
        buf = []
        for seg in rest:
            if seg["type"] == "op":
                buf.append(seg)
            else:
                if buf:
                    grouped.append(buf)
                    buf = []
                grouped.append(seg)
        if buf:
            grouped.append(buf)

        # compress map ops
        compressed = []
        for group in grouped:
            if isinstance(group, list):
                # map ops to compress
                compressed.append(get_compressed_mapper(group))
            else:
                compressed.append(group)

        rest = compressed

    # compile the ds
    for seg in rest:
        if seg["type"] == "op":
            ds = ds.map(seg["op"], num_parallel_calls=compressed_parallelism)
        if seg["type"] == "op+unbatch":
            ds = ds.map(seg["op"], num_parallel_calls=compressed_parallelism)
            ds = ds.unbatch()
        elif seg["type"] == "ds_transform":
            ds = ds.apply(seg["op"])
        elif seg["type"] == "unbatch":
            ds = ds.unbatch()
    return ds


def verify_pipeline(pipeline_spec):
    '''Verify pipeline specification for matching schemas
    Throws an exception in case an error is found

    :param pipeline_spec: list(dict)
    '''
    if len(pipeline_spec) <= 1:
        return True

    head, *tail = pipeline_spec

    last_output_schema = head["output_schema"]

    for segment in tail:
        current_input_schema = segment["input_schema"]
        if current_input_schema != last_output_schema:
            raise Exception("Schemas do not match at {} ({} -> {})".format(segment["name"], last_output_schema, current_input_schema))
        last_output_schema = segment["output_schema"]


def serialized_split(pipeline_spec
                   , split_pos: int):
    '''Split pipeline at given position and add serialization and deserialization
    operators to the parts

    :param pipeline_spec: list(dict)
    :param split_pos: index to split the pipeline, operator at index will be included in second half
    :return: tuple, with both halfs of the pipeline
    '''
    if split_pos > len(pipeline_spec):
        raise Exception("Both splits must at least contain one segment.")

    a, b = pipeline_spec[:split_pos], pipeline_spec[split_pos:]

    serialization_schema = a[-1]["output_schema"]
    a.append({
        "name": "serialize",
        "type": "op",
        "op": serializer(serialization_schema),
        "input_schema": serialization_schema,
        "output_schema": tf.TensorSpec([], tf.string)
    })
    b.insert(0, {
        "name": "deserialize",
        "type": "op",
        "op": deserializer(serialization_schema),
        "input_schema": tf.TensorSpec([], tf.string),
        "output_schema": serialization_schema 
    })

    return a, b

def serializer(schema):
    '''Prepares the serialization to a string for the previous data format
    :param schema: tf.TensorSpec
    :return: tf.py_function (input -> str)
    '''
    if not isinstance(schema, dict):
        schema = {"data": schema}

    order = sorted(list(schema.keys()))

    def serialize(*xs):
        features = {}
        for feature_name, feature_type in schema.items():
            feature = None
            if feature_type.dtype == tf.string:
                # string tensors
                # value = x[feature_name].numpy()
                value = xs[order.index(feature_name)].numpy()
                if not hasattr(value, "shape"):
                    value = [value]
                feature = tf.train.Feature(bytes_list=tf.train.BytesList(value=value))
            else:
                # numeric tensors
                # value = x[feature_name]
                value = xs[order.index(feature_name)].numpy()
                value = tf.io.serialize_tensor(value).numpy()
                feature = tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

            features[feature_name] = feature

        example = tf.train.Example(features=tf.train.Features(feature=features))
        
        return example.SerializeToString()

    def map_fn(x):
        if not isinstance(x, dict):
            inputs = [x]
        else:
            inputs = [x[feature] for feature in order]
        return tf.py_function(serialize, inputs, tf.string)

    return map_fn


def deserializer(schema):
    '''Prepares the deserialization from a string to the previous data format
    :param schema: tf.TensorSpec
    :return: tf.py_function (str -> input)
    '''
    singleton = False
    if not isinstance(schema, dict):
        schema = {"data": schema}
        singleton = True

    decode_schema = {}
    for feature_name, feature_type in schema.items():
        if feature_type.dtype != tf.string:
            decode_schema[feature_name] = tf.io.FixedLenFeature([1], tf.string)#feature_type.dtype)
        elif len(feature_type.shape) > 0 and feature_type.shape[0] is None:
            decode_schema[feature_name] = tf.io.FixedLenSequenceFeature(feature_type.shape[1:], tf.string, allow_missing=True)
        else:
            decode_schema[feature_name] = tf.io.FixedLenFeature(feature_type.shape, tf.string)#feature_type.dtype)

    def deserialize(x):
        example = tf.io.parse_single_example(x, decode_schema)

        for feature_name, feature_spec in schema.items():
            feature_type = feature_spec.dtype
            if feature_type != tf.string:
                example[feature_name] = tf.io.parse_tensor(example[feature_name][0], feature_type)

        if singleton:
            return example["data"]
        else:
            return example

    return deserialize

def save_ds_parallel(dataset
                   , shard_count: int 
                   , shard_directory: str
                   , compression_type: str):
    '''Saves the dataset into N shards at the according path. 
    TODO: writers are buffered
          if buffer write-back is synchronous, this is not really parallel
          but there does not seem to be any other way using TF measures

    :param dataset: tf.Dataset to be saved
    :param shard_count: int, amount of shards to split the dataset in
    :param shard_directory: str - filepath to the directory to save the shards in. If it already exists, an error is thrown
    :param compression_type: str - compression type for the intermediate representations. Possible parameters: ZLIB, GZIP, or "" for no compression
    '''

    tf_writer = tf.io.TFRecordWriter

    shard_directory_path = pathlib.Path(shard_directory)
    shard_directory_path.mkdir(exist_ok = True, parents = True)

    writers = [tf.io.TFRecordWriter(f"{shard_directory}/shard-{shard_number}.tfrecord", options=compression_type) for shard_number in range(shard_count)]

    for i, record in dataset.enumerate():
        writers[i % shard_count].write(record.numpy())

    for writer in writers:
        writer.close()
        
