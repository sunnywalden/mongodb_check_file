#!/usr/bin/python
# -*- coding: utf-8 -*-
##本脚本用于统计给定searchid视频画像中的标签

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
            
        work_dir = cp.get('searchid_files','wk_dir').strip()
        ids = work_dir + cp.get('searchid_files','ids').strip()
        res_file = work_dir + cp.get('searchid_files','res_file').strip()
    print(ids,res_file)
    return ids,res_file

def searchid_generater(ids):
    print(ids)

    dates = ['2018-07-18', '2018-07-19']
    searchids = []
    with open(ids,'r') as f:
	while True:
        	line = f.readline().strip()
		if not line:
			break
        	print('deal with line',line) 

		record = {}
        	if line:
            		date = line.split('|')[2].split()[0].strip()
            		searchid = line.split('|')[4].strip('\n').strip()
	    
            		if date not in dates:
				print('debug searchid:',searchid)
                		searchids.append(searchid)
            		else:
                		pass
		else:
			pass
    

    print(searchids)
    return searchids


def main():
    ids,res_file = get_config()
    print('Debug searchid file before deal with it:', ids)
    searchIds = searchid_generater(ids)

    check_vedio_status.check_status(searchIds,res_file)
        

if __name__  == '__main__':
    main()
