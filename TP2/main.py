import sys

import Synonymes_Filter as sf
import Synonymes_Training as st
import argparse


def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', action='store_true')
    group.add_argument('-r', action='store_true')
    group.add_argument('-b', action='store_true')
    group.add_argument('-q', action='store_true')

    parser.add_argument('-t', type=int, help='taille de la fenetre')
    parser.add_argument('--enc', type=str, help='encodage du fichier')
    parser.add_argument('--chemin', type=str, help='chemin du corpus dentraienemnt')

    trainer = None

    args = parser.parse_args()

    if args.e:
        print('entrainement')
        fenetre = args.t
        enc = args.enc
        chemin = args.chemin

        trainer = st.Synonymes_Training(chemin, enc)
        trainer.read()
        trainer.create_cooccurrence_matrix(int(fenetre))

        parser.parse_args()

    elif args.r:
        print('recherche')
        fenetre = args.t

        text = input("\nEntrez un mot et la méthode de calcul"
                     "\n i.e. produit scalaire: 0, least-squares: 1, city-block: 2\n\nTapez -q pour quitter.\n\n")

        text = text.split()

        print(text[0], text[1])

        if text[0] == "-q":
            sys.exit()

        syn_filter = sf.Synonymes_Filter(text[0], fenetre, int(text[1]), trainer.cooc_matrix, trainer.word_indices)
        syn_filter.get_score()

        syn_filter.get_top_words()

        print("\n")
        for word in syn_filter.top_results:
            print(word)

    elif args.b:
        print('regenerer')

    elif args.q:
        sys.exit()


if __name__ == '__main__':
    main()
