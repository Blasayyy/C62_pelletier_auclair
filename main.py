import Synonymes_Filter as sf
import Synonymes_Training as st



def main():
    chemin = "DonQuichotteUTF8.txt"
    enc = "utf-8"

    trainer = st.Synonymes_Training(chemin, enc)
    trainer.read()
    trainer.create_cooccurrence_matrix(5)


    syn_filter = sf.Synonymes_Filter("sancho", 5, 1, trainer.word_indices)
    syn_filter.scalar_product(trainer.cooc_matrix)
    syn_filter.get_top_words()
    print("--------------------------")
    syn_filter.city_block(trainer.cooc_matrix)
    syn_filter.get_top_words()

    return 0

if __name__ == '__main__':
    quit(main())