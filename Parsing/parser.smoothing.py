# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:43:08 2018

@author: Administrator
"""

import sys, fileinput
from tree import Tree
import re
import math
import time

# Initializing the dict for storing rules and prob of training dataset
rules = {}
probs = {}
# Dict of storing rule from right(terminals) to left
terminals = {}

# Time for running CKY parser
time_spend = 0

# Reading the trees and finding rules of each node
def findrules(t):
    for node in t.bottomup():
        if node.children == []:
            continue
        count = 0
        children_rule = ''
        for children in node.children:
            count += 1
            if len(node.children) == 1:
                if children.label not in terminals:
                    terminals[children.label] = set()
                terminals[children.label].add(node.label)
            if count == 1:
                children_rule = children_rule + children.label
            else:
                children_rule = children_rule + ' ' + children.label
            
        if node.label not in rules:
            rules[node.label] = {}
        if children_rule in rules[node.label]:
            rules[node.label][children_rule] += 1
        else:
            rules[node.label][children_rule] = 1

def alpha_smoothing(a):
    terminals['<unk>'] = set()
    for rule in rules:
        terminals['<unk>'].add(rule)
        for children_rule in rules[rule]:
            children = children_rule.split()
            if len(children) == 1:
                rules[rule][children_rule] += a
        rules[rule]['<unk>'] = a

def rules_prob():
    for rule in rules:
        node_num = 0
        probs[rule] = {}
        for children_rule in rules[rule]:
            node_num += rules[rule][children_rule]
        
        for children_rule in rules[rule]:
            probs[rule][children_rule] = float(rules[rule][children_rule])/node_num           
        
def CKY_parser(each_line):
    start = time.time()
    words = each_line.split()
    
    # Creating the chart of CKY and at first all have been set to 0 
    backpointer = {}
    best_prob = {}
    
    for i in range(0, len(words) + 1):
        backpointer[i] = {}
        best_prob[i] = {}
        for j in range(0, len(words) + 1):
            backpointer[i][j] = {}
            best_prob[i][j] = {}
            for rule in rules:
                best_prob[i][j][rule] = 0
                backpointer[i][j][rule] = []
                
    # Checking the probability of each word (width = 1)
    for a in range(1, len(words) + 1):
        if words[a - 1] in terminals:
            one_word = words[a - 1]
        else:
            one_word = '<unk>'
        
        for node in terminals[one_word]:
            if probs[node][one_word] > best_prob[a - 1][a][node]:
                best_prob[a - 1][a][node] = probs[node][one_word]
                backpointer[a - 1][a][node].append(one_word)
        
    # Then filling other positions in the CKY chart
    for b in range(2, len(words) + 1):
        for c in range(0, len(words) + 1 - b):
            d = c + b
            for e in range(c + 1, d):
                for rule in rules:
                    for children_rule in rules[rule]:
                        children = children_rule.split()
                        
                        if len(children) == 1:
                            continue
                        else:
                            p = probs[rule][children_rule] * best_prob[c][e][children[0]] * best_prob[e][d][children[1]]
                            
                            if p > best_prob[c][d][rule]:
                                best_prob[c][d][rule] = p
                                backpointer[c][d][rule] = []
                                backpointer[c][d][rule].append(children[0])
                                backpointer[c][d][rule].append(children[1])
                                backpointer[c][d][rule].append(e)
                                
    end = time.time()
    time_spend = float(end - start)
    
    
    print 'time: ' + str(time_spend) + ' length: ' + str(len(words))
    
    if not backpointer[0][len(words)]['TOP']:
        sys.stdout.write('')
    else:
        tree_print('TOP', 0 , len(words), backpointer)
    
    if not best_prob[0][len(words)]['TOP']:
        return 'None'
    else:
        return str(math.log(best_prob[0][len(words)]['TOP'],10))

def tree_print(rule, i, j, backpointer):
    if len(backpointer[i][j][rule]) == 1:
         sys.stdout.write('(' + rule + ' ' + backpointer[i][j][rule][0] + ')')
    else:
        sys.stdout.write('(' + rule + ' ')
        tree_print(backpointer[i][j][rule][0], i, backpointer[i][j][rule][2], backpointer)
        sys.stdout.write(' ')
        tree_print(backpointer[i][j][rule][1], backpointer[i][j][rule][2], j, backpointer)
        sys.stdout.write(')')
    
if __name__ == '__main__':
    # Finding the rules from training dataset
    for line in open("train.trees.pre.unk"):
        t = Tree.from_str(line)
        findrules(t)
    
    # Getting the number of total rules
    total_rule = 0
    count = 0 
    for rule in rules:
        for children_rule in rules[rule]:
            total_rule += 1
            if rules[rule][children_rule] > count:
                count = rules[rule][children_rule]
                max_rule = children_rule
                max_parent = rule 
                
    alpha_smoothing(0.5)       
    rules_prob()
    
    
    out = open('dev.string.probs', 'w')
    for line in open('dev.strings'):
        cky = CKY_parser(line)
        out.write(line.strip('\n') + cky + '\n')
        print 
        
    out.close()  