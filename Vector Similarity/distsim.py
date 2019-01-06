from __future__ import division
import sys,json,math
import os
import numpy as np

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict

def cossim_sparse(v1,v2):
    # Take two context-count dictionaries as input
    # and return the cosine similarity between the two vectors.
    # Should return a number beween 0 and 1

    ## TODO: delete this line and implement me
    sum_total = 0
    sum_x = 0
    sum_y = 0
    
    for i in v1:
        sum_total += v1[i] * v2.get(i, 0)
        sum_x += v1[i]**2
        
    for j in v2:
        sum_y += v2[j]**2
    
    return sum_total/(np.sqrt(sum_x)*np.sqrt(sum_y))

def cossim_dense(v1,v2):
    # v1 and v2 are numpy arrays
    # Compute the cosine simlarity between them.
    # Should return a number between -1 and 1
    
    ## TODO: delete this line and implement me
    return np.sum(v1*v2)/(np.sqrt(np.sum(v1**2)) * (np.sqrt(np.sum(v2**2))))


def show_nearest(word_2_vec, w_vec, exclude_w, sim_metric):
    #word_2_vec: a dictionary of word-context vectors. The vector could be a sparse (dictionary) or dense (numpy array).
    #w_vec: the context vector of a particular query word `w`. It could be a sparse vector (dictionary) or dense vector (numpy array).
    #exclude_w: the words you want to exclude in the responses. It is a set in python.
    #sim_metric: the similarity metric you want to use. It is a python function
    # which takes two word vectors as arguments.

    # return: an iterable (e.g. a list) of up to 10 tuples of the form (word, score) where the nth tuple indicates the nth most similar word to the input word and the similarity score of that word and the input word
    # if fewer than 10 words are available the function should return a shorter iterable
    #
    # example:
    #[(cat, 0.827517295965), (university, -0.190753135501)]
    

    
    ## TODO: delete this line and implement me
    sim = {}
    c = 0
    
    for x in word_2_vec:
        if x not in exclude_w:
            res = sim_metric(word_2_vec[x], w_vec)
            if c < 10:
                sim[x] = res
                c += 1
            else:
                minimum = min(sim, key = sim.get)
                
                if res > sim[minimum]:
                    sim[x] = res
                    del sim[minimum]
                    
    final = sorted(sim.items(), key = lambda x: x[1], reverse = True)                
    return final