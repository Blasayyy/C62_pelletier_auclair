import numpy as np
import sqlite3

class DAO:
    def __init__(self):
        pass

    def update_database(self, cooc_matrix, indices, window):
        conn = sqlite3.connect('synonymes.db')
        cur = conn.cursor()
        table_name = "synonymes_w" + str(window)

        # Check if the table exists
        cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cur.fetchone() is not None

        # If the table doesn't exist, create it
        if not table_exists:
            create_table_cmd = f"CREATE TABLE {table_name} ("
            for i in range(len(indices)):
                word = indices[i]
                create_table_cmd += f"{word} INTEGER"
                if i < len(indices) - 1:
                    create_table_cmd += ","
            create_table_cmd += ")"
            cur.execute(create_table_cmd)

        # Iterate over the rows of the co-occurrence matrix and insert or update them in the table
        for i in range(len(indices)):
            row_name = indices[i]
            row_data = cooc_matrix[i]
            cur.execute(f"SELECT rowid FROM {table_name} WHERE rowid=?", (i + 1,))
            row_exists = cur.fetchone() is not None
            if row_exists:
                cur.execute(f"UPDATE {table_name} SET {row_name} = {row_name} + ? WHERE rowid = ?", (row_data, i + 1))
            else:
                insert_row_cmd = f"INSERT INTO {table_name} VALUES ("
                for j in range(len(row_data)):
                    insert_row_cmd += f"{row_data[j]}"
                    if j < len(row_data) - 1:
                        insert_row_cmd += ","
                insert_row_cmd += ")"
                cur.execute(insert_row_cmd)

        conn.commit()
        conn.close()


