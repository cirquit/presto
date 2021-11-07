import newspaper
import numpy as np
import tensorflow as tf
import tensorflow_text as text


def pipeline_definition(src_path):
    # vocabulary size 50001, GPT2 originally used 50257
    vocabulary_size = 50001
    bpe_model_path = tf.keras.utils.get_file("bpe_en_50k.model", "https://nlp.h-its.org/bpemb/en/en.wiki.bpe.vs50000.model")
    bpe_model = open(bpe_model_path, 'rb').read()

    embedding_dimension = 768
    bpe_tokernizer = text.SentencepieceTokenizer(model=bpe_model, out_type=tf.dtypes.int32)
    return [
        {
            "name": "read files",
            "type": "source",
            "op": tf.data.Dataset.list_files(src_path + "/*.txt").map(tf.io.read_file),
            "output_schema": tf.TensorSpec([], tf.string)
        },
        {
            "name": "extract content",
            "type": "op",
            "op": _extract_html_tf,
            "input_schema": tf.TensorSpec([], tf.string),
            "output_schema": tf.TensorSpec([], tf.string)
        },
        {
            "name": "byte pair encoding",
            "type": "op",
            "op": _apply_bpe_tokenizer(bpe_tokernizer),
            "input_schema": tf.TensorSpec([], tf.string),
            "output_schema": tf.TensorSpec([None], tf.int32)
        },
        {
            "name": "lookup embedding",
            "type": "op",
            "op": _get_embedding_lookup(vocabulary_size, embedding_dimension),
            "input_schema": tf.TensorSpec([None], tf.int32),
            "output_schema": tf.TensorSpec([None, embedding_dimension], tf.float32)
        },
        {
            "name": "identity",
            "type": "op",
            "op": tf.identity,
            "input_schema": tf.TensorSpec([None, embedding_dimension], tf.float32),
            "output_schema": tf.TensorSpec([None, embedding_dimension], tf.float32)
        },
    ]


def _extract_html_tf(html_tensor):
    """Extract main text from scraped HTML."""

    # call from graph into Python
    content = tf.py_function(_extract_html, [html_tensor], tf.string)

    # necessary for some reason
    content = tf.ensure_shape(content, ())

    return content


def _extract_html(eager_html_tensor):
    try:
        article = newspaper.Article(url="", fetch_images=False)
        article.set_html(eager_html_tensor.numpy())
        article.parse()
    # newspaper seems to get some strange errors on this dataset, probably some malformed html
    # this happend 2-3 times in the whole dataset, so it hopefully does not change the final
    # throughput and processing time. On average, a text file has 42.77KB, UTF8 encoded. For
    # simplicity I'll assume 1 byte per char on average as we're dealing with raw text. The change
    # between the raw and extracted file sizes are negligible, so we're just copying them. We're
    # creating 44KB of text as filler:
    # "Hello world" = 11 chars => 11 byte * 4000 = 44000 byte = 44 KB
    except:
        return ["Hello World"]*4000
    return article.text


def _apply_bpe_tokenizer(bpe_tokernizer):
    def tokenize(text_tensor):
        return bpe_tokernizer.tokenize(text_tensor)
    return tokenize


def _get_embedding_lookup(vocabulary_size, embedding_dimension):
    # there is no fitting real embedding on https://nlp.h-its.org/bpemb/en/
    # but actual numbers are not important for us anyways
    # we are also going to not do the positional encoding here, as https://huggingface.co/transformers/model_doc/gpt2.html#gpt2tokenizer also doesnt do that
    em = np.random.random((vocabulary_size, embedding_dimension)).astype(np.float32)
    embedding_lookup = lambda token_ids: tf.nn.embedding_lookup(em, token_ids)

    return embedding_lookup
