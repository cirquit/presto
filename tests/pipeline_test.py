import numpy as np
import tensorflow as tf
import unittest

from presto import pipeline

class PipelineTest(unittest.TestCase):

    def test_singleton(self):
        data = tf.random.uniform((3, 3), dtype=tf.int32, maxval=10)
        schema = tf.TensorSpec([3, 3], tf.int32)

        serializer = pipeline.serializer(schema)
        serialized = serializer(data)

        print(serialized)

        deserializer = pipeline.deserializer(schema)
        deserialized = deserializer(serialized)

        np.testing.assert_allclose(data, deserialized)

    def test_singleton_string(self):
        data = tf.constant(b"deadbeef")
        schema = tf.TensorSpec((), tf.string)

        serializer = pipeline.serializer(schema)
        serialized = serializer(data)

        print(serialized)

        deserializer = pipeline.deserializer(schema)
        deserialized = deserializer(serialized)

        self.assertEqual(data, deserialized)

    def test_structured(self):
        data1 = tf.random.uniform((3, 3), dtype=tf.int32, maxval=10)
        data2 = tf.random.uniform((4,), dtype=tf.float32)
        data3 = tf.constant(b"deadbeef", dtype=tf.string)
        data = dict(d1=data1, d2=data2, d3=data3)

        schema = dict(
            d1=tf.TensorSpec((3, 3), dtype=tf.int32),
            d2=tf.TensorSpec((4,), dtype=tf.float32),
            d3=tf.TensorSpec((), dtype=tf.string)
        )

        serializer = pipeline.serializer(schema)
        serialized = serializer(data)

        print(serialized)

        deserializer = pipeline.deserializer(schema)
        deserialized = deserializer(serialized)

        self.assertSetEqual(set(data.keys()), set(deserialized.keys()))
        np.testing.assert_array_almost_equal(data["d1"], deserialized["d1"])
        np.testing.assert_array_almost_equal(data["d2"], deserialized["d2"])
        self.assertEqual(data3, deserialized["d3"])

    def test_ds(self):
        def gen():
            for i in range(3):
                a = tf.eye(2, dtype=tf.int32) * i
                b = tf.eye(3, dtype=tf.float32) * i
                yield dict(a=a, b=b, c=b"deadbeef")

        ds = tf.data.Dataset.from_generator(gen, dict(a=tf.int32, b=tf.float32, c=tf.string))

        schema = {
            "a": tf.TensorSpec((2, 2), tf.int32),
            "b": tf.TensorSpec((3, 3), tf.float32),
            "c": tf.TensorSpec((), tf.string)
        }

        ds = ds.map(pipeline.serializer(schema))
        ds = ds.map(pipeline.deserializer(schema))

        for i in ds:
            print(i)


if __name__ == "__main__":
    unittest.main()
