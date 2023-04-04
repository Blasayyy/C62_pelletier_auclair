from Synonymes_Training import Synonymes_Training as st
import DAO

def main():
    chemin = ".\FichiersTexte\DonQuichotteUTF8.txt"
    enc = "utf-8"
    fenetre = 5

    trainer = st(chemin, enc)
    trainer.read()
    trainer.create_cooccurrence_matrix(int(fenetre))

    dao = DAO.DAO()
    dao.create_synonymes_table()
    dao.update_database(trainer.cooc_matrix, trainer.word_indices, fenetre)

if __name__ == '__main__':
    quit(main())