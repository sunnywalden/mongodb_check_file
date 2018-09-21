# -*- coding: utf-8 -*
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
import ConfigParser
import codecs

class OfflineBase(object):
    def __init__(self):
        self.ES_HOSTS = [
            'http://host1:9201',
            'http://host2:9201',
        ]
        self.es_conn = Elasticsearch(self.ES_HOSTS)
        self.demo_index = 'demo_v1'
        self.demo_type = 'logs'
        self.scroll = '5m'
        self.timeout = '1m'
        self.xml_root_path = '/mnt/test'
        self.output_path = '/data/demo/'
        self.file_name = 'id.txt'

#    def get_config(self):
        cp = ConfigParser.SafeConfigParser()
        with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:
                cp.readfp(f)
                self.offline_ids_file = cp.get('files','offline_ids_file').strip().encode('UTF-8')

    def get_result_list(self, es_result):
        final_result = []
        for item in es_result:
            final_result.append(item['_source']['Id'])
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
        for id in lists:
            xml_path = self.xml_root_path + '/' + id[0:3] + '/' + id[3:6] + '/' + id[6:9] + '.xml'
            if not os.path.exists(xml_path):
                result_list.append(search_id)
        self.write_file(result_list)
        print len(result_list)
        return result_list

    def offline(self):
        searchIds = []
        #with open('./id_offline.txt','r') as f:
        with open(self.ids_file, 'r') as f:
            for line in f:
                Id = line.strip()
                Ids.append(Id)
#        result_list = self.query_xml()
        for Id in Ids:
            print('offline id',Id,'in ES')
            qsl_body = {
                "query": {
                    "match": {
                        "Id": Id
                    }
                }
            }
            self.es_conn.delete_by_query(index=self.tv_index, doc_type=self.tv_type, body=qsl_body)


if __name__ == '__main__':
    offline = OfflineBase()
    #offline.query_xml()
    offline.offline()
