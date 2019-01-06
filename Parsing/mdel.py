# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 11:55:29 2018

@author: Administrator
"""

from collections import defaultdict
from nltk import Tree
import math
import time
import types
import argparse
import sys
import codecs

from rbranch import prepfile

if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

grammar_dict_log = defaultdict(list)
grammar_dict_nolog = defaultdict(list)

class Parser:
    # Find matching rules in grammar
    def match_rules(self, word):
        global grammar_dict_log
        matched_rules = []
        for key, value in grammar_dict_log.items():
            for list_of_rhs in value:
                if word == list_of_rhs[0]:
                    matched_rules.append([key, list_of_rhs[-1]])

        if len(word.split()) == 1 and not matched_rules:
            for key, value in grammar_dict_log.items():
                for list_of_rhs in value:
                    if '<unk>' == list_of_rhs[0]:
                        matched_rules.append([key, list_of_rhs[-1]])
        return matched_rules

    # Convert parse tree to string
    def tree_to_str(self, tree):
        length_of_tree = len(tree)
        for i in range(length_of_tree):
            if isinstance(tree[i], list):
                tree[i] = self.tree_to_str(tree[i])
        str_tree = "({})".format(' '.join(tree))
        return str_tree

    # Create parse tree
    def create_parse_tree(self, sentence_parse, table_parse, pointer, row, col, item):
        if pointer[row][col]:
            pointer_list = []
            row1 = pointer[row][col][item][0][0]
            col1 = pointer[row][col][item][0][1]
            item1 = pointer[row][col][item][0][2]
            pointer_list.append(self.create_parse_tree(sentence_parse, table_parse, pointer, row1, col1, item1))
            row2 = pointer[row][col][item][1][0]
            col2 = pointer[row][col][item][1][1]
            item2 = pointer[row][col][item][1][2]
            pointer_list.append(self.create_parse_tree(sentence_parse, table_parse, pointer, row2, col2, item2))
        else:
            pointer_list = [sentence_parse[col - 1]]
        tree_table = [table_parse[row][col][item][0]]
        tree_table.extend(pointer_list)
        return tree_table


    # CKY Parser
    def parse(self, sentence, start):
        start_time = start
        # print sentence
        # Create the CYK table
        length = len(sentence)
        table = [None] * length
        for j in range(length):
            table[j] = [None] * (length + 1)
            for i in range(length + 1):
                table[j][i] = []

        # Create a back pointer table
        pointer_table = [None] * length
        for j in range(length):
            pointer_table[j] = [None] * (length + 1)
            for i in range(length + 1):
                pointer_table[j][i] = []

        # Fill the diagonal of the CYK table with parts-of-speech of the words
        for k in range(1, length + 1):
            terminals_rules = self.match_rules(sentence[k-1])
            for terminal_rule in terminals_rules:
                lhs_diagonal = [(terminal_rule[0], terminal_rule[1])]
                table[k - 1][k].extend(lhs_diagonal)

        # Fill the CYK table
        for i in range(1, length + 1):
            for j in range(i - 2, -1, -1):
                for k in range(j + 1, i):
                    for l in range(len(table[j][k])):
                        for m in range(len(table[k][i])):

                            if time.time() - start_time > 70:
                                # print "timeout"
                                return None

                            prob = table[j][k][l][1] + table[k][i][m][1]
                            rhs = table[j][k][l][0] + ' ' + table[k][i][m][0]
                            lhs_temp = self.match_rules(rhs)

                            lhs = []
                            if len(lhs_temp) is not 0:
                                for temp in lhs_temp:
                                    lhs += [(temp[0], temp[1] + prob)]
                            else:
                                lhs = lhs_temp

                            if lhs:
                                rules_added = []
                                for rule in lhs:
                                    if rule not in table[j][i]:
                                        rules_added.append(rule)
                                        table[j][i].extend([rule])
                                if rules_added:
                                    pointer_table[j][i].extend([[[j, k, l], [k, i, m]]] * len(rules_added))

        # Call function to generate a parse tree
        if table[0][length]:
            last_cell = table[0][length]
            max_prob = last_cell[0][1]
            index_of_max_prob = 0

            for i in range(1, len(last_cell)):
                prob_x = last_cell[i][1]
                if prob_x > max_prob:
                    max_prob = prob_x
                    index_of_max_prob = i
            # print "Log Probability: " + str(max_prob)
            return self.create_parse_tree(sentence, table, pointer_table, 0, length, index_of_max_prob)
        else:
            return None



def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
    ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
    group = parser.add_mutually_exclusive_group()
    dest = arg if dest is None else dest
    group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
    group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)


def main():
    global grammar_dict_log
    parser = argparse.ArgumentParser(description="ignore input; make a demo grammar that is compliant in form",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    addonoffarg(parser, 'debug', help="debug mode", default=False)
    parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file (ignored)")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file (grammar)")

    try:
        args = parser.parse_args()
    except IOError as msg:
        parser.error(str(msg))

    workdir = tempfile.mkdtemp(prefix=os.path.basename(__file__), dir=os.getenv('TMPDIR', '/tmp'))

    def cleanwork():
        shutil.rmtree(workdir, ignore_errors=True)

    if args.debug:
        print(workdir)
    else:
        atexit.register(cleanwork)

    infile = prepfile(args.infile, 'r')
    outfile = prepfile(args.outfile, 'w')
    infile = args.infile
    outfile = args.outfile


    # Generate grammar
    f1 = open('train.trees.pre.unk', 'r')
    productions = []
    for line in f1:
        t = Tree.fromstring(line)
        productions += t.productions()

    # f2 = open('notes2.txt', 'w')
    productions_dict = defaultdict(list)
    for production in productions:
        rule = str(production).strip().split("->")
        rule_lhs = rule[0].strip()
        rule_rhs = rule[1].strip().replace("'", "")
        # rule_lhs = rule[0].lower().strip()
        # rule_rhs = rule[1].lower().strip().replace("'", "")
        if productions_dict[rule_lhs]:
            productions_dict[rule_lhs].append([rule_rhs])
        else:
            productions_dict[rule_lhs].append([rule_rhs])

    # for k, v in productions_dict.iteritems():
    #     f2.write(k + ": " + str(v) + "\n")

    #grammar_dict_log = defaultdict(list)
    #grammar_dict_nolog = defaultdict(list)
    # grammar_dict_log_lower = defaultdict(list)
    # grammar_dict_nolog_lower = defaultdict(list)
    for key, value in productions_dict.iteritems():
        rule_dict = defaultdict(int)
        length = len(value)
        for v in value:
            rule_dict[str(v)] += 1
        for k, v in rule_dict.iteritems():
            prob = (float(v) / float(length))
            grammar_dict_nolog[key].append([k[2:-2], prob])
            prob_log = math.log10(float(v) / float(length))
            # pr = bigfloat.log(bigfloat.exp10(float(probability)))
            # grammar_dict[lhs_rule].append([rhs_rule, pr])
            grammar_dict_log[key].append([k[2:-2], prob_log])
            # grammar_dict_nolog_lower[key].append([k[2:-2], prob])
            # grammar_dict_log_lower[key].append([k[2:-2], prob_log])
    # f2.write("\n\n")

    # Write to grammar.txt
    # f3 = open('grammar2.txt', 'w')
    count = 0
    for key, value in grammar_dict_nolog.iteritems():
        for v in value:
            count += 1
            # f3.write(str(key) + " -> " + str(v[0]) + " # " + str(v[1]) + "\n")

    # Call Viterbi Parser
    v_parser = Parser()
    # f4 = open('dev.parses', 'w')

    # sentence = "The flight should be eleven a.m tomorrow ."
    # sent_tree = v_parser.parse(sentence.split(), time.time())
    # print v_parser.tree_to_str(sent_tree)

    # with open('dev.strings') as fp:
    for line in infile:
        start = time.time()
        words = line.split()
        #print words
        # words = [word.lower() for word in line.split()]
        sentence_tree = v_parser.parse(words, time.time())

        if sentence_tree is None:
            """
            if words[0].startswith("What") or words[0].startswith("Where"):
                result_tree = "(TOP (SBARQ (WHNP ( " + words[0] + "))) (PUNC ?))"
            elif words[0].startswith("Are"):
                result_tree = "(TOP (SQ (VBP Are)) (PUNC ?))"
            elif words[0].startswith("Does"):
                result_tree = "(TOP (SQ ( Does)) (PUNC ?))"
            elif words[0].startswith("The"):
                result_tree = "(TOP (S (NP (DT The))) (PUNC .))"
            else:
                result_tree = "(TOP (FRAG (NP " + words[0] + ")) (PUNC .))"
            f4.write(str(result_tree)+"\n")
            """
            outfile.write("\n")
        else:
            result_tree = v_parser.tree_to_str(sentence_tree)
            outfile.write(result_tree + "\n")
            # print "Parse tree: " + str(result_tree) + "\n"


if __name__ == '__main__':
  main()
