import tensorflow as tf 

devices = tf.config.list_physical_devices('GPU')

if len(devices) > 0:
    print("## Using GPU ##")
else:
    print("## Using CPU ###")