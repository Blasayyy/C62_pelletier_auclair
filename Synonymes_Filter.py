import numpy as np

class Synonymes_Filter:
    def __init__(self, word_to_search, nb_results, score_strategy, cooc_matrix, word_indices):
        self.word_to_search = word_to_search
        self.nb_results = nb_results
        self.score_strategy = score_strategy
        self.word_indices = word_indices
        self.cooc_matrix = cooc_matrix
        self.top_results = []

    def get_score(self):
        row_index = self.get_index_from_word()
        target_row = self.cooc_matrix[row_index]
        score = []
        for row in self.cooc_matrix:
            if self.score_strategy == 0:
                score.append(np.sum(np.square(row - target_row)))
            elif self.score_strategy == 1:
                score.append(np.dot(row, target_row))
            elif self.score_strategy == 2:
                score.append(np.abs(row - target_row).sum())

        self.score = score

    def get_index_from_word(self):
        return self.word_indices[self.word_to_search]

    def get_top_words(self):
        if self.score_strategy >= 1:
            index_sort = np.argsort(self.score)[::-1]
        else:
            index_sort = np.argsort(self.score)

        top_counter = 0
        index_counter = 0

        stop_words = open('FichiersTexte/stop_words_french.txt', 'r', encoding="utf-8").read()

        while top_counter < self.nb_results:
            index = index_sort[index_counter]

            if self.word_indices[index] in stop_words or self.word_indices[index] == self.word_to_search:
                index_counter += 1
                continue
            else:
                top_counter += 1
                index_counter += 1
                if self.score[index] and self.word_indices[index]:
                    self.top_results.append(f'{self.word_indices[index]} : {self.score[index]}')

        return self.top_results

