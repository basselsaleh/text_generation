import os
import random

class MarkovModel:
    
    def __init__(self, k=1):
        '''
        Parameters:
        -----------------
        k   :   kernel size, i.e. how many characters to condition model prediction on
        '''
        self.k = k

    def load_text(self, source_dir):
        '''
        Load source text from source_dir. Default behavior here is that any files in source_dir
        will be read as text and joined together into one big string

        Parameters:
        -----------------
        source_dir  :   directory to read text from

        Returns:
        -----------------
        full_text   :   all the text from all the files in source_dir, joined into one string
        content     :   content of each file stored separately in a list
        '''
        entries = os.listdir(source_dir)
        entries.sort()
        content = []
        for entry in entries:
            with open(f'{source_dir}/{entry}', encoding='ISO-8859-1') as f:
                content.append(''.join(f.readlines()))

        self.full_text = '\n\n'.join(content)

        return self.full_text, content
    
    def build_lookup(self):
        '''
        Build the lookup table for frequency of character occurances. This is the distribution from which we will
        draw new characters when generating text.

        Returns:
        -----------------
        lookup      :   lookup table as nested dictionaries. e.g. lookup['e'] will be dictionary of all possible characters that follow
                        'e', where the values are the number of occurances of that character
        '''
        assert self.full_text is not None

        k = self.k
        source_text = self.full_text
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
        
        self.lookup = lookup
        return lookup
    
    def generate_text(self, seed, length, outfile=None):
        '''
        Generate new text, given a starting seed and desired length

        Parameters:
        -----------------
        seed    :   starting seed, a string of k characters that needs to appear somewhere in the source text
        length  :   desired length of generated text
        outfile :   if provided, generated text will be saved to this file. otherwise it will be printed to the console
        '''
        assert len(seed) == self.k
        assert seed in self.full_text
        assert self.lookup is not None

        k = self.k
        lookup = self.lookup
        x = seed
        text = x
        for i in range(k, length):
            x = text[i-k:]

            chars = list(lookup[x].keys())
            weights = list(lookup[x].values())

            next_char = random.choices(chars, weights=weights, k=1)[0]
            text += next_char

        if outfile is None:
            print(text)
        else:
            with open(outfile, 'w') as f:
                f.write(text)