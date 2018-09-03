# -*- coding: utf-8 -*
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
import ConfigParser
import codecs

class OfflineTv(object):
    def __init__(self):
        self.ES_HOSTS = [
            'http://10.150.20.113:9201',
            'http://10.150.20.114:9201',
            'http://10.150.20.115:9201',
            'http://10.150.20.116:9201',
            'http://10.150.20.117:9201',
            'http://10.150.20.118:9201',
        ]
        self.es_conn = Elasticsearch(self.ES_HOSTS)
        self.tv_index = 'tv_poms_index_v3'
        self.tv_type = 'tv_poms_data'
        self.scroll = '5m'
        self.timeout = '1m'
        self.xml_root_path = '/mnt/content'
        self.output_path = '/data/TV_offline/'
        self.file_name = 'search_id.txt'

#    def get_config(self):
        cp = ConfigParser.SafeConfigParser()
        with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:
                cp.readfp(f)
                self.offline_searchids_file = cp.get('files','offline_searchids_file').strip().encode('UTF-8')

    def get_result_list(self, es_result):
        final_result = []
        for item in es_result:
            final_result.append(item['_source']['searchId'])
        return final_result

    def write_file(self, final_result):
        with open(self.output_path + self.file_name, 'a') as f:
            for line in final_result:
                f.write(str(line) + '\n')

    def get_search_result(self):
        es_search_options = {
            "query": {
                "match_all": {}
            }
        }
        es_result = helpers.scan(
            client=self.es_conn,
            query=es_search_options,
            scroll=self.scroll,
            index=self.tv_index,
            doc_type=self.tv_type,
            timeout=self.timeout
        )
        final_result = self.get_result_list(es_result)
        return final_result

    def query_xml(self):
        result_list = []
        lists = self.get_search_result()
        for search_id in lists:
            xml_path = self.xml_root_path + '/' + search_id[0:3] + '/' + search_id[3:6] + '/' + search_id[6:9] + '.xml'
            if not os.path.exists(xml_path):
                result_list.append(search_id)
        self.write_file(result_list)
        print len(result_list)
        return result_list

    def offline(self):
        searchIds = []
        #with open('./searchid_offline.txt','r') as f:
        with open(self.offline_searchids_file,'r') as f:
            for line in f:
                searchId = line.strip()
                searchIds.append(searchId)
#        result_list = self.query_xml()
        for searchId in searchIds:
            print('offline searchid',searchId,'in ES')
            qsl_body = {
                "query": {
                    "match": {
                        "searchId": searchId
                    }
                }
            }
            self.es_conn.delete_by_query(index=self.tv_index, doc_type=self.tv_type, body=qsl_body)


if __name__ == '__main__':
    offline = OfflineTv()
    #offline.query_xml()
    offline.offline()
