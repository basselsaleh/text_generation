import random
import re
import string
import wikipediaapi
import nltk
from nltk.corpus import stopwords

def load_wiki(category):
    wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI)

    cat_page = wiki.page(category)
    article_names = [p for p in cat_page.categorymembers.keys() if ':' not in p]

    content = ''
    for article in article_names:
        page = wiki.page(article)
        page_content = page.text
        content += page_content

    return content.replace('\n', ' ')#.replace('=', '')

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

    text = seed
    for i in range(k, length):
        x = text[i-k:]

        chars = list(lookup[x].keys())
        weights = list(lookup[x].values())

        next_char = random.choices(chars, weights=weights, k=1)[0]
        text += next_char
    
    return text

def main():
    source_text = load_wiki('Category:Cats')
    nltk.download('stopwords')
    stops = set(stopwords.words('english'))

    k = 10
    seed = source_text[0:k]

    lookup = build_lookup(source_text, k)

    print('\nHello, my name is CatGPT. What can I help you with today?')
    
    while True:
        input_text = input('\n> ')
        if input_text.lower() == 'goodbye':
            break

        words = re.findall(r"[\w']+|[.,!?;]", input_text.lower().translate(str.maketrans('','',string.punctuation)))
        keywords = list(filter(lambda w: not w in stops, words))

        seeds = []
        for w in keywords:
            for match in re.finditer(' ' + w, source_text):
                s = match.start() + 1
                e = match.end()
                padded = source_text[s:e]
                # TODO: check if word is already longer than k, then do something else
                while len(padded) < k:
                    e += 1
                    padded = source_text[s:e]
                
                seeds.append(padded)
        
        # if for some reason no match was found, set the seed as start of text
        if not seeds:
            seed = source_text[0:k]
        else:
            seed = random.choice(seeds)

        response = generate_text(lookup, k, length=500, seed=seed)
        last_period = response.rfind('.')
        if last_period == -1:
            last_period = len(response)
            response += '.'
        response = response[0].upper() + response[1:last_period+1]

        print('\n' + response)

def main2():
    import json

    #source_text = 'The cat (Felis catus)'# is a domestic species of small carnivorous mammal.'# It is the only domesticated species in the family Felidae and is commonly referred to as the domestic cat or house cat to distinguish it from the wild members of the family. Cats are commonly kept as house pets but can also be farm cats or feral cats; the feral cat ranges freely and avoids human contact. Domestic cats are valued by humans for companionship and their ability to kill rodents. About 60 cat breeds are recognized by various cat registries.'
    source_text = 'hello there'

    k = 2

    lookup = build_lookup(source_text, k)

    print(json.dumps(lookup, indent=4))

    # seed = source_text[:k]
    # new_text = generate_text(lookup, k=k, length=100, seed=seed)

    # print(new_text)

if __name__ == '__main__':
    main()