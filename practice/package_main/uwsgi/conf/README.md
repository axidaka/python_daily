# uwsgi 

通过配置文件启动 uwsgi --ini yourconfile
查看主进程pid uwsgi --reload pidfile
重启主进程 uwsgi --reload pidfile
通过状态文件查看 uwsgi --connect-and-read statsfile