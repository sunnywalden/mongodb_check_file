#!/bin/bash

##written by Henry 20180428

#sudo su 

#sleep 10s



#打印需要手动上线的视频id
echo '******************需要手动下线的视频id************************'
echo '需要手动下线的视频id个数'
#cat /tmp/do.txt${date_todo} >> /tmp/done.txt
wc -l new_offline_searchids_file.txt 

echo '**************************************************************'

#执行手动下线程序
#python xml_manual_offline_process_walden.py search_id.txt| /usr/local/kafka/bin/kafka-console-producer.sh --broker-list 10.200.26.15:9092 --topic program_onoff
python /data/xml_router/xml_router/xml_manual_offline_process_walden.py search_id.txt| /usr/local/kafka/bin/kafka-console-producer.sh --broker-list 10.200.26.15:9092 --topic program_onoff


#记录已处理视频id
#cat /tmp/do.txt${date_todo} >> /tmp/done.txt

#sleep 180s

#确认处理结果
grep failed /data/xml_router/xml_router/logs/xml_manual_offline_processor.txt.`date +%Y%m%d`|grep ERR

#删除文件
rm -rf new_offline_searchids_file.txt
