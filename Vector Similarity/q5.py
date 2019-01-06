#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
###Provide your answer below

###Answer examples; replace with your choices
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['obama'],set(['obama']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'

for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['china'],set(['china']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'

for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['car'],set(['car']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'
    
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['great'],set(['great']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'

for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['boy'],set(['boy']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'
    
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['love'],set(['love']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print '\n'

