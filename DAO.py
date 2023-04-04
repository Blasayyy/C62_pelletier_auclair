import numpy as np
import sqlite3

class DAO:
    def __init__(self):
        pass

    def create_synonymes_table(self):
        conn = sqlite3.connect('synonymes_db.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS synonymes (word_1 TEXT, word_2 TEXT, window INTEGER, score INTEGER)''')

        conn.commit()
        conn.close()

    def update_database(self, cooccurrence_matrix, index_dict, window):
        # get the non-zero indices and values from the co-occurrence matrix
        nonzero_indices = np.nonzero(cooccurrence_matrix)
        values = cooccurrence_matrix[nonzero_indices]

        # connect to the database
        conn = sqlite3.connect('synonymes_db.db')

        # create a cursor object
        c = conn.cursor()

        # loop through the non-zero indices and insert the corresponding data into the database
        for i in range(len(nonzero_indices[0])):
            index_1 = nonzero_indices[0][i]
            index_2 = nonzero_indices[1][i]
            word_1 = index_dict[index_1]
            word_2 = index_dict[index_2]
            score = values[i]
            c.execute("INSERT INTO synonymes (word_1, word_2, window, score) VALUES (?, ?, ?, ?)",
                      (word_1, word_2, window, score))

        # commit the changes and close the connection
        conn.commit()
        conn.close()


    # def update_database(self, cooc_matrix, indices, window):
    #     conn = sqlite3.connect('synonymes.db')
    #     cur = conn.cursor()
    #     table_name = "synonymes_w" + str(window)
    #
    #
    #     cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    #     table_exists = cur.fetchone() is not None
    #
    #
    #     if not table_exists:
    #         create_table_cmd = f"CREATE TABLE {table_name} ("
    #         for i in range(len(indices)):
    #             word = indices[i]
    #             create_table_cmd += f"{word} INTEGER"
    #             if i < len(indices) - 1:
    #                 create_table_cmd += ","
    #         create_table_cmd += ")"
    #         cur.execute(create_table_cmd)
    #
    #
    #     for i in range(len(indices)):
    #         row_name = indices[i]
    #         row_data = cooc_matrix[i]
    #         cur.execute(f"SELECT rowid FROM {table_name} WHERE rowid=?", (i + 1,))
    #         row_exists = cur.fetchone() is not None
    #         if row_exists:
    #             cur.execute(f"UPDATE {table_name} SET {row_name} = {row_name} + ? WHERE rowid = ?", (row_data, i + 1))
    #         else:
    #             insert_row_cmd = f"INSERT INTO {table_name} VALUES ("
    #             for j in range(len(row_data)):
    #                 insert_row_cmd += f"{row_data[j]}"
    #                 if j < len(row_data) - 1:
    #                     insert_row_cmd += ","
    #             insert_row_cmd += ")"
    #             cur.execute(insert_row_cmd)
    #
    #     conn.commit()
    #     conn.close()


