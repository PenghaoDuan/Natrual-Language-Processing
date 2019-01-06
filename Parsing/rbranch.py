#!/usr/bin/env python3
# right branching "parser"
# from  boilerplate code by Jon May (jonmay@isi.edu)
import argparse
import sys
import codecs
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
from tree import Tree

scriptdir = os.path.dirname(os.path.abspath(__file__))


reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

 # Initializing the dict for storing rules and prob of training dataset
rules = {}
probs = {}
  # Dict of storing rule from right(terminals) to left
terminals = {}


def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)

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

def alpha_smoothing(a):
    terminals['<unk>'] = set()
    for rule in rules:
        terminals['<unk>'].add(rule)
        for children_rule in rules[rule]:
            children = children_rule.split()
            if len(children) == 1:
                rules[rule][children_rule] += a
        rules[rule]['<unk>'] = a
        
def CKY_parser(each_line):
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
          one_word = words[a - 1].encode("utf-8")
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
                            
#      end = time.time()
#      time_spend = float(end - start)


#      print 'time: ' + str(time_spend) + ' length: ' + str(len(words))

  if not backpointer[0][len(words)]['TOP']:
      sys.stdout.write('')
  else:
      path = []
      tree_print('TOP', 0 , len(words), backpointer, path)

  if not best_prob[0][len(words)]['TOP']:
#        return 'None'
      return ' ' 
  else:
#        return str(math.log(best_prob[0][len(words)]['TOP'],10))
      return path


def tree_print(rule, i, j, backpointer,path):
  if len(backpointer[i][j][rule]) == 1:
#      sys.stdout.write('(' + rule + ' ' + backpointer[i][j][rule][0] + ')')
      path.append('(' + rule + ' ' + backpointer[i][j][rule][0] + ')')
  else:
#      sys.stdout.write('(' + rule + ' ')
      path.append('(' + rule + ' ')
      tree_print(backpointer[i][j][rule][0], i, backpointer[i][j][rule][2], backpointer,path)
#      sys.stdout.write(' ')
      path.append(' ')
      tree_print(backpointer[i][j][rule][1], backpointer[i][j][rule][2], j, backpointer,path)
#      sys.stdout.write(')')
      path.append(')')


def main():
  parser = argparse.ArgumentParser(description="trivial right-branching parser that ignores any grammar passed in",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input (one sentence per line strings) file")
  parser.add_argument("--grammarfile", "-g", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="grammar file; ignored")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output (one tree per line) file")
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
  grammarfile = prepfile(args.grammarfile, 'r')
  outfile = prepfile(args.outfile, 'w')

  for line in grammarfile:
      line = line.encode("utf-8")
      t = Tree.from_str(line)
      findrules(t)
  
  alpha_smoothing(0.5)    
  rules_prob()
 
  final_path = []
  
  for sentences in infile:
#      sentences = sentences.endcode("utf-8")
      final_path.append(CKY_parser(sentences))
  
  for line in final_path:
      line_str = ''
      line = line_str.join(line)
      outfile.write(line + '\n')
      print line 
      
      
  
  outfile.close()
  
if __name__ == '__main__':
  main()
