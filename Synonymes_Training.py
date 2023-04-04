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
        self.non_zero_matrix = None
        self.non_zero_indices = None


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
        self.fix_window()
        window = self.window

        # get a list of unique words in the input list
        unique_words = list(set(self.words))
        self.unique_words = unique_words
        num_words = len(unique_words)

        # create a dictionary to map each word to its index in the matrix
        word_indices = {word: i for i, word in enumerate(unique_words)}
        self.word_indices = word_indices

        # initialize a 2D numpy array with zeros
        cooc_mat = np.zeros((num_words, num_words))

        # iterate over the input list of words and count co-occurrences within the window
        for i, word in enumerate(self.words):
            for j in range(i - window, i + window + 1):
                if j != i:
                    try:
                        cooc_mat[word_indices[word], word_indices[self.words[j]]] += 1
                    except:
                        pass

        self.cooc_matrix = cooc_mat

    def split_text_into_words(self):
        # splits text into words, not counting punctuation
        words = re.findall(r'\b\w+\b', self.text)
        # converts list to lowercase
        words = [word.lower() for word in words]

        self.words = words

    def fix_window(self, window):
        if window % 2 == 0:
            window_fixed = window / 2
        else:
            window_fixed = (window - 1) / 2

        self.window = window_fixed


    def remove_zero_entries(self):
        non_zero_rows, non_zero_cols = np.nonzero(self.cooc_matrix)
        unique_rows = np.unique(non_zero_rows)
        unique_cols = np.unique(non_zero_cols)
        new_matrix = self.cooc_matrix[unique_rows][:, unique_cols]
        new_index_dict = {new_index: word for new_index, (old_index, word) in enumerate(self.word_indices.items()) if
                          old_index in unique_cols}
        self.non_zero_matrix = new_matrix
        self.non_zero_indices = new_index_dict
