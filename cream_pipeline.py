from cream.cream_day import CREAM_Day
from cream.metrics import Electrical_Metrics
import numpy as np
import tensorflow as tf
import glob
import random
from pathlib import Path

# globals
cream_sps = 6400
window_size_s = 10
cream_mains_frequency_hz = 50
window_sample_count = window_size_s * cream_sps
cream_period_length = cream_sps / cream_mains_frequency_hz
cream_sample_day_path  = "/dataset/m1554766/CREAM/X8/2018-08-23"

def pipeline_definition(source_path: str):
    return [
        {
            "name": "list files",
            "type": "source",
            "op": tf.data.Dataset.from_tensor_slices(
                list_files(cream_dataset_path = source_path)
            ),
            "output_schema": tf.TensorSpec((), tf.string)
        },
        {
            "name": "voltage + current extraction 6.4kHz",
            "type": "op+unbatch",
            "op": get_voltage_current_sampled_tf(),
            "input_schema": tf.TensorSpec((), tf.string),
            "output_schema": tf.TensorSpec((2, 64000), tf.float64)
        },
        {
            "name": "active power + rms current + cumsum rms current",
            "type": "op",
            "op": compute_active_power_rms_tf(),
            "input_schema": tf.TensorSpec((2, 64000), tf.float64),
            "output_schema": tf.TensorSpec((3, 500), tf.float64)
        },
        {
            "name": "identity",
            "type": "op",
            "op": tf.identity,
            "input_schema": tf.TensorSpec((3, 500), tf.float64),
            "output_schema": tf.TensorSpec((3, 500), tf.float64)
        }

    ]

def list_files(cream_dataset_path):
    ### <---- depending on how many days you want
    days =  ["2018-08-23" ,"2018-08-24" ,"2018-08-25" ,"2018-08-26" ,"2018-08-27" ,"2018-08-28"
            ,"2018-08-29" ,"2018-08-30" ,"2018-08-31" ,"2018-09-01" ,"2018-09-02" ,"2018-09-03"
            ,"2018-09-04" ,"2018-09-05" ,"2018-09-06" ,"2018-09-07" ,"2018-09-08" ,"2018-09-09"
            ,"2018-09-11" ,"2018-09-12" ,"2018-09-13" ,"2018-09-14" ,"2018-09-15" ,"2018-09-16"
            ,"2018-09-17" ,"2018-09-18" ,"2018-09-19" ,"2018-09-21" ,"2018-09-22" ,"2018-09-23"
            ,"2018-09-24" ,"2018-09-25" ,"2018-09-26" ,"2018-09-27" ,"2018-09-28" ,"2018-09-29"
            ,"2018-09-30" ,"2018-10-01" ,"2018-10-02" ,"2018-10-03" ,"2018-10-04" ,"2018-10-05"
            ,"2018-10-06" ,"2018-10-07" ,"2018-10-08"]
    files = []
    for day in days:
        day_path = cream_dataset_path + "/" + day
        files += glob.glob(day_path + "/*.hdf5", recursive=False)
    return files

def get_voltage_current_sampled(file_path):
    # tuple(np.ndarray(float64), np.ndarray(float64))
    cream_day = CREAM_Day(cream_day_location = cream_sample_day_path)
    voltage, current = cream_day.load_file(file_path = file_path)
    voltage_window_count = int(len(voltage) / window_sample_count)
    voltage_samples = voltage.reshape(voltage_window_count, window_sample_count)
    current_window_count = int(len(current) / window_sample_count)
    current_samples = current.reshape(current_window_count, window_sample_count)
    return voltage_samples, current_samples

def get_voltage_current_sampled_tf():
    '''Returning a lambda that calls an inner function that gets the string tensors and returns
       a (360, 2, 64000) float64 tensor
       => 360seconds, voltage + current = 2, 64000 samples
    '''
    def inner_fn(file_path: tf.Tensor):
        file_path = file_path.numpy().decode('utf-8')
        voltage, current = get_voltage_current_sampled(file_path = file_path)
        zipped = list(zip(voltage, current))
        zipped_tf = tf.convert_to_tensor(np.array(zipped))
        #tf.print(zipped_tf.shape)
        return zipped_tf
    return lambda path: tf.py_function(inner_fn, [path], Tout=[tf.float64])

def compute_active_power_rms(voltage_sample, current_sample, cream_period_length):
    electrical_metrics = Electrical_Metrics()
    active_power = electrical_metrics.active_power(instant_voltage = voltage_sample
                                                 , instant_current = current_sample
                                                 , period_length = cream_period_length)
    rms_current  = electrical_metrics.compute_single_rms(signal = current_sample
                                                       , period_length = cream_period_length)
    return active_power, rms_current

def compute_cumsum(signal_rms):
    differences_np = signal_rms - np.mean(signal_rms)
    return np.cumsum(differences_np)

def compute_active_power_rms_tf():
    '''64000 samples of voltage and current transformed to active power, RMS of the current and its CUMSUM
    (active power) => 64000 / cream_period_length (128) = 500 samples à float64
    (current rms)  => 64000 / cream_period_length (128) = 500 samples à float64
    (cumsum current rms) => 500 samples à float64
    '''
    def inner_fn(element: tf.Tensor):
        voltage = element[0].numpy()
        current = element[1].numpy()
        active_power, rms_current = compute_active_power_rms(voltage_sample = voltage
                                                           , current_sample = current
                                                           , cream_period_length = cream_period_length)
        cumsum_rms_current = compute_cumsum(rms_current)
        return tf.convert_to_tensor([active_power, rms_current, cumsum_rms_current])
    return lambda element: tf.py_function(inner_fn, [element], Tout=[tf.float64])
