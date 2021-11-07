from pathlib import Path

import librosa
import tensorflow as tf
import tensorflow_io as tfio

_LIBRIVOICE_SAMPLING_RATE = 16000 # Hz

def pipeline_definition(source_path: str):
    '''TODO
    '''
    return [
        {
            "name": "list files",
            "type": "source",
            "op": _ds_from_transcript_files(source_path),
            "output_schema": tf.TensorSpec([], tf.string)
        },
        {
            "name": "read and decode flac",
            "type": "op",
            "op": _read_flac,
            "input_schema": tf.TensorSpec([], tf.string),
            "output_schema": tf.TensorSpec([None], tf.int16)
        },
        {
            "name": "convert to spectrogram",
            "type": "op",
            "op": _to_spectrogram,
            "input_schema": tf.TensorSpec([None], tf.int16),
            "output_schema": tf.TensorSpec([None, 80], tf.float32)
        },
        # here right now to do the full preprocessing benchmark
        # maybe replace with online augmentation
        {
            "name": "identity",
            "type": "op",
            "op": tf.identity,
            "input_schema": tf.TensorSpec([None, 80], tf.float32),
            "output_schema": tf.TensorSpec([None, 80], tf.float32)
        },
    ]


def _ds_from_transcript_files(source_path):
    # Dataset.list_files does not support recursive globs
    transcript_files = [str(path) for path in Path(source_path).rglob("*.txt")]

    ds = tf.data.TextLineDataset(
        transcript_files
    )

    def prepare_file_path(line):
        parts = tf.strings.split(line, maxsplit=1)
        code = parts[0]
        transcript = parts[1]
       
        parts = tf.strings.split(code, sep="-")
        path_prefix = tf.strings.join([source_path, parts[0], parts[1], code], separator="/")
        path = path_prefix + ".flac"

        return path, transcript

    ds = ds.map(prepare_file_path)

    # throw away transcript for now
    ds = ds.map(lambda path, transcript: path)

    return ds


def _read_flac(path):
    io_tensor = tfio.IOTensor.graph(tf.int16).from_audio(path)
    audio_tensor = io_tensor.to_tensor()
    audio_tensor = tf.squeeze(audio_tensor)
    return audio_tensor


def _read_with_librosa():
    def read(path):
        audio_tensor, _ = librosa.core.load(path.numpy(), sr=_LIBRIVOICE_SAMPLING_RATE)
        audio_tensor = tf.squeeze(audio_tensor)
        return audio_tensor
    return lambda p: tf.py_function(read, [p], tf.int16)


def _to_spectrogram(audio_sample, window_s=20e-3, step_s=10e-3, mel_banks=80):
    # stft needs data in float32 in [-1.0,+1.0]
    audio_sample = tf.cast(audio_sample, tf.float32)
    audio_sample /= 2**(16-1)

    # convert from time to frequency domain
    frames_per_second = 1 / window_s
    frame_samples = int(_LIBRIVOICE_SAMPLING_RATE / frames_per_second)
    step_samples = int(frame_samples / (window_s / step_s))
    # smallest power of 2 enclosing frame_samples (960)
    fft_length = 1024
    spectrogram = tf.signal.stft(
        signals=audio_sample,
        frame_length=frame_samples,
        frame_step=step_samples,
        fft_length=fft_length
    )

    # convert complex spectrogram to magnitude spectrogam
    spectrogram = tf.abs(spectrogram)

    # get this as a dynamic variable so that it will be on the same graph as spectrogram
    linear_to_mel_matrix = tf.signal.linear_to_mel_weight_matrix(
        num_mel_bins=mel_banks,
        num_spectrogram_bins=fft_length // 2 + 1,
        sample_rate=_LIBRIVOICE_SAMPLING_RATE
    )

    # convert to mel spectrogram
    spectrogram = tf.matmul(spectrogram, linear_to_mel_matrix)

    # convert to log space
    spectrogram = tf.math.log(spectrogram + 1e-8)

    return spectrogram