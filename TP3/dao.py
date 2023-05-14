import sqlite3

CHEMIN_BD = 'cooccurrences.db'
FK = 'PRAGMA foreign_keys = 1'

CREER_MOT = '''
CREATE TABLE IF NOT EXISTS mot
(
    id INTEGER PRIMARY KEY NOT NULL,
    chaine CHAR(26) NOT NULL
)
'''
DROP_MOT = 'DROP TABLE IF EXISTS mot'
INSERER_MOT = 'INSERT OR IGNORE INTO mot(chaine, id) VALUES(?,?)'
CHARGER_MOT = 'SELECT chaine, id FROM mot'

CREER_COOCCURRENCE = '''
CREATE TABLE IF NOT EXISTS cooccurrence
(
    id_mot INTEGER NOT NULL REFERENCES mot(id),
    id_cooccurrence INTEGER NOT NULL REFERENCES mot(id),
    taille_fenetre INTEGER NOT NULL,
    frequence INTEGER NOT NULL,
    PRIMARY KEY(id_mot, id_cooccurrence, taille_fenetre)
)
'''

DROP_COOCCURRENCE = 'DROP TABLE IF EXISTS cooccurrence'
INSERER_COOCCURRENCE = 'INSERT OR REPLACE INTO cooccurrence VALUES(?,?,?,?)'
CHARGER_COOCCURRENCE = 'SELECT id_mot, id_cooccurrence, frequence FROM cooccurrence WHERE taille_fenetre = ?'

class DAO():
    def __init__(self, chemin = CHEMIN_BD):
        self.chemin = chemin

    def __enter__(self):
        self.connexion = sqlite3.connect(self.chemin)
        self.curseur = self.connexion.cursor()
        self.curseur.execute(FK)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.curseur.close()
        self.connexion.close()

    def creer_tables(self):
        self.curseur.execute(DROP_COOCCURRENCE)
        self.curseur.execute(DROP_MOT)
        self.curseur.execute(CREER_MOT)
        self.curseur.execute(CREER_COOCCURRENCE)

    def inserer_mots(self, mots):
        self.curseur.executemany(INSERER_MOT, mots)
        self.connexion.commit()

    def inserer_cooccurrences(self, cooccurrences):
        self.curseur.executemany(INSERER_COOCCURRENCE, cooccurrences)
        self.connexion.commit()

    def charger_mots(self):
        self.curseur.execute(CHARGER_MOT)
        return self.curseur.fetchall()

    def charger_cooccurrences(self, tfen):
        self.curseur.execute(CHARGER_COOCCURRENCE, (tfen,))
        return self.curseur.fetchall()
