from sys import argv
import re
import numpy as np

class Synonymes_Training:
    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.text = None
        self.words = None
        self.cooc_matrix = None
        self.word_indices = None
        self.window = None

    def __enter__(self):
        self.read()
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        self.f.close()

    def read(self):
        self.f = open(self.path, 'r', encoding=self.encoding)
        self.text = self.f.read()

    def create_cooccurrence_matrix(self, window):
        self.split_text_into_words()
        self.fix_window(window)
        window = self.window

        unique_words = list(set(self.words))
        self.unique_words = unique_words
        num_words = len(unique_words)

        word_indices = {word: i for i, word in enumerate(unique_words)}
        self.word_indices = word_indices

        cooc_mat = np.zeros((num_words, num_words))

        for i, word in enumerate(self.words):
            for j in range(i - window, i + window + 1):
                if j != i:
                    try:
                        cooc_mat[word_indices[word], word_indices[self.words[j]]] += 1
                    except:
                        pass

        self.cooc_matrix = cooc_mat

    def split_text_into_words(self):
        words = re.findall(r'\b\w+\b', self.text)
        words = [word.lower() for word in words]
        self.words = words

    def fix_window(self, window):
        if window % 2 == 0:
            window_fixed = window / 2
        else:
            window_fixed = (window - 1) / 2

        self.window = int(window_fixed)