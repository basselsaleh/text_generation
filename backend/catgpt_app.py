from flask import Flask, request
from flask_cors import CORS

import re
import string
import random
import nltk
from nltk.corpus import stopwords

from cmd_line_app import load_wiki, build_lookup, generate_text

app = Flask(__name__)
CORS(app)

source_text = None
stops = None
k = None
lookup = None

def initialize_app():
    print('Initializing app')
    global source_text
    global stops
    global k
    global lookup

    # load text from all the Wikipedia pages on cats
    source_text = load_wiki('Category:Cats')

    # use nltk to download the set of stopwords
    nltk.download('stopwords')
    stops = set(stopwords.words('english'))

    # set kernel size. I'm a fan of k = 10
    k = 10

    # build probability distribution as lookup table
    lookup = build_lookup(source_text, k)

@app.route('/generate-response', methods=['POST'])
def app_response():
    global source_text
    global stops
    global k
    global lookup

    input_text = request.data.decode('utf-8')

    # get a list of the user's words, ignoring punctuation, then filter out the stopwords
    words = re.findall(r"[\w']+|[.,!?;]", input_text.lower().translate(str.maketrans('','',string.punctuation)))
    keywords = list(filter(lambda w: not w in stops, words))

    # for each keyword, find matches in the text and pad them to be of length k
    # add them to a list of potential seeds
    seeds = []
    for w in keywords:
        for match in re.finditer(' ' + w, source_text):
            s = match.start() + 1
            e = match.end()
            padded = source_text[s:e]

            if len(padded) > k:
                seeds.append(padded[:k])
            while len(padded) < k:
                e += 1
                padded = source_text[s:e]
            
            seeds.append(padded)
    
    # if for some reason no match was found, set the seed as start of text
    if not seeds:
        seed = source_text[0:k]
    else:
        seed = random.choice(seeds)

    print(seed)

    # generate a response of length 500 (or whatever you want)
    response = generate_text(lookup, k, length=500, seed=seed)

    # do some post-processing to make sure the response ends with a period and starts capitalized
    last_period = response.rfind('.')
    if last_period == -1:
        last_period = len(response)
        response += '.'
    response = response[0].upper() + response[1:last_period+1]

    return response

if __name__ == '__main__':
    initialize_app()
    app.run('localhost', 6969)