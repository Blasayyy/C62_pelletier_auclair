import numpy as np

class Synonymes_Filter:
    def __init__(self, word_to_search, nb_results, score_strategy):
        self.word_to_search = word_to_search
        self.nb_results = nb_results
        self.score_strategy = score_strategy
        self.stop_words = {"le", "ta", "ton", "la"}

    def scalar_product(self, cooc_matrix):
        row_index = self.get_index_from_word(cooc_matrix)
        score = []
        target_row = cooc_matrix[row_index]
        for row in cooc_matrix:
            score.append(np.dot(row, target_row))
        self.score = score

    def get_index_from_word(self, word_indices):
        return word_indices[self.word_to_search]