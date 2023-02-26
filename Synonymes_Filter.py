import numpy as np

class Synonymes_Filter:
    def __init__(self, word_to_search, nb_results, score_strategy, word_indices):
        self.word_to_search = word_to_search
        self.nb_results = nb_results
        self.score_strategy = score_strategy
        self.stop_words = {"le", "ta", "ton", "la", "de", "et", "l", "à"}
        self.word_indices = word_indices

    def scalar_product(self, cooc_matrix):
        row_index = self.get_index_from_word()
        score = []
        target_row = cooc_matrix[row_index]
        for row in cooc_matrix:
            score.append(np.dot(row, target_row))
        self.score = score

    def city_block(self, cooc_matrix):
        row_index = self.get_index_from_word()
        target_row = cooc_matrix[row_index]
        score = []
        for row in cooc_matrix:
            score.append(np.abs(row - target_row).sum())
        self.score = score


    def get_index_from_word(self):
        return self.word_indices[self.word_to_search]

    def get_top_words(self):
        index_sort = np.argsort(self.score)[::-1]
        flipped_word_indices = {v: k for k, v in self.word_indices.items()}
        counter = 0

        with open(r'stop_words_french.txt', 'r') as file:
            content = file.read()

            for index in index_sort[0:75]:
                if counter > 5:
                    break
                if flipped_word_indices[index] in content:
                    continue
                print(f'{flipped_word_indices[index]} : {self.score[index]}')
                counter += 1

            # if 'Line 8' in content:
            #     print('string exist')
            # else:
            #     print('string does not exist')

        # for index in index_sort[0:50]:
        #     if counter > 5:
        #         break
        #     if flipped_word_indices[index] in self.stop_words:
        #         continue
        #     print(f'{flipped_word_indices[index]} : {self.score[index]}')
        #     counter += 1

