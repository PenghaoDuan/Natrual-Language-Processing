#!/usr/bin/env python
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

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize



scriptdir = os.path.dirname(os.path.abspath(__file__))


reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


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



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
#Assuming the cmudict could be used in this program
        try:
            self._pronunciations = nltk.corpus.cmudict.dict()
        except LookupError:
            nltk.download('cmudict')
            self._pronunciations = nltk.corpus.cmudict.dict()
        
 
    def num_syllables(self, word):     
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        # TODO: provide an implementation!
        try:
            a=[len(list(y for y in x if y[-1].isdigit())) for x in self._pronunciations[word.lower()]]
            return min(a)
        except LookupError:
            return 1
        
        
    def isVowel(self,pronunciation):
#        count=0
        for i in range(len(pronunciation)):
            if pronunciation[i][-1].isdigit():
                return pronunciation[i:]
#            else:
#                count=count+1
#            return pronunciation[count:]

    def rhymes(self, a, b):
        
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        # TODO: provide an implementation!
        #        At first deciding whose sound length is longer, it may have more than one lengths 
#        and choose the shorter one
#        a_len=min([len(list(y for y in x)) for x in self._pronunciations[a]])
#        b_len=min([len(list(y for y in x)) for x in self._pronunciations[b]])
#       Travering all the pronunciations in word a and wor b
        for x in self._pronunciations[a]:
            for y in self._pronunciations[b]:
                Flag=True
                
                if len(x)==len(y):
                    if self.isVowel(x)==self.isVowel(y):
                        return True
                    else:
                        Flag=False
                        
                
                    
                if len(x)!=len(y):
                    c=min(len(self.isVowel(x)),len(self.isVowel(y)))
                    for i in range(c):
                        if x[-(i+1)]==y[-(i+1)]:
                            continue
                        else:
                            Flag=False
                            break
                    if Flag:
                        return True
                
                
        if Flag:
            return True
        else:
            return False

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        # TODO: provide an implementation!
       #        Processing the text for fetting list of words in every sentence
        r='[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
        after_text=re.sub(r,'',text)
        essay=after_text.strip().split('\n')
        tokenized_sents=[word_tokenize(i) for i in essay]
        
        for x in tokenized_sents:
            x[-1]=x[-1].lower()
        
        if len(tokenized_sents)!=5:
            return False
        else:
            line_Sylen=[]
            for x in tokenized_sents:
                word_Sylen=0
                for y in x:
                    word_Sylen=word_Sylen+self.num_syllables(y)
                line_Sylen.append(word_Sylen)
#       Determining whether there is a line has fewer than 4 syllables or not
            if min(line_Sylen)<4:
                return False
            else:
#                Determing  whether each  of B lines should have fewer syllables than  A lines 
                A_len=[]
                B_len=[]
                
                for x in range(len(line_Sylen)):
                    if x==0 or x==1 or x==4:
                        A_len.append(line_Sylen[x])
                    else:
                        B_len.append(line_Sylen[x])
                
                if min(A_len)<max(B_len):
                    return False
                else:
#                    Determining whether syllales differ by two or not
                    temp_B=B_len[0]
                    for y in B_len:
                        if abs(y-temp_B)>2:
                            return False
                        else:
                            temp_B=y

                    temp_A=A_len[-1]
                    for x in A_len:
                        if abs(x-temp_A)>2:
                            return False
                        else:
                            temp_A=x
                      
#                Then all the requiremnts have been met, classifying last word rhyme or not
                    A=[]
                    B=[]
                    for i in range(len(tokenized_sents)):
                        if i==0 or i==1 or i==4:
                            A.append(tokenized_sents[i][-1])
                        else:
                            B.append(tokenized_sents[i][-1])
                            
#                        A B do not rhyme with each other
                    for x in A:
                        for y in B:
                            if self.rhymes(x,y):
                                return False
