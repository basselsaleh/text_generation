import random
import wikipedia

def load_wiki(article_name):
    wiki = wikipedia.page(article_name)
    content = wiki.content

    return content.replace('\n', ' ').replace('=', '')

def build_lookup(source_text, k):
    lookup = dict()

    for i,_ in enumerate(source_text):
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

    x = seed; text = x
    for i in range(k, length):
        x = text[i-k:]

        chars = list(lookup[x].keys())
        weights = list(lookup[x].values())

        next_char = random.choices(chars, weights=weights, k=1)[0]
        text += next_char
    
    print(text)

def main():
    source_text = load_wiki('Cats')

    k = 10
    seed = source_text[0:k]

    lookup = build_lookup(source_text, k)
    generate_text(lookup, k, length=1000, seed=seed)

if __name__ == '__main__':
    main()