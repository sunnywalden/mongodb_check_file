#!/usr/bin/python
#-- coding:utf-8 --

import os
from pymongo import MongoClient
import ConfigParser
import codecs
import sys,subprocess,os
import re
import json

sys.path.append("/opt/check_onoff_mongo_xmlfile")

class SearchidofXml:
    def __init__(self):
	cp = ConfigParser.SafeConfigParser()
	with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:
    		cp.readfp(f)
		self.dir = cp.get('xml','dir').strip()
		self.xml_searchids_file = cp.get('files','xml_searchids_file').strip()

    def get_searchids(self):
	##定义存放xml文件所在一、二级路径的正则表达式	
	pattern = re.compile(r'\d{3}\n')
	file_pattern = re.compile(r'\d+.xml')
	##获取xml存放路径下的所有子路径	
	xml_first_dirs_str = subprocess.check_output(['ls',self.dir])
	##获取符合正则表达式的路径列表	
	xml_first_dirs = pattern.findall(xml_first_dirs_str)

	searchids = []

	for first_dir in xml_first_dirs:
		##逐个处理xml路径下符合要求的一级路径
		f_dir = first_dir.strip('\n')
		if f_dir != '000':
			f_pwd = self.dir + '/' + f_dir + '/'
			try:
                            xml_sec_dirs_str = subprocess.check_output(['ls',f_pwd])
                        except:
                            pass
                        else:
			    xml_sec_dirs = pattern.findall(xml_sec_dirs_str)
			    for sec_dir in xml_sec_dirs:
				##逐个处理xml路径下符合要求的二级路径
				s_dir = sec_dir.strip('\n')
				s_tmp = self.dir + '/' + f_dir + '/' + s_dir + '/'
				print('dealing with dir',s_tmp,'now')
                                try:
				    xml_files_str = subprocess.check_output(['ls',s_tmp])
                                except:
                                    pass
                                else:
				    xml_files = file_pattern.findall(xml_files_str)
				    for xml_file in xml_files:
					##逐个处理xml路径下二级路径中xml文件
					##得到xml文件名
					file_name = s_tmp + xml_file
					print('dealing with file',file_name,'now')
					xml_id = xml_file.strip('.xml')
					#if subprocess.check_output(['ls',file_name.encode('UTF-8')]):
					if os.path.isfile(file_name.encode('UTF-8')):
						##得到searchid
						searchid = f_dir + s_dir + xml_id
						print(file_name,searchid)
						searchids.append(searchid)
	##写入json文件
	with open(self.xml_searchids_file,'w') as f:
		json.dump(searchids, f)
	return searchids			  

    if __name__ == '__main__':
	get_searchids()
