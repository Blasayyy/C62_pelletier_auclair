import csv
from collections import defaultdict
import numpy as np
from scipy.spatial import distance


def assign_word_types(words, filename):
    word_data = defaultdict(lambda: {'type': '', 'freq': 0})

    with open(filename, 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            word = row[0]
            word_type = row[3]
            freq = float(row[9])

            if word_data[word]['freq'] < freq:
                word_data[word]['type'] = word_type
                word_data[word]['freq'] = freq

    typed_words = []
    for word, id in words:
        word_type = word_data[word]['type'] if word in word_data else 'UNK'
        typed_words.append((id, word, word_type))

    return typed_words


def create_data_matrix(cooccurrences, vocabulaire_data):
    words = set()
    cooccur = set()
    for id_word, id_cooccurrence, _ in cooccurrences:
        words.add(id_word)
        cooccur.add(id_cooccurrence)

    word_to_idx = {word: i for i, word in enumerate(sorted(words))}
    cooccur_to_idx = {cooccurrence: i for i, cooccurrence in enumerate(sorted(cooccur))}

    data = np.zeros((len(words), len(cooccur)))

    for id_word, id_cooccurrence, frequency in cooccurrences:
        data[word_to_idx[id_word], cooccur_to_idx[id_cooccurrence]] = frequency

    vocab_dict = {index: word for word, index in vocabulaire_data}
    vocab_list = [vocab_dict.get(index) for index in range(len(vocab_dict))]

    return data, vocab_list

def print_closest_words(centroids, data, typed_words, cluster_types, cluster_type_counts, n):
    for i, centroid in enumerate(centroids):
        dists = distance.cdist([centroid], data, 'euclidean')[0]
        closest_words = np.argsort(dists)[:n]
        print(f'Centroid {i} -> cgram: {cluster_types[i]} ({cluster_type_counts[i]} votes)')
        for word_idx in closest_words:
            word_id, word, word_type = typed_words[word_idx]
            print(f'\t{word} ({word_type}) --> {dists[word_idx]}')

