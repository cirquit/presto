import sys
import numpy as np
import tensorflow as tf

def pipeline_definition(shape, sample_count, data_type, computation_type):

    if data_type == "float32":
        dtype = tf.float32
        create_dataset = float32_dataset(shape=shape, sample_count=sample_count)
    elif data_type == "uint8":
        dtype = tf.uint8
        create_dataset = uint8_dataset(shape=shape, sample_count=sample_count)
    else:
        print(f"ERROR: Unsupported dtype in pipeline_definition: {dtype}")
        sys.exit(1)

    return [
        {
            "name": f"create-dataset-{data_type}",
            "type": "source",
            "op": create_dataset,
            "input_schema": tf.TensorSpec([None, shape[1]], dtype),
            "output_schema": tf.TensorSpec([None, shape[1]], dtype)
        },
        {
            "name": "identity",
            "type": "op",
            "op": tf.identity,
            "input_schema": tf.TensorSpec([None, shape[1]], dtype),
            "output_schema": tf.TensorSpec([None, shape[1]], dtype)
        },
    ]

def uint8_dataset(shape, sample_count):
    '''
    '''
    def uint8_generator(shape, sample_count):
        '''
        '''
        for _ in range(sample_count):
            yield np.random.randint(low=0, high=255, size=shape, dtype=np.uint8)

    generator = lambda: uint8_generator(shape=shape, sample_count=sample_count)
    ds = tf.data.Dataset.from_generator(generator = generator
                                   ,output_types= tf.uint8
                                   ,output_shapes=(tf.TensorShape([None, shape[1]])))
    return ds

def float32_dataset(shape, sample_count):
    '''
    '''
    def float32_generator(shape, sample_count):
        '''
        '''
        min_float = -2**15
        max_float = 2**15-1
        for _ in range(sample_count):
            yield np.random.uniform(low=min_float, high=max_float, size=shape).astype(np.float32)

    generator = lambda: float32_generator(shape=shape, sample_count=sample_count)
    ds = tf.data.Dataset.from_generator(generator = generator
                                   ,output_types= tf.float32
                                   ,output_shapes=(tf.TensorShape([None, shape[1]])))
    return ds
