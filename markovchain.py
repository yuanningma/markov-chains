import sys
import time
import os
import re
import math
import random

chain_cache = {}
name_set = {}

def get_input():
    try:
        query = sys.argv[1:]
        if len(sys.argv) <= 1:
            raise IndexError
        return ' '.join(query)
    except IndexError:
        print("Please enter a file path or set of words")
        sys.exit()

def generate_name(type, number=None):
    chain = markov_chain(type)
    if (chain != None):
        # print("hello")
        if (number == None or number == 1):

            return markov_name(chain)
        else:
            toret = ""
            for i in range(0, number):
                toret += markov_name(chain) + '\n'
            return toret

    return ''

def markov_chain(type):
    if type in chain_cache:
        # print("in cache")
        return chain_cache[type]
    else:
        if type in name_set:
            # print("in name set")
            list = name_set[type]
            # print(list)
            chain = construct_chain(list)
            # print(chain)
            # print("reach here?")
            if chain != None:
                chain_cache[type] = chain
                # print(type)
                return chain
        return None

def construct_chain(list):
    # print(list)
    chain = {}
    for i in range(0, len(list)):
        # print(i)
        names = list[i].split("\s+")
        chain = incr_chain(chain, 'parts', len(names))
        # print("reach here?")

        for j in range(0, len(names)):
            # print(j)
            name = names[j]
            if len(name) == 0:
                names.remove(names[j])
                continue
            chain = incr_chain(chain, 'name_len', len(name))
            # print("reach here?")
            c = name[0]
            chain = incr_chain(chain, 'initial', c)
            # print("here?")
            string = name[1:]
            # print(len(string))

            last_c = c


            while (len(string) > 0):
                # print("hello")
                c = string[0]
                chain = incr_chain(chain, last_c, c)
                # print(string)
                string = string[1:]
                # print("last: " + last_c + " c: " + c)
                last_c = c
                # print(len(string))
    # print(chain)
    return scale_chain(chain)

def incr_chain(chain, key, token):
    if key in chain:
        if token in chain[key]:
            chain[key][token] += 1
        else:
            chain[key][token] = 1
    else:
        chain[key] = {}
        chain[key][token] = 1
    return chain

def scale_chain(chain):
    table_len = {}
    for key in chain:
        table_len[key] = 0
        for token in chain[key]:
            count = chain[key][token]
            weighted = math.floor(math.pow(count, 1.3))
            chain[key][token] = weighted
            table_len[key] += weighted
    chain['table_len'] = table_len
    return chain

def markov_name(chain):
    parts = select_link(chain, 'parts')
    # print(parts)
    names = []
    # print(chain)
    for i in range(0, parts):
        name_len = select_link(chain, 'name_len')
        c = select_link(chain, 'initial')
        name = c
        last_c = c
        while (len(name) < name_len):
            c = select_link(chain, last_c)
            name += c
            last_c = c
        names.append(name)
        # print('name is: ' + name)

    str = ""
    for s in names:
        str += s + "  "
    return str

def select_link(chain, key):
    len = chain['table_len'][key]
    idx = math.floor(random.random()*len)

    t = 0
    # print('new')
    # print(key)
    # print(chain[key])
    for token in chain[key]:
        t += chain[key][token]
        if (idx < t):
            return token
    return '-'


def generate():
    input = get_input()
    if "/" in input or ".txt" in input:
        # path
        with open(input) as f:
            text = f.read()
        # print(text)
        pattern = re.compile("^\s+|\s*,\s*|\s+$,'\\n'")
        # tokenized_text = [word[1:len(word)-1] for word in pattern.split(text) if word != '']
        # name_set['main'] = tokenized_text

        tokenized_text = [word for word in pattern.split(text) if word != '']
        # tok_txt = [word.strip() for word in text.split('\n, ^\s+')]
        tok_txt = [word.strip() for word in text.split()]

        print(len(tok_txt))
        name_set['main'] = tok_txt
        # print(tok_txt)
        #



        print('NAME IS: ' + generate_name("main", 5))



    else:
        print("under construction")

generate()
