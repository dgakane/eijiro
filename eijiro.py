#!/usr/bin/env python3

eijiro_text_path = "~/Dropbox/eijiro/EIJI-144.TXT"

import string
import codecs
import json
import os.path
eijiro_text_path = os.path.expanduser(eijiro_text_path)
import argparse
import re
import logging
#logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def re_esc(s):
    metachars = '.^$*+?{}[]\|()'
    dict = {c: '\\'+c for c in metachars}
    map = str.maketrans(dict)
    return s.translate(map)

class Eijiro:
    def __init__(self):
        self.eijiro_text = eijiro_text_path
        self.index_file = os.path.join(
                            os.path.dirname(eijiro_text_path),
                            "index_" + os.path.basename(eijiro_text_path) + ".json")
        if(os.path.isfile(self.eijiro_text)):
            if (not os.path.isfile(self.index_file)):        
                ans = input("Index file doesn't exist. Do you want to create it? (Y/n): ")
                if (ans.lower() == 'n'):
                    print("This script requires index file.")
                else:
                    self.create_index_file()
        else:
            print( self.eijiro_text + " doesn't exist in the directory.")

    def create_index_file(self):
        index = {key: {"line": 0, "pos": 0} for key in string.ascii_uppercase}
        index["former_symbol"] = {"line": 0, "pos": 0}
        with codecs.open(self.eijiro_text, 'r', encoding="shift-jis", errors="ignore") as f:
            i = 0
            pos = 0
            while True:
                l = f.readline()
                if not l: break
                if( not l[1].isalpha() and l[1] > "Z"):
                    logging.debug(l)
                    index["latter_symbol"] = {"line": i, "pos": pos}
                    break
                for char in string.ascii_uppercase:
                    if(index[char]["line"]): continue
                    if ( l[1] == char or l[1] == char.lower()):
                        logging.debug(char + ": " + l)
                        index[char]["line"] = i
                        index[char]["pos"] = pos
                i += 1
                pos = f.tell()
        with open(self.index_file, "w") as f:
            f.write(json.dumps(index, sort_keys=True, indent=4))

    def search(self, phrase, mode=None):

        if(mode == 'all'):
            postfix = ''
        elif(mode == 'more'):
            postfix= '\s'
        else:
            postfix = '\s+[{:]'

        with open(self.index_file, 'r') as f:
            index = json.loads(f.read())
        index_keys = ['former_symbol'] + [i for i in string.ascii_uppercase] + ['latter_symbol']
        # ['former_symbol', 'A', 'B', 'C', ... , 'Z', 'latter_symbol']
        first_char = phrase[0]
        if(first_char.isalpha() and first_char <= 'z'):
            hash = first_char.upper()
        else:
            if(first_char < 'A'):
                hash = 'former_symbol'
            else:
                hash = 'latter_symbol'
        delta_lines = 0
        if( hash != 'latter_symbol'):
            next_hash = index_keys[index_keys.index(hash) + 1]
            delta_lines = index[next_hash]['line'] -index[hash]['line']
            logging.debug(delta_lines)
        with codecs.open(self.eijiro_text, 'r', encoding="shift-jis", errors="ignore") as f:
            f.seek(index[hash]['pos'])
            cnt = 0
            phrase = re_esc(phrase)
            pattern = re.compile(chr(9632) + phrase + postfix, flags=re.IGNORECASE)
            for line in f:
                if (delta_lines > 0 and delta_lines < cnt): break
                m = pattern.match(line)
                if(m):
                    found = re.sub('｛.*?｝', '', line[1:])
                    print(found, end="")
                cnt += 1

def parse_args():
    parser = argparse.ArgumentParser(description='Search the given phrase from the Eijiro text file.')
    parser.add_argument('phrase', action='store', nargs='+', const=None, type=str, choices=None,
                        help="phrase that you want to know the definition.",
                        metavar=None)
    parser.add_argument('-f', '--force_index', action='store_true', 
                        help='re-create index file.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--more', action='store_true', 
                        help='show  more result that starts with the given phrase + white space.')
    group.add_argument('-a', '--all', action='store_true', 
                        help='show all result that starts with the given phrase.')

    return parser.parse_args()

if  __name__ == "__main__": 
    args = parse_args()
    logging.debug(args)
    eiji = Eijiro()
    if(args.force_index):
        eiji.create_index_file()

    if(args.all == True):
        mode = 'all'
    elif(args.more == True):
        mode = 'more'
    else:
        mode = None
    phrase = ' '.join(args.phrase)
    logging.debug(phrase)
    eiji.search(phrase, mode)
