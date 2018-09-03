一、简述

通过定时任务触发，查询mongoDB的migu_video，得到当前上下线状态的视频的searchid；

扫描xml文件，得到咪咕方需要上线的视频的searchid；

双向求差集，得到需要下线和上线的视频的searchid；

通过脚本，更新TV及基础视频的ES库，删除需要下线的视频;

通过socket将待上下线的searchid文件发送到统一上下线服务所在主机

auto_start.sh脚本定时执行，检测到文件，则调用手动上下线脚本，通知MQ对对应视频进行上下线
