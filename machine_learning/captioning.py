import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

from common.common_properties import *
from machine_learning.text_processing import TextProcessingClass


class CaptioningClass:
    def __init__(self, captioning_model_name):
        model = VGG16()
        self.image_features_model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
        self.captioning_model = load_model(get_captioning_model_path(captioning_model_name))
        self.text_processing_class = TextProcessingClass()

    def _extract_features(self, image):
        image = image.resize((224, 224))
        image = np.asarray(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        return self.image_features_model.predict(image, verbose=0)

    def generate_caption(self, image):
        features = self._extract_features(image)

        in_text = start_seq_token
        for _ in range(self.text_processing_class.word_max_len):
            sequence = self.text_processing_class.tokenizer.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence], maxlen=self.text_processing_class.word_max_len)
            yhat = np.argmax(self.captioning_model.predict([features, sequence], verbose=0), axis=-1)
            word = self.text_processing_class.get_word_from_index(yhat)
            if not word:
                break
            in_text += " " + word
            if word == end_seq_token:
                break
        return in_text
