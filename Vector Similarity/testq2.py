#!/usr/bin/env python
import distsim
#Sparse
print 'sparse'
word_to_ccdict = distsim.load_contexts("nytcounts.university_cat_dog")
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['dog'], set(['dog']), distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))


#print distsim.show_nearest(word_to_ccdict, word_to_ccdict['dog'], set(['dog']), distsim.cossim_sparse)
print '\n'
##Dense
print 'dense'
word_to_ccarray = distsim.load_word2vec("nyt_word2vec.university_cat_dog")
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccarray, word_to_ccarray['dog'], set(['dog']), distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))