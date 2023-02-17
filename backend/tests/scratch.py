import numpy as np
import random
import os

def load_text(source_dir):
    entries = os.listdir(source_dir)
    entries.sort()
    content = []
    for entry in entries:
        with open(f'{source_dir}/{entry}') as f:
            content.append(''.join(f.readlines()))
    
    # print(np.mean([len(con) for con in content]))

    full_text = '\n\n'.join(content)
    
    return full_text, content

def build_lookup(source_text, k):
    lookup = dict()

    for i,s in enumerate(source_text):
        if i+k >= len(source_text):
            break
        x = source_text[i:i+k]
        y = source_text[i+k]
        
        if x not in lookup:
            lookup[x] = {y: 1}
        else:
            if y not in lookup[x]:
                lookup[x][y] = 1
            else:
                lookup[x][y] += 1
    
    return lookup

def generate_text(lookup, k, length, seed):
    assert len(seed) == k

    x = seed
    text = x
    for i in range(k, length):
        x = text[i-k:]

        chars = list(lookup[x].keys())
        weights = list(lookup[x].values())

        next_char = random.choices(chars, weights=weights, k=1)[0]
        text += next_char

    outfile = '/Users/basselsaleh/Documents/Brain/personal projects/AI_full_entry.md'
    with open(outfile, 'w') as f:
        f.write(text)

def main():
    journal_dir = '/Users/basselsaleh/Documents/Brain/journal/'
    full_text, entries = load_text(journal_dir)

    k = 10

    lookup = build_lookup(full_text, k=k)

    # this uses a random string of length k from the source as a seed
    # seed_idx = random.choice(np.arange(len(source_text)))
    # seed = source_text[seed_idx:seed_idx + k]

    # this uses a random start from an entry as a seed. hopefully this creates a result that resembles the structure of an entry
    seed = random.choice([entry[0:k] for entry in entries])

    generate_text(lookup, k=k, length=4500, seed=seed)


if __name__ == '__main__':
    main()