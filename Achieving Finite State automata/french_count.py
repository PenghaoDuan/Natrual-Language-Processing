# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 23:07:46 2018

@author: Administrator
"""

import sys
from fst import FST
from fsmutils import composewords
import pandas as pd

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.initial_state = 'start'
    
    f.add_state('c')
    f.add_state('b')
    f.add_state('a')
    
    #Classifying the hundred digits
    for x in range(1,10):
        f.add_state('d-'+str(x))

        if x==1:
            f.add_arc('start','d-'+str(x), str(x), ['cent'])
            f.add_arc('d-'+str(x),'c','','')
        else:
            f.add_arc('start','d-'+str(x), str(x), [kFRENCH_TRANS[x]+' cent'])
            f.add_arc('d-'+str(x),'c','','')
            
        f.add_state('d-'+str(x)+'_end_1')
        f.add_state('d-'+str(x)+'_end_2')
        f.set_final('d-'+str(x)+'_end_2')
        
        f.add_arc('d-'+str(x),'d-'+str(x)+'_end_1','0','')
        if x==1:
            f.add_arc('d-'+str(x)+'_end_1','d-'+str(x)+'_end_2','0','')
        else:
            f.add_arc('d-'+str(x)+'_end_1','d-'+str(x)+'_end_2','0','')
        
    
    #Translating the single digit
    f.add_arc('start','c','0','')
    f.add_arc('c','b','0','')
    f.set_final('a') 
    for ii in xrange(10):
        f.add_arc('b', 'a', [str(ii)], [kFRENCH_TRANS[ii]])
    
    #Translating the digits from 10~16
    f.add_state('c_1')
    f.add_state('c_1_end')
    f.set_final('c_1_end')
    f.add_arc('c','c_1','1','')
    for ii in xrange(7):
        f.add_arc('c_1', 'c_1_end', [str(ii)], [kFRENCH_TRANS[10+ii]])
        
    #Translating the digits from 17~19
    f.add_state('c_1_end_1')
    f.set_final('c_1_end_1')
    for ii in range(7,10):
        f.add_arc('c_1', 'c_1_end_1', [str(ii)], ['dix '+kFRENCH_TRANS[ii]])
    
    #Translating the digits from 20~59
    for i in range(2,7):
        f.add_state('c-'+str(i))
        f.add_state('c-'+str(i)+'_end')
        f.set_final('c-'+str(i)+'_end')
        f.add_arc('c','c-'+str(i), str(i), '')
        for ii in range(0,10):
            if ii==0:
                f.add_arc('c-'+str(i), 'c-'+str(i)+'_end', [str(ii)], [kFRENCH_TRANS[10*i]])
            elif ii==1:
                f.add_arc('c-'+str(i), 'c-'+str(i)+'_end', [str(ii)],[kFRENCH_TRANS[10*i]+' et ' + kFRENCH_TRANS[ii]])
            elif ii in range(2,10):
                f.add_arc('c-'+str(i), 'c-'+str(i)+'_end', [str(ii)], [kFRENCH_TRANS[10*i]+' '+kFRENCH_TRANS[ii]])
       
    #Translating the digits from 70 to 79
    f.add_state('c_7')
    f.add_state('c_7_end')
    f.set_final('c_7_end')
    f.add_arc('c','c_7','7','')
    
    for ii in range(0,7):
        if ii==1:
            f.add_arc('c_7', 'c_7_end', [str(ii)], [kFRENCH_TRANS[60]+' et '+kFRENCH_TRANS[10+ii]])
        else:
            f.add_arc('c_7', 'c_7_end', [str(ii)], [kFRENCH_TRANS[60]+' '+kFRENCH_TRANS[10+ii]])  
    
    for ii in range(7,10):
        f.add_arc('c_7', 'c_7_end', [str(ii)], [kFRENCH_TRANS[60]+' dix '+kFRENCH_TRANS[ii]])
    
    #Translating the digits from 80 to 89
    f.add_state('c_8')
    f.add_state('c_8_end')
    f.set_final('c_8_end')
    f.add_arc('c', 'c_8' ,'8', '')
    
    for ii in range(0,10):
        if ii==0:   
            f.add_arc('c_8', 'c_8_end', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]+'s'])
        else:
            f.add_arc('c_8', 'c_8_end', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]+' '+kFRENCH_TRANS[ii]])
    
    #Translating the digits from 90~99
    f.add_state('c_9')
    f.add_state('c_9_end')
    f.set_final('c_9_end')
    f.add_arc('c', 'c_9', '9', '')
    
    for ii in range(0,7):
        f.add_arc('c_9', 'c_9_end', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]+' '+kFRENCH_TRANS[10+ii]])
    for ii in range(7,10):
        f.add_arc('c_9', 'c_9_end', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]+' dix '+kFRENCH_TRANS[ii]])
    
    return f
    

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
#    user_input=0
    
    f = french_count()
    if string_input:
        print user_input, '-->',
        y=" ".join(f.transduce(prepare_input(user_input)))
        print y
    
    a=[]
    for i in range(0,1000):
        print i, '-->',
        y=" ".join(f.transduce(prepare_input(i)))
        a.append(y)
        print y
    df=pd.DataFrame(a,columns=["Result"])
    df.to_csv('translation.csv',index=False)