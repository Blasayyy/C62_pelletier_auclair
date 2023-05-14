import sqlite3

class DAO:
    def __init__(self):
        pass

    def create_synonymes_table(self):
        conn = sqlite3.connect('synonymes_db.db')
        c = conn.cursor()

        c.execute(
            '''CREATE TABLE IF NOT EXISTS synonymes 
               (word_1 TEXT, word_2 TEXT, window INTEGER, score INTEGER, 
               PRIMARY KEY (word_1, word_2, window))''')
        c.execute('CREATE INDEX IF NOT EXISTS pk_index ON synonymes (word_1, word_2, window)')

        conn.commit()
        conn.close()

    def update_database(self, cooc_matrix, index_dict, window):
        conn = sqlite3.connect('synonymes_db.db')
        c = conn.cursor()
        with open('.\FichiersTexte\stop_words_french.txt', 'r', encoding='utf-8') as f:
            stop_words = set(line.strip() for line in f)

        index_dict = {v: k for k, v in index_dict.items()}
        nonzero_indices = cooc_matrix.nonzero()
        values = cooc_matrix[nonzero_indices]
        for i in range(nonzero_indices[0].shape[0]):
            index_1 = nonzero_indices[0][i]
            index_2 = nonzero_indices[1][i]
            word_1 = index_dict[index_1]
            word_2 = index_dict[index_2]
            score = values[i]
            if word_1 > word_2:
                word_1, word_2 = word_2, word_1
            if word_1 not in stop_words and word_2 not in stop_words:
                c.execute('''INSERT INTO synonymes (word_1, word_2, window, score)
                             VALUES (?, ?, ?, ?)
                             ON CONFLICT(word_1, word_2, window) DO UPDATE SET score = score + excluded.score''',
                          (word_1, word_2, window, score))

        conn.commit()
        conn.close()

    def delete_data(self):
        conn = sqlite3.connect('synonymes_db.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS synonymes')


        conn.commit()
        conn.close()

        self.create_synonymes_table()

    def get_top_related_words(self, word, size, window, mode):
        conn = sqlite3.connect('synonymes_db.db')
        c = conn.cursor()
        self.mode = mode

        c.execute('''SELECT word_2, score
                     FROM synonymes
                     WHERE word_1 = ? AND window = ?
                     UNION
                     SELECT word_1, score
                     FROM synonymes
                     WHERE word_2 = ? AND window = ?
                     ORDER BY score DESC
                     LIMIT ?''', (word, window, word, window, size))

        results = [(w, s) for w, s in c.fetchall() if w != word]

        conn.close()

        return results