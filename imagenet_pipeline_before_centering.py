import tensorflow as tf

def pipeline_definition(src_path: str):
    '''Our proposed way to defined the preprocessing pipeline. It's converted to a tf.data.Dataset via pipeline.py
    Check demo.py for the example usage.

    Each step is a dict with the following keys:
    * "name": str
    * "type": str - either "op" or "source" (source does not have an input schema)
    * "op": a function that transforms the data in form of "input_schema" to "output_schema"
    * "input_schema": tf.TensorSpec - i.e., the type of the data
    * "output_schema": tf.TensorSpec - i.e., the type of the data

    :param src_path: str
    :return: list(dict)
    '''

    return [
        {
            "name": "list files",
            "type": "source",
            "op": tf.data.Dataset.list_files([
                src_path + "/*/*." + ext
                for ext in ["jpeg", "bmp", "png", "JPEG"]]
              , seed = 42
            ),
            "output_schema": tf.TensorSpec([], tf.string)
        },
        {
            "name": "read image",
            "type": "op",
            "op": tf.io.read_file,
            "input_schema": tf.TensorSpec([], tf.string),
            "output_schema": tf.TensorSpec([], tf.string)
        },
        {
            "name": "decode image",
            "type": "op",
            "op": _decode_image,
            "input_schema": tf.TensorSpec([], tf.string),
            "output_schema": tf.TensorSpec([None, None, 3], tf.uint8)
        },
        {
            "name": "resize image",
            "type": "op",
            "op": _minsize_scale,
            "input_schema": tf.TensorSpec([None, None, 3], tf.uint8),
            "output_schema": tf.TensorSpec([None, None, 3], tf.uint8)
        },
        {
            "name": "apply greyscale",
            "type": "op",
            "op": tf.image.rgb_to_grayscale,
            "input_schema": tf.TensorSpec([None, None, 3], tf.uint8),
            "output_schema": tf.TensorSpec([None, None, 1], tf.uint8)
        },
        {
            "name": "center pixel values",
            "type": "op",
            "op": _center_pixel_values,
            "input_schema": tf.TensorSpec([None, None, 1], tf.float32),
            "output_schema": tf.TensorSpec([None, None, 1], tf.float32)
        },
        {
            "name": "random crop",
            "type": "op",
            "op": _random_crop,
            "input_schema": tf.TensorSpec([None, None, 1], tf.float32),
            "output_schema": tf.TensorSpec([224, 224, 1], tf.float32)
        },
    ]


def _decode_image(encoded):
    return tf.io.decode_image(encoded, channels=3, expand_animations=False)

def _scale_and_crop(image):
    # scale
    shape = tf.shape(image)
    h = shape[0]
    w = shape[1]
    scaler = tf.constant(256.0) / tf.cast(tf.math.reduce_min([h, w]), tf.float32)
    new_h = tf.cast(tf.cast(h, tf.float32) * scaler, tf.int32)
    new_w = tf.cast(tf.cast(w, tf.float32) * scaler, tf.int32)
    image = tf.image.resize(image, [new_h, new_w])

    # crop
    image = tf.image.resize_with_crop_or_pad(image, 224, 224)

    return image

def _minsize_scale(image, min_length=256):
    # scale
    shape = tf.shape(image)
    h = shape[0]
    w = shape[1]
    scaler = tf.constant(min_length, tf.float32) / tf.cast(tf.math.reduce_min([h, w]), tf.float32)
    new_h = tf.cast(tf.cast(h, tf.float32) * scaler, tf.int32)
    new_w = tf.cast(tf.cast(w, tf.float32) * scaler, tf.int32)
    image.set_shape([None, None, None])
    image = tf.image.resize(image, [new_h, new_w])

    # convert back to uint8
    image = tf.cast(image, tf.uint8)

    return image

def _random_crop(image, crop_shape=(224, 224, 1)):
    return tf.image.random_crop(image, crop_shape)

def _center_pixel_values(image):
    image = tf.cast(image, tf.float32)
    image /= 127.5
    image -= 1.0
    return image

