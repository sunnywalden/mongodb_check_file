#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
from pymongo import MongoClient
from pymongo import ReadPreference
import ConfigParser
import codecs
import sys
import json

sys.path.append("/opt/check_onoff_mongo_xmlfile")

class SearchidofMongo:
    def __init__(self):
	
	cp = ConfigParser.SafeConfigParser()
	with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:
    		cp.readfp(f)
		self.hosts = cp.get('mongo','hosts').strip().encode('UTF-8')
		self.database = cp.get('mongo','database').strip().encode('UTF-8')
		self.collection = cp.get('mongo','collection').strip().encode('UTF-8')
		self.query_type = cp.get('mongo','query_type').strip().encode('UTF-8')
		self.query = cp.get('mongo','query').strip().encode('UTF-8')
		self.returns = cp.get('mongo','returns').strip().encode('UTF-8')
		self.options = cp.get('mongo','options').strip().encode('UTF-8')
		self.mongo_searchids_file = cp.get('files','mongo_searchids_file').strip().encode('UTF-8')


    def get_corsor(self):
	host = eval(self.hosts)
	client = MongoClient(host)
	query_line = eval(self.query)
	returns_line = eval(self.returns)
	options_line = self.options
	db=client.get_database(self.database,read_preference=ReadPreference.SECONDARY_PREFERRED)
	dblist = client.database_names()
	##连接MongoDB
	if self.database in dblist:
		print(self.database,"database exists in",dblist)
		collist = db.collection_names()
		if self.collection in collist:
			print(self.collection,"collection exists in",collist)
			col = db[self.collection]
			print('Connection to mongodb',self.hosts,self.database,self.collection,'success!')
		else:
			print(self.collection,"collection not exists in",collist)
	else:
		print(self.database,"database not exists in",dblist)
	##连接成功后，确认查询类别，支持aggregate,distinct及find查询
	if self.query_type == "aggregate":
		cursor = col.aggregate(pipeline=eval(query),allowDiskUse=True)
	elif self.query_type == "distinct":
		cursor = col.distinct(query,options)
	else:
		print('Start query now')
		#cursor = col.find(query_line,returns_line,options_line)
		cursor = col.find({},{'searchId': 1, '_id': 0},no_cursor_timeout=True)
	return cursor

    def get_searchids(self):
	cursor = self.get_corsor()
	searchIds = []
        
	for searchid in cursor:
            		searchIds.append(searchid["searchId"])
	cursor.close()
	print('connect to mongo closed now!')
	##查询结果写入json文件
	with open(self.mongo_searchids_file,'w') as f:
		json.dump(searchIds, f)
	return searchIds

    if __name__ == '__main__':
	get_searchids()
