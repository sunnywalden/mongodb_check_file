#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import os,sys
sys.path.append('/opt/check_onoff_mongo_xmlfile')
from check_mongo.search_mongo import SearchidofMongo
from check_xml.search_xml_muti_thread import SearchidofXml
from check_xml_for_offline.tv_offline_data import OfflineTv
from check_xml_for_offline.base_offline_data import OfflineBase
from check_general_onoff import socket_searchid_file_sender
import time
import json
import codecs

#sys.path.append('/opt/check_onoff_mongo_xmlfile')

def get_conf():
	##从配置文件获取配置
        cp = ConfigParser.SafeConfigParser()
        with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:
                cp.readfp(f)
                mongo_searchids_file = cp.get('files','mongo_searchids_file').strip()
                xml_searchids_file = cp.get('files','xml_searchids_file').strip()
                offline_searchids_file = cp.get('files','offline_searchids_file').strip()
                online_searchids_file = cp.get('files','online_searchids_file').strip()
	return mongo_searchids_file,xml_searchids_file,offline_searchids_file,online_searchids_file

def get_searchid():
	#mongo_searchIds = search_mongo()
	#xml_searchIds = search_xml()
	mongo_searchids_file,xml_searchids_file,offline_searchids_file,online_searchids_file = get_conf()
	##从缓存文件获取查询MongoDB得到的searchid列表
	with open(mongo_searchids_file, 'r') as f1:
		#mongo_searchIds = eval(json.load(f1))
		mongo_searchIds = json.load(f1)
		print('type of mongo_searchIds',type(mongo_searchIds))
	##从缓存文件获取查询xml文件路径得到的searchid列表
	with open(xml_searchids_file + 'muti_version', 'r') as f2:
		#xml_searchIds = eval(json.load(f2))
		xml_searchIds = json.load(f2)
		print('type of xml_searchIds',type(xml_searchIds))
	return mongo_searchIds,xml_searchIds,offline_searchids_file,online_searchids_file

def get_diff():
	mongo_searchIds,xml_searchIds,offline_searchids_file,online_searchids_file = get_searchid()
	##mongodb中存在，但xml文件不存在的searchid，需要做下线处理

	m_searchids = set(mongo_searchIds)
	x_searchids = set(xml_searchIds)
	offline_searchids = list(m_searchids.difference(x_searchids))
	online_searchids = list(x_searchids.difference(m_searchids))
	print('type of m_searchids and x_searchids',type(m_searchids),type(x_searchids))
	#for searchid in offline_searchids:
	with open(offline_searchids_file,'w+') as f1:
		for searchid in offline_searchids:
			f1.write(searchid + '\n')
		f1.close()
	#for searchid in online_searchids:
	with open(online_searchids_file,'w+') as f2:
		for searchid in online_searchids:
			f2.write(searchid + '\n')
		f2.close()

if __name__=='__main__':
	start_time = time.strftime('%Y-%m-%d %H%M%S',time.localtime(time.time()))
	print('We start here',start_time)
	#查询MongoDB，获取所有已上线视频searchid
	mongo_searchid = SearchidofMongo()
	mongo_searchid.get_searchids()
	#扫描xml文件路径，获取所有咪咕方需要上线的searchid
	xml_searchid = SearchidofXml()
	xml_searchid.get_searchids()
	#比较二个来源的searchid，求差集得到需要上线、下线的searchid
	get_diff()
	##TV搜索ES视频库执行下线操作
	tv_offline = OfflineTv()
	tv_offline.offline()
	##基础视频搜索ES库执行下线操作
	base_offline = OfflineBase()
	base_offline.offline()
	##调用统一上下线手动下线脚本，通知进行队列下线
	socket_searchid_file_sender.socket_client(offline_searchids_file)
	socket_searchid_file_sender.socket_client(online_searchids_file)
	finish_time = time.strftime('%Y-%m-%d %H%M%S',time.localtime(time.time()))
	print('finished here',finish_time)
