import Synonymes_Filter as sf
import Synonymes_Training as st



def main(top_target, encodage, chemin):
    # chemin = "DonQuichotteUTF8.txt"
    # enc = "utf-8"
    # top_target = 5

    trainer = st.Synonymes_Training(chemin, encodage)
    trainer.read()
    trainer.create_cooccurrence_matrix(top_target)


    syn_filter = sf.Synonymes_Filter("tranquille", 5, 1, trainer.cooc_matrix, trainer.word_indices)
    syn_filter.get_score()
    print(syn_filter.get_top_words())

    return 0

if __name__ == '__main__':
    quit(main())