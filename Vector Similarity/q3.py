#!/usr/bin/env python
import distsim

word_to_ccdict = distsim.load_contexts("nytcounts.4k")


### provide your answer below
#answer = []
#answer.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['china'], set(['china']), distsim.cossim_sparse))
#answer.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['hand'], set(['hand']), distsim.cossim_sparse))
#answer.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['good'], set(['good']), distsim.cossim_sparse))
#answer.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['eat'], set(['eat']), distsim.cossim_sparse))

###Answer examples; replace with your choices
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['obama'],set(['obama']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'

for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['china'],set(['china']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'
    
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['car'],set(['car']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'

for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['great'],set(['great']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'
  
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['boy'],set(['boy']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'

for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['love'],set(['love']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
