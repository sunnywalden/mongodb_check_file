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
                mongo_ids_file = cp.get('files','mongo_ids_file').strip()
                xml_ids_file = cp.get('files','xml_ids_file').strip()
                offline_ids_file = cp.get('files','offline_ids_file').strip()
                online_ids_file = cp.get('files','online_ids_file').strip()
	return mongo_ids_file,xml_ids_file,offline_ids_file,online_ids_file

def get_id():
	#mongo_Ids = search_mongo()
	#xml_Ids = search_xml()
	mongo_ids_file,xml_ids_file,offline_ids_file,online_ids_file = get_conf()
	##从缓存文件获取查询MongoDB得到的id列表
	with open(mongo_ids_file, 'r') as f1:
		#mongo_Ids = eval(json.load(f1))
		mongo_Ids = json.load(f1)
		print('type of mongo_Ids',type(mongo_Ids))
	##从缓存文件获取查询xml文件路径得到的id列表
	with open(xml_ids_file + 'muti_version', 'r') as f2:
		#xml_Ids = eval(json.load(f2))
		xml_Ids = json.load(f2)
		print('type of xml_Ids',type(xml_Ids))
	return mongo_Ids,xml_Ids,offline_ids_file,online_ids_file

def get_diff():
	mongo_Ids,xml_Ids,offline_ids_file,online_ids_file = get_id()
	##mongodb中存在，但xml文件不存在的id，需要做处理

	m_ids = set(mongo_Ids)
	x_ids = set(xml_Ids)
	offline_ids = list(m_ids.difference(x_ids))
	online_ids = list(x_ids.difference(m_ids))
	print('type of m_ids and x_ids',type(m_ids),type(x_ids))
	#for id in offline_ids:
	with open(offline_ids_file,'w+') as f1:
		for id in offline_ids:
			f1.write(id + '\n')
		f1.close()
	#for id in online_ids:
	with open(online_ids_file,'w+') as f2:
		for id in online_ids:
			f2.write(id + '\n')
		f2.close()

if __name__=='__main__':
	start_time = time.strftime('%Y-%m-%d %H%M%S',time.localtime(time.time()))
	print('We start here',start_time)
	#查询MongoDB，获取所有已上线视频id
	mongo_id = SearchidofMongo()
	mongo_id.get_ids()
	#扫描xml文件路径，获取所有需要上线的id
	xml_id = SearchidofXml()
	xml_id.get_ids()
	#比较二个来源的id，求差集得到需要上线、下线的id
	get_diff()
	##ES视频库执行下线操作
	tv_offline = OfflineTv()
	tv_offline.offline()
	##ES库执行下线操作
	base_offline = OfflineBase()
	base_offline.offline()
	##调用统一上下线手动下线脚本，通知进行队列下线
	socket_searchid_file_sender.socket_client(offline_ids_file)
	socket_searchid_file_sender.socket_client(online_ids_file)
	finish_time = time.strftime('%Y-%m-%d %H%M%S',time.localtime(time.time()))
	print('finished here',finish_time)
