# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 08:29:13 2018

@author: Administrator
"""

dic = {"name": 11, "case":12, "penghao":13}
print min(dic, key = dic.get)
print dic["name"]
a= (sorted(dic.items(), key = lambda x: x[1], reverse = True))

a= set(['dog'])
b= 'dog'
print b in a 