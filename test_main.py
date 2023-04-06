from Synonymes_Training import Synonymes_Training as st
import DAO
from datetime import datetime

def main():
    current_time = datetime.now()
    chemin = ".\FichiersTexte\GerminalUTF8.txt"
    enc = "utf-8"
    fenetre = 10

    trainer = st(chemin, enc)
    trainer.read()
    trainer.create_cooccurrence_matrix(int(fenetre))

    dao = DAO.DAO()
    dao.create_synonymes_table()
    dao.delete_data()
    dao.update_database(trainer.cooc_matrix, trainer.word_indices, fenetre)
    result = dao.get_top_related_words("antique", 10, 10)
    for w, s in result:
        print(w, s)

    endtime = datetime.now()
    print(endtime - current_time)
if __name__ == '__main__':
    quit(main())