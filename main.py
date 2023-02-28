import sys

import Synonymes_Filter as sf
import Synonymes_Training as st
from sys import argv



def main():
    chemin = "DonQuichotteUTF8.txt"
    enc = "utf-8"

    fenetre = argv[1]
    enc = argv[2]
    chemin = argv[3]



    print(argv[1], argv[2], argv[3])

    trainer = st.Synonymes_Training(chemin, enc)
    trainer.read()
    trainer.create_cooccurrence_matrix(int(fenetre))

    text = input("\nEntrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul"
          "\n i.e. produit scalaire: 0, least-squares: 1, city-block: 2\n\nTapez q pour quitter.\n\n")

    text = text.split()

    print(text[0], text[1], text[2])

    if text[0] == "q":
        sys.exit()

    syn_filter = sf.Synonymes_Filter(text[0], int(text[1]), int(text[2]), trainer.cooc_matrix, trainer.word_indices)
    syn_filter.get_score()

    syn_filter.get_top_words()

    print("\n")
    for word in syn_filter.top_results:
        print(word)


if __name__ == '__main__':
    quit(main())