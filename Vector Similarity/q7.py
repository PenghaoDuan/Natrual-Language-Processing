# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 14:22:15 2018

@author: Administrator
"""
import distsim
from collections import defaultdict

word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
start = 0
count = 0
scores = defaultdict(float)
pre = ""
num = 0

for line in open('word-test.v3.txt'):
    words = line.strip().split(' ')
    
    if line[0] == ':' and start == 1:
        print pre.strip('\n') + ":" + str(round(scores['1_best']/count, 2)) + " " + str(round(scores['5_best']/count, 2)) + " " + str(round(scores['10_best']/count, 2))
        scores.clear()
        count = 0
        
    if len(words) == 4:
        start = 1
        count += 1
        d1 = word_to_vec_dict[words[0].strip('\t')]
        d2 = word_to_vec_dict[words[1].strip('\t')]
        d3 = word_to_vec_dict[words[3].strip('\t')]
        
        result = distsim.show_nearest(word_to_vec_dict, d1 - d2 + d3, set([words[0], words[1], words[3]]), distsim.cossim_dense)
        
        keys = [item[0] for item in result]
        
        if words[2] in keys:
            index = keys.index(words[2])
        else:
            index = -1
            #Printing the potential correct words
            print line.strip('\n') + "\tanswer:" + keys[0]
        
        if index == 0:
            scores['1_best'] += 1
            scores['5_best'] += 1
            scores['10_best'] += 1
            
        elif index <= 4 and index != -1:
            scores['5_best'] += 1
            scores['10_best'] += 1
            
        elif index <= 9 and index != -1:
            scores['10_best'] += 1
            
    elif line[0] == ":":
        pre = line.split(" ")[1]

print pre.strip('\n') + ":" + str(round(scores['1_best']/count, 2)) + " " + str(round(scores['5_best']/count, 2)) + " " + str(round(scores['10_best']/count, 2))
            
        

        