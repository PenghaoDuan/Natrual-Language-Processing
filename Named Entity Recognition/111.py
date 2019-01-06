# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 20:50:43 2018

@author: Administrator
"""
import os
dict_files = {}

path = 'data/lexicon'
files = os.listdir(path)



def get_keys(d, values):
    return [k for k, v in d.items() if values in v] 

if __name__ == "__main__":
    for file in files:
        if not os.path.isdir(file):
            text = []
            f = open(path +"/"+file)
#            iter_f = iter(f)
#            string=""
            for line in f:
                text.append(line.strip('\n'))
            dict_files[file] = set(text)
    print get_keys(dict_files, 'Television')

if 'Television' in dict_files['award.award']:
    print 'yes'