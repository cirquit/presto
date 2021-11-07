import librosa
import numpy as np
import tensorflow as tf
import tensorflow_io as tfio

_COMMONVOICE_SAMPLING_RATE = 48000 # Hz

def pipeline_definition(source_path, languages, custom_decode_op=False, deterministic_sampling=True):
    '''TODO
    '''
    def get_decoder_part():
        if custom_decode_op:
            # custom implementation that was merged into tf-io
            def _read_mp3_custom(data):
                samples = tfio.audio.decode_mp3(data)
                audio_tensor = tf.cast(samples * (2**(16-1)-1), tf.int16)
                audio_tensor = tf.squeeze(audio_tensor)
                return audio_tensor

            return [
                {
                    "name": "read files",
                    "type": "op",
                    "op": tf.io.read_file,
                    "input_schema": tf.TensorSpec([], tf.string),
                    "output_schema": tf.TensorSpec([], tf.string)
                },
                {
                    "name": "decode mp3",
                    "type": "op",
                    "op": _read_mp3_custom,
                    "input_schema": tf.TensorSpec([], tf.string),
                    "output_schema": tf.TensorSpec([None], tf.int16)
                },
            ]
        else:
            return [
                {
                    "name": "read and decode mp3",
                    "type": "op",
                    "op": _read_decode_mp3,
                    "input_schema": tf.TensorSpec([], tf.string),
                    "output_schema": tf.TensorSpec([None], tf.int16)
                },
            ]
    return [
        {
            "name": "list files",
            "type": "source",
            "op": _read_multiple_tsvs(source_path, languages, deterministic_sampling),
            "output_schema": tf.TensorSpec([], tf.string)
        },
        *get_decoder_part(),
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


def _read_multiple_tsvs(source_path, languages, deterministic_sampling):

    label_file_name = "train.tsv"
    clips_dir_name = "clips"

    label_files = [source_path + "/" + lang + "/" + label_file_name for lang in languages]
    clips_dir = [source_path + "/" + lang + "/" + clips_dir_name for lang in languages]

    datasets = [_ds_from_tsv(label_file, clips_path, deterministic_sampling)
                    for label_file, clips_path in zip(label_files, clips_dir)]

    first_dataset = datasets[0]
    for i, ds in enumerate(datasets):
        if i > 0: # skip first dataset
            first_dataset = first_dataset.concatenate(ds)

    return first_dataset


def _ds_from_tsv(label_file, clips_path, deterministic_sampling):
    ds = tf.data.experimental.CsvDataset(
        label_file,
        [tf.string, tf.string],
        select_cols=[1, 2],
        field_delim="\t",
        use_quote_delim=False,
        header=True
    )
    if not deterministic_sampling:
        # cv-corpus-5.1-singleword/en/train.tsv has 12718 entries => big enough buffer 15k
        ds = ds.shuffle(buffer_size=15000)

    ds = ds.map(lambda p, _: tf.strings.join([clips_path, p], "/"))

    return ds

def _read_decode_mp3(path):
    io_tensor = tfio.IOTensor.graph(tf.float32).from_audio(path)
    audio_tensor = io_tensor.to_tensor()
    audio_tensor = tf.cast(audio_tensor * (2**(32-1)-1), tf.int16)
    audio_tensor = tf.squeeze(audio_tensor)
    return audio_tensor

def _read_mp3():
    # apparently ffmpeg only works in eager mode
    def ffmpeg_decode(path):
        ffmpeg_io = tfio.IOTensor.from_ffmpeg(path)
        audio_io = ffmpeg_io("a:0")
        audio_tensor = audio_io.to_tensor()
        audio_tensor = tf.squeeze(audio_tensor)
        return audio_tensor
    return lambda p: tf.py_function(ffmpeg_decode, [p], tf.int16)


def _read_mp3_librosa():
    def read(path):
        audio_tensor, _ = librosa.core.load(
            path.numpy().decode("ascii"),
            _COMMONVOICE_SAMPLING_RATE
        )

        # librosa returns float32, we want int16 to make storage comparable
        audio_tensor = (audio_tensor * (2**(16-1)-1)).astype(np.int16)
        audio_tensor = tf.squeeze(audio_tensor)
        return audio_tensor
    return lambda p: tf.py_function(read, [p], tf.int16)


def _to_spectrogram(audio_sample, window_s=20e-3, step_s=10e-3, mel_banks=80):
    # stft needs data in float32 in [-1.0,+1.0]
    audio_sample = tf.cast(audio_sample, tf.float32)
    audio_sample /= 2**(16-1)

    # convert from time to frequency domain
    frames_per_second = 1 / window_s
    frame_samples = int(_COMMONVOICE_SAMPLING_RATE / frames_per_second)
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
        sample_rate=_COMMONVOICE_SAMPLING_RATE
    )

    # convert to mel spectrogram
    spectrogram = tf.matmul(spectrogram, linear_to_mel_matrix)

    # convert to log space
    spectrogram = tf.math.log(spectrogram + 1e-8)

    return spectrogram