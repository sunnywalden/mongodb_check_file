#!/usr/bin/python
# -*- coding: utf-8 -*-
##本脚本用于统计给定id的标签

import ConfigParser

import sys
import codecs

import re
import types

sys.path.append('/opt/check_onoff_mongo_xmlfile')


import check_vedio_status
import os
import glob

def get_config():
    cp = ConfigParser.SafeConfigParser()

    with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:  
        cp.readfp(f)
            
        work_dir = cp.get('id_files','wk_dir').strip()
        ids = work_dir + cp.get('id_files','ids').strip()
        res_file = work_dir + cp.get('id_files','res_file').strip()
    print(ids,res_file)
    return ids,res_file

def id_generater(ids):
    print(ids)

    dates = ['2018-07-18', '2018-07-19']
    ids = []
    with open(ids,'r') as f:
	while True:
        	line = f.readline().strip()
		if not line:
			break
        	print('deal with line',line) 

		record = {}
        	if line:
            		date = line.split('|')[2].split()[0].strip()
            		id = line.split('|')[4].strip('\n').strip()
	    
            		if date not in dates:
				print('debug id:',id)
                		ids.append(id)
            		else:
                		pass
		else:
			pass
    

    print(ids)
    return ids


def main():
    ids,res_file = get_config()
    print('Debug id file before deal with it:', ids)
    Ids = id_generater(ids)

    check_vedio_status.check_status(Ids,res_file)
        

if __name__  == '__main__':
    main()
