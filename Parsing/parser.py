#!/usr/bin/env python

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

def rules_prob():
    for rule in rules:
        node_num = 0
        probs[rule] = {}
        for children_rule in rules[rule]:
            node_num += rules[rule][children_rule]
        
        for children_rule in rules[rule]:
            probs[rule][children_rule] = float(rules[rule][children_rule])/node_num
spent = []    
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
    
    #The time spent in the CKY parser algorithm
    spent.append(math.log10(time_spend))
    
#    print 'time: ' + str(time_spend) + ' length: ' + str(len(words))
    print  str(math.log10(time_spend)) 
    
    if not backpointer[0][len(words)]['TOP']:
        sys.stdout.write('')
    else:
        path = []
#        tree_print('TOP', 0 , len(words), backpointer, path)
    
    if not best_prob[0][len(words)]['TOP']:
#        return 'None'
        return ' ' 
    else:
#        return str(math.log(best_prob[0][len(words)]['TOP'],10))
        return path


def tree_print(rule, i, j, backpointer,path):
    if len(backpointer[i][j][rule]) == 1:
         sys.stdout.write('(' + rule + ' ' + backpointer[i][j][rule][0] + ')')
         path.append('(' + rule + ' ' + backpointer[i][j][rule][0] + ')')
    else:
        sys.stdout.write('(' + rule + ' ')
        path.append('(' + rule + ' ')
        tree_print(backpointer[i][j][rule][0], i, backpointer[i][j][rule][2], backpointer,path)
        sys.stdout.write(' ')
        path.append(' ')
        tree_print(backpointer[i][j][rule][1], backpointer[i][j][rule][2], j, backpointer,path)
        sys.stdout.write(')')
        path.append(')')
    
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
            
    rules_prob()
    
    final_path = []
    
    out = open('dev.string.probs', 'w')
    for line in open('dev.strings'):
        cky = CKY_parser(line)
#        out.write(line.strip('\n') + cky + '\n')
        final_path.append(cky)
        print 
#        break
    out.close()  
    
    # Showing the answers for question_1     
#    print '\n'
#    print 'Rules in grammar are: ' + str(total_rule)
#    print 'Most frequent rule is: ' + max_parent + ' -> ' + max_rule
#    print 'Times it occured: ' + str(rules[max_parent][max_rule])
#    



######################  Original Version of answers ###########################

#Node_label = {}
#b = {}
#
#def findNode(a):  # For generating the grammar rule based on training data
#    if len(a.children) == 0:
#        return
#        
#    if len(a.children) == 1:       
#        if a.label in Node_label:
#           Node_label[a.label] += 1
#        else:
#           Node_label[a.label] = 1
#
#            
#        if a.label + str("->") + a.children[0].label in b:
#            b[a.label + str("->") + a.children[0].label] += 1
#        else:
#            b[a.label + str("->") + a.children[0].label] = 1
#        return 
#    
#    if len(a.children) == 2:
#        findNode(a.children[0]) 
#        findNode(a.children[1])
#        if a.label in Node_label:
#            Node_label[a.label] += 1
#        else:
#            Node_label[a.label] = 1
#            
#        if a.label + str("->") + a.children[0].label + " " + a.children[1].label in b:
#            b[a.label + str("->") + a.children[0].label + " " + a.children[1].label] += 1 
#        else:
#            b[a.label + str("->") + a.children[0].label + " " + a.children[1].label] = 1
#            
#        return
#
#
#if __name__ == "__main__":
#    fileinput.close()
#    x = open('train.trees.pre.unk','r')
#    y = x.read()
#    
#    for line in fileinput.input('train.trees.pre.unk'):
#        t = tree.Tree.from_str(line)
#        root = t.root
#        findNode(root)
#        
#    maxValue = 0
#    
#    for line in b:
#        if b[line] > maxValue:
#            maxValue = b[line]
#            maxKey = line
#            
#    for rule in b: 
#        node = rule.split('->')
#        b[rule] = float(b[rule])/float(Node_label[node[0]])
#        
##########################    Creating a parser   ##############################    
#    
#    input_text = open('dev.strings', 'r')
#    sentences = input_text.readlines()
#    rules_mine = b.keys()
#    rule_newform = []
#    new_sentences = []
#    
##    Transforming the rules chart into a new form
#    for i in range(len(rules)):
#        each_rule = rules[i]
#        each_rule_prob = b[each_rule]
#        each_rule = re.split(r"->|\s",each_rule)
#        each_rule.append(each_rule_prob)
#        rule_newform.append(each_rule)
#        
##   Preporcessing the input sentences and labeling each word
#    sentence_label = []
#    for each_sentence in sentences:
#        new_sentence = each_sentence.strip('\n')
#        each_sentence_split = new_sentence.split(" ")
#        
#        word_label = []
#        for i in range(len(each_sentence_split)):
#            for j in range(len(rule_newform)):
#                if each_sentence_split[i] in rule_newform[j]:
#                    word_label.append(rule_newform[j][0])
#        break
#    
#    


    
    
    
        
    
#        print(node[0])
#    print(Node_label['QP'])
#    print(Node_label)
    
    
    
        
    # Binarize, inserting 'X*' nodes.
#    t.binarize()

    # Remove unary nodes
#    t.remove_unit()
    # The tree is now strictly binary branching, so that the CFG is in Chomsky normal form.

    # Make sure that all the roots still have the same label.
#    assert t.root.label == 'TOP'
#    t= tree.Tree._scan_tree(line)
   
    
#    output_file.write("%s\n"%t)

#output_file.close()    
    
    
