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

    # fixed to 500, because the smallest sample is 2500 big, so always devisible
    transform_period = 500

    if computation_type == "numpy-raw":
        comp_fn = lambda signal: rms_numpy_raw()(signal=signal, period_length=transform_period)
    elif computation_type == "numpy-class":
        comp_fn = lambda signal: rms_numpy_class()(signal=signal, period_length=transform_period)
    elif computation_type == "tensorflow-fn-wrapped":
        comp_fn = lambda signal: rms_tensorflow_fn_wrapped()(signal=signal, period_length=transform_period)
    elif computation_type == "tensorflow-for-loop-fn-wrapped":
        comp_fn = lambda signal: rms_tensorflow_for_loop_fn_wrapped()(signal=signal, period_length=transform_period)
    else:
        comp_fn = lambda signal: rms_tensorflow(signal=signal, period_length=transform_period)

    return [
        {
            "name": f"create-dataset-{computation_type}",
            "type": "source",
            "op": create_dataset,
            "input_schema": tf.TensorSpec([None, shape[1]], dtype),
            "output_schema": tf.TensorSpec([None, shape[1]], dtype)
        },
        {
            "name": f"apply-rms-{computation_type}",
            "type": "op",
            "op": comp_fn,
            "input_schema": tf.TensorSpec([None, shape[1]], dtype),
            "output_schema": tf.TensorSpec([None, int((shape[0] * shape[1]) / 500)], dtype)
        },

        {
            "name": "identity",
            "type": "op",
            "op": tf.identity,
            "input_schema": tf.TensorSpec([None, int((shape[0] * shape[1]) / 500)], dtype),
            "output_schema": tf.TensorSpec([None, int((shape[0] * shape[1]) / 500)], dtype)
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


def rms_tensorflow(signal, period_length):
    '''
    :param signal: tf.Tensor
    :param period_length: int
    :return: flattened tensor
    '''
    # flatten
    signal_reshaped = tf.reshape(signal, [-1])
    # split into phase chunks
    split_signal = tf.split(signal_reshaped, num_or_size_splits=period_length, axis=0)
    # rms
    rms_fn = lambda period: tf.sqrt(tf.cast(tf.reduce_mean(tf.math.square(period)), dtype=tf.float32))
    # apply rms onto every chunk
    result = tf.map_fn(fn=rms_fn, elems=split_signal, fn_output_signature=tf.float32)
    return result

def rms_tensorflow_fn_wrapped():
    '''
    :param signal: tf.Tensor
    :param period_length: int
    :return: flattened tensor
    '''
    def inner_fn(signal, period_length):
        # flatten
        signal_reshaped = tf.reshape(signal, [-1])
        # split into phase chunks
        split_signal = tf.split(signal_reshaped, num_or_size_splits=int(period_length), axis=0)
        # rms
        rms_fn = lambda period: tf.sqrt(tf.cast(tf.reduce_mean(tf.math.square(period)), dtype=tf.float32))
        # apply rms onto every chunk
        result = tf.map_fn(fn=rms_fn, elems=split_signal, fn_output_signature=tf.float32)
        return result

    return lambda signal, period_length: tf.py_function(inner_fn, [signal, period_length], Tout=[tf.float32])

def rms_tensorflow_for_loop_fn_wrapped():
    '''
    :param signal: tf.Tensor
    :param period_length: int
    :return: flattened tensor
    '''
    def inner_fn(signal, period_length):
        # flatten
        signal_reshaped = tf.reshape(signal, [-1])
        # rms
        rms_fn = lambda period: tf.sqrt(tf.cast(tf.reduce_mean(tf.math.square(period)), dtype=tf.float32))
        rms_values = []
        period_length = int(period_length)
        for i in range(0, len(signal_reshaped), period_length):
            if i + period_length <= len(signal_reshaped):
                signal_one_period = signal_reshaped[i:int(i + period_length)]
                rms_one_period = rms_fn(signal_one_period) #rms
                rms_values.append(rms_one_period)
        return tf.convert_to_tensor(rms_values, dtype=tf.float32)

    return lambda signal, period_length: tf.py_function(inner_fn, [signal, period_length], Tout=[tf.float32])



def rms_numpy_raw():
    '''
    :param signal: tf.Tensor
    :param period_length: int
    :return: flattened np.array
    '''

    def inner_fn(signal, period_length):

        signal_np = signal.numpy()
        signal_flat = signal_np.flatten()
        
        rms_values = []
        period_length = int(period_length)
        for i in range(0, len(signal_flat), period_length):
            if i + period_length <= len(signal_flat):
                signal_one_period = signal_flat[i:int(i + period_length)]
                rms_one_period = np.sqrt(np.mean(np.square(signal_one_period))) #rms
                rms_values.append(rms_one_period)
        return tf.convert_to_tensor(rms_values, dtype=tf.float32)

    return lambda signal, period_length: tf.py_function(inner_fn, [signal, period_length], Tout=[tf.float32])


def rms_numpy_class():
    '''
    :param signal: tf.Tensor
    :param period_length: int
    :return: flattened np.array
    '''

    def inner_fn(signal, period_length):

        signal_np = signal.numpy()
        t = Temp()
        rms_values = Temp.apply(signal=signal_np, period_length=period_length)
        return tf.convert_to_tensor(rms_values, dtype=tf.float32)

    return lambda signal, period_length: tf.py_function(inner_fn, [signal, period_length], Tout=[tf.float32])


class Temp(object):
    """docstring for Temp"""
    def __init__(self):
        pass

    def apply(signal, period_length):
        signal_flat = signal.flatten()
        
        rms_values = []
        period_length = int(period_length)
        for i in range(0, len(signal_flat), period_length):
            if i + period_length <= len(signal_flat):
                signal_one_period = signal_flat[i:int(i + period_length)]
                rms_one_period = np.sqrt(np.mean(np.square(signal_one_period))) #rms
                rms_values.append(rms_one_period)
        return rms_values
