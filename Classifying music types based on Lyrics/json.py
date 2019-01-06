# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 10:20:27 2018

@author: Administrator
"""

import csv
import json

def read_csv(file):
    csv_rows= []
    
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        new_title = []
        new_title.append(title[3])
        new_title.append(title[2])
        for row in reader:
            csv_rows.extend([{new_title[i]:row[new_title[i]] for i in range(len(new_title))}])
#        for row in reader:
#            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
        return csv_rows
 
# 写json文件
def write_json(data, json_file, format=None):
    with open(json_file, "w") as f:
        if format == "good":
            f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))
        else:
            f.write(json.dumps(data))

x = read_csv('data_10000.csv')
write_json(read_csv('data_10000.csv'), 'data_sample.json', 'good')

#csv_rows= []
    
#with open('data_10000.csv') as csvfile:
#    reader = csv.DictReader(csvfile)
#    title = reader.fieldnames
#    new_title = []
#    new_title.append(title[3])
#    new_title.append(title[2])
#    for row in reader:
#        csv_rows.extend([{new_title[i]:row[new_title[i]] for i in range(len(new_title))}])
    