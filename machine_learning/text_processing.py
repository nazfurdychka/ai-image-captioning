import re
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer

from common.common_properties import *


class TextProcessingClass:
    def __init__(self):
        captions_data = pd.read_csv(path_to_captions_csv)
        captions_data = self._clean_captions(captions_data)
        self.tokenizer = self._init_tokenizer(captions_data)
        self.vocab_len = len(self.tokenizer.word_index) + 1
        self.word_max_len = max(len(caption.split()) for caption in captions_data[comment_column_name])

    def get_word_from_index(self, index):
        for word, i in self.tokenizer.word_index.items():
            if i == index:
                return word
        return None

    def _init_tokenizer(self, captions_data):
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(captions_data[comment_column_name])

        return tokenizer

    def _clean_captions(self, captions_data):
        captions_data[comment_column_name] = captions_data[comment_column_name].apply(self._preprocess_text)
        captions_data[comment_column_name] = captions_data[comment_column_name].apply(self._add_word_tokens)

        return captions_data

    def _preprocess_text(self, comment):
        article_words = ['a', 'the']
        comment = re.sub(r'[^a-z ]', '', comment.lower())
        comment = ' '.join([word for word in comment.split() if word not in article_words])
        return comment

    def _add_word_tokens(self, text):
        return start_seq_token + ' ' + text + ' ' + end_seq_token
