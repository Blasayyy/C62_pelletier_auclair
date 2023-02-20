from sys import argv
import re
import numpy as np

class Synonymes_Training:
    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.text = None
        self.words = None


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
        window = self.fix_window(window)
        print(window)

        # Get a list of unique words in the input list
        unique_words = list(set(self.words))
        num_words = len(unique_words)

        # Create a dictionary to map each word to its index in the matrix
        word_indices = {word: i for i, word in enumerate(unique_words)}
        print(word_indices)

        # Initialize a 2D numpy array with zeros
        cooc_mat = np.zeros((num_words, num_words))

        # Iterate over the input list of words and count co-occurrences within the window
        for i, word in enumerate(self.words):
            for j in range(i - window, i + window + 1):
                if j != i and j >= 0 and j < len(self.words):
                    other_word = self.words[j]
                    if other_word in unique_words:
                        cooc_mat[word_indices[word], word_indices[other_word]] += 1

        self.cooc_matrix = cooc_mat

    def split_text_into_words(self):
        # splits text into words, not counting punctuation that isn't an end of sentence character (.?!)
        words = re.findall(r"\b\w+\b|[.!?]", self.text)
        words = [word.lower() for word in words]

        self.words = words

    def fix_window(self, window):
        if window % 2 == 0:
            window_fixed = window / 2
        else:
            window_fixed = (window - 1) / 2

        return int(window_fixed)

def main():
    chemin = "Tisane.txt"
    enc = "utf-8"

    trainer = Synonymes_Training(chemin, enc)
    trainer.read()
    trainer.create_cooccurrence_matrix(5)
    print(trainer.cooc_matrix)

    return 0

if __name__ == '__main__':
    quit(main())