#                   Finally, checking A lines/Blines rhyme?                   
                    if self.rhymes(B[0],B[1])==False:
                        return False
                    else:
                        count=0
                        for i in range(0,len(A)-1):
                            for j in range(i+1,len(A)):
                                if self.rhymes(A[i],A[j]):
                                    count=count+1
                        if count<2:
                            return False
        return True
    
        
        
       
    # TODO: if implementing guess_syllables add that function here by uncommenting the stub code and
    # completing the function. If you want guess_syllables to be used by num_syllables, feel free to integrate it appropriately.
    #
    def guess_syllables(self, word):
        word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables

        exception_add = ['serious','crucial']
        exception_del = ['fortunately','unfortunately']
    
        co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
        co_two = ['coapt','coed','coinci']
    
        pre_one = ['preach']
    
        syls = 0 #added syllable number
        disc = 0 #discarded syllable number
    
        #1) if letters < 3 : return 1
        if len(word) <= 3 :
            syls = 1
            return syls
    
        #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
        # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)
    
        if word[-2:] == "es" or word[-2:] == "ed" :
            doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]',word))
            if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
                if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
                    pass
                else :
                    disc+=1
    
        #3) discard trailing "e", except where ending is "le"  
    
        le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']
    
        if word[-1:] == "e" :
            if word[-2:] == "le" and word not in le_except :
                pass
    
            else :
                disc+=1
    
        #4) check if consecutive vowels exists, triplets or pairs, count them as one.
    
        doubleAndtripple = len(re.findall(r'[eaoui][eaoui]',word))
        tripple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
        disc+=doubleAndtripple + tripple
    
        #5) count remaining vowels in word.
        numVowels = len(re.findall(r'[eaoui]',word))
    
        #6) add one if starts with "mc"
        if word[:2] == "mc" :
            syls+=1
    
        #7) add one if ends with "y" but is not surrouned by vowel
        if word[-1:] == "y" and word[-2] not in "aeoui" :
            syls +=1
    
        #8) add one if "y" is surrounded by non-vowels and is not in the last word.
    
        for i,j in enumerate(word) :
            if j == "y" :
                if (i != 0) and (i != len(word)-1) :
                    if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
                        syls+=1
    
        #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.
    
        if word[:3] == "tri" and word[3] in "aeoui" :
            syls+=1
    
        if word[:2] == "bi" and word[2] in "aeoui" :
            syls+=1
    
        #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"
    
        if word[-3:] == "ian" : 
        #and (word[-4:] != "cian" or word[-4:] != "tian") :
            if word[-4:] == "cian" or word[-4:] == "tian" :
                pass
            else :
                syls+=1
    
        #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
    
        if word[:2] == "co" and word[2] in 'eaoui' :
    
            if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
                syls+=1
            elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
                pass
            else :
                syls+=1
    
        #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
    
        if word[:3] == "pre" and word[3] in 'eaoui' :
            if word[:6] in pre_one :
                pass
            else :
                syls+=1
    
        #13) check for "-n't" and cross match with dictionary to add syllable.
    
        negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]
    
        if word[-3:] == "n't" :
            if word in negative :
                syls+=1
            else :
                pass   
    
        #14) Handling the exceptional words.
    
        if word in exception_del :
            disc+=1
    
        if word in exception_add :
            syls+=1     
    
        # calculate the output
        return numVowels - disc + syls
    """
       Guesses the number of syllables in a word. Extra credit function.
       """
    #   # TODO: provide an implementation!
    #   pass

    # TODO: if composing your own limerick, put it here and uncomment this function. is_limerick(my_limerick()) should be True
    #
    #
    def my_limerick(self):
       """
       A limerick I wrote about computational linguistics
       """
       limerick="""
       Natural Language Processing in modern world is very good
the words translated by it would be easily understood
codes could be quickly programmed on the bed
it can even transform speaking voice to be read
the first man who ran it in the company is a schuld
       """
       return limerick


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))
  print(ld.rhymes("read", "need"))

if __name__ == '__main__':
  main()