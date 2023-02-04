# primary driver for using text generation models

import random
from markov_model import MarkovModel

def main():
    # kernel size
    k = 10

    # directory of source text, in this case my personal journal
    #journal_dir = '/Users/basselsaleh/Documents/Brain/journal'
    journal_dir = 'journal_entries'

    # directory to output new text
    outdir = f'/Users/basselsaleh/Documents/Brain/personal projects/Text Generation/AI journaling/7-31-22/AI_entry_k{k}.md'

    model = MarkovModel(k=k)

    _, entries = model.load_text(journal_dir)
    model.build_lookup()

    # generate seed that is random start of a journal entry
    seed = random.choice([entry[0:k] for entry in entries])

    model.generate_text(seed=seed, length=4500, outfile=outdir)


if __name__ == '__main__':
    main()