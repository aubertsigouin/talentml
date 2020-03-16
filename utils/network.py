# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:40:39 2020

@author: AubertSigouin-Lebel
"""
from collections import Counter
import itertools
import pandas as pd
import nltk
nltk.download('punkt')

def word_count(text, word_list):
    counts = Counter()

    uniques = set(nltk.word_tokenize(text))
    
    for word in word_list:
        if word in uniques:
            counts[word] += text.count(word)

    return(counts)

def co_occurences(list_of_dict, kind='links'):
    
    df = pd.DataFrame(index = range(len(list_of_dict)))

    links = []
    
    for obs in range(len(list_of_dict)):
        words = [k for k,v in list_of_dict[obs].items()]
        occurences = [v for k,v in list_of_dict[obs].items()]
        
        combinations = list(itertools.combinations(words, 2))
        
        for idx, word in enumerate(words) :
            df.loc[obs, word] = occurences[idx]
            
        for combo in combinations:
            links.append([df.columns.get_loc(combo[0]), df.columns.get_loc(combo[1])])
        
    df = df.fillna(0)
    
    returns = {
        'links' : links,
        'matrix' : df
        }
    
    return(returns[kind])