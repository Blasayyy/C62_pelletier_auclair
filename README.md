# C62_pelletier_auclair

Notes:

Pour sort le dict:

scores = []

for mot, index in d_vocabulaire.items():
    if index != index_voulu and not in stopwords:
        score = fonction(matrice[index], matrice[index_voulu])
        scores.append((mot, score))

trier apres