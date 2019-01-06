# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import fst
import string

vowels=['a','e','i','o','u']

f=fst.FST('devowelizer')

f.add_state('1')

f.initial_state='1'

f.set_final('1')

for letter in string.ascii_lowercase:
    if letter in vowels:
        _=f.add_arc('1','1',(letter),())
        print _
    else:
        _=f.add_arc('1','1',(letter),(letter))
        print _
        
print ''.join(f.transduce(['v','o','w','e','l']))
print ''.join(f.transduce('e x c e p t i o n a l'.split()))
print ''.join(f.transduce('c o n s o n a t'.split())) 

