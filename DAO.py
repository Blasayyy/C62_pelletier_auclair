import numpy as np
import sqlite3

class DAO:
    def __init__(self):
        self.connection = sqlite3.connect("synonymes.db")
        self.cursor = self.connection.cursor()

    def update_database(self, cooc_matrix, indices, window):
        table_name = "synonyms_w" + str(indices)


