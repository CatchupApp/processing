import text_eval
import public_parsing_ops
import tensorflow as tf
import numpy as np

_SPM_VOCAB = 'ckpt/c4.unigram.newline.10pct.96000.model'
encoder = public_parsing_ops.create_text_encoder("sentencepiece",
                                                 _SPM_VOCAB)
shapes = {
    'cnn_dailymail': (1024, 128),
    'gigaword':(128, 32)
}

def summarize(text, model_dir="model/gigaword", model_name="gigaword"):
    shape,_ = shapes[model_name]

    input_ids = encoder.encode(text)
    inputs = np.zeros(shape)
    idx = len(input_ids)
    if idx>shape: idx =shape

    inputs[:idx] = input_ids[:idx]
    imported = tf.saved_model.load(model_dir, tags='serve')
    example = tf.train.Example()
    example.features.feature["inputs"].int64_list.value.extend(inputs.astype(int))
    output = imported.signatures['serving_default'](examples=tf.constant([example.SerializeToString()]))

    return text_eval.ids2str(encoder, output['outputs'].numpy(), None)


text = open("ex2.txt", "r", encoding="utf-8").read()

print(summarize(text))
