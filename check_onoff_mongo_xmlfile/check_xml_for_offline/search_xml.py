#!/usr/bin/python
# -- coding:utf-8 --

import os
# from pymongo import MongoClient
# import ConfigParser
import codecs
import sys, subprocess, os
import re


# sys.path.append("/opt/check_onoff_mongo_xmlfile")

def segmented(iterable):
    def _seg(width):
        it = iterable
        while len(it) > width:
            yield it[:width]
            it = it[width:]
        yield it
    return _seg

def get_searchids():
    searchids = []
    for i in range(1,49):
        idlist_dir = '/opt/check_onoff_mongo_xmlfile/check_xml_for_offline/dataerror/'
        idlist_file = 'error' + str(i) + '.txt'
	print('check for file',idlist_file)
	id_file = idlist_dir + idlist_file
        check_idfile = os.path.exists(id_file)
        if check_idfile:
            with open(id_file) as file:
                for le in file:
                    deal_id = le.strip()
                    searchId = deal_id
                    print("The video check for mannual offline is:", searchId)
                    searchids.append(searchId)
        else:
            print('file', idlist_dir + idlist_file, 'not exists!')
    return searchids

def check_searchids():
    searchIds = get_searchids()
    for searchId in searchIds:
#       try:
#         searchId = searchId_generate.next()
         print('the searchid to check is',searchId)
         split_searchId = segmented(searchId)
         tmp_id = list(split_searchId(3))
         print(tmp_id)
         xml_file = "/mnt/content/" + '/'.join(tmp_id) + ".txt"
         print('check for xml file', xml_file)
    # print(xml_file)
         check_xml = os.path.exists(xml_file)
         if not check_xml:
             with open('./searchid_offline.txt', 'a') as f:
                 print('write searchid', searchId, 'to offline list file')
                 f.write(searchId + '\n')
#       except:
#         print('generate searchid error')
#         break

if __name__=='__main__':
    check_searchids()
