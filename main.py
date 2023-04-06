import DAO
import Synonymes_Training as st
import argparse


def main():
    parser = argparse.ArgumentParser()
    dao = DAO.DAO()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', action='store_true')
    group.add_argument('-r', action='store_true')
    group.add_argument('-b', action='store_true')

    parser.add_argument('-t', type=int, help='taille de la fenetre')
    parser.add_argument('--enc', type=str, help='encodage du fichier')
    parser.add_argument('--chemin', type=str, help='chemin du corpus dentraienemnt')

    args = parser.parse_args()

    if args.e:
        print('Entraînement: en cours..\n')
        fenetre = args.t
        enc = args.enc
        chemin = args.chemin

        trainer = st.Synonymes_Training(chemin, enc)
        trainer.read()
        trainer.create_cooccurrence_matrix(int(fenetre))

        dao.create_synonymes_table()

        dao.update_database(trainer.cooc_matrix, trainer.word_indices, fenetre)
        print('Complété')

    elif args.r:
        print('Recherche :\n')
        fenetre = args.t

        mot = input("Entrez un mot: ")
        resulats = input("\nEntrez le nombre de résultats à afficher: ")
        mode = -1
        while mode < 0 or mode > 2:
            mode = int(input("\nEt finalement la méthode de calcul: produit scalaire - 0, least-squares - 1, city-block - 2: "))
        print("\n")

        result = dao.get_top_related_words(mot, resulats, fenetre, mode)

        if len(result) < 1:
            print("Aucun résultats")
        else:
            for w, s in result:
                print(w, s)

    elif args.b:
        print('La table à été supprimée')
        dao.delete_data()


if __name__ == '__main__':
    quit(main())
