#!/bin/bash

offline_file_name='new_offline_searchids_file.txt'
online_file_name='new_online_searchids_file.txt'
check_cmd=`ls ${offline_file_name}`
check_cmd1=`ls ${online_file_name}`

if [ ${check_cmd} ];
then
    bash manual_offline_process_V1.0.sh
fi
if [ ${check_cmd1} ];
then
    bash manual_online_process_V1.2.sh
fi
