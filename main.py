import Synonymes_Filter as sf
import Synonymes_Training as st



def main():
    chemin = "Tisane.txt"
    enc = "utf-8"

    trainer = st.Synonymes_Training(chemin, enc)
    trainer.read()
    trainer.create_cooccurrence_matrix(5)
    print(trainer.cooc_matrix)

    syn_filter = sf.Synonymes_Filter("tisane", 5, 1, trainer.word_indices)
    syn_filter.scalar_product(trainer.cooc_matrix)
    print(syn_filter.score)
    syn_filter.get_top_words()

    return 0

if __name__ == '__main__':
    quit(main())