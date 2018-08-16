#!/bin/sh

# Please modify the ServiceName, and WEB_CONTAINER_HOME if it's necessary

ulimit -c unlimited


ServiceName="unknown_tws"

if [ -z $WEB_CONTAINER_HOME ]
then
	WEB_CONTAINER_HOME="/usr/local/webcontainer"
fi
echo "WEB_CONTAINER_HOME is $WEB_CONTAINER_HOME ."

ServiceHomeDir=$(cd "$(dirname "$0")"; cd ../; pwd)

case "$1" in
	start)
		if [ $# -lt 1 ]
		then
			echo "Usage : $0 start "
			exit
		fi
		counter=`ps -awef | grep "webcontainer" | grep "\<$ServiceName\>" | grep -v grep | wc -l`
		if [ $counter -gt 0 ] 
		then
			echo "Service module $ServiceName already there."
			exit 
		fi
		# Start Service.
		echo "Service($ServiceName) home dir: $ServiceHomeDir."
		$WEB_CONTAINER_HOME/bin/webcontainer $ServiceName
		echo -n "Starting service $ServiceName..."
		echo "done."
		cd ..
		;;
	stop)
		if [ $# -lt 1 ]
		then
			echo "Usage : $0 stop "
			exit
		fi
		counter=`ps -awef | grep "webcontainer" | grep "\<$ServiceName\>" | grep -v grep | wc -l`
		if [ $counter -eq 0 ] 
		then
			echo "Service module $ServiceName already gone."
			exit 
		fi
		# Stop Service.
		echo -n "Stoping service $ServiceName..."
		kill -15 `ps -awef | grep "webcontainer" | grep "\<$ServiceName\>" | grep -v grep | awk '{print $2}'`

		# double kill
		sleep 3
                counter=`ps -awef | grep "webcontainer" | grep "\<$ServiceName\>" | grep -v grep | wc -l`
                if [ $counter -eq 0 ]
                then
                        echo "done"
                        exit
                fi
		kill -9 `ps -awef | grep "webcontainer" | grep "\<$ServiceName\>" | grep -v grep | awk '{print $2}'`
		echo "done"
		;;
	restart)
		if [ $# -lt 1 ]
		then
			echo "Usage : $0 restart"
			exit
		fi
		$0 stop 
		sleep 1
		$0 start 
		;;
	update)
		if [ $# -lt 2 ]
		then
			echo "Usage : $0 update $2"
			exit
		fi
		$0 stop
		sleep 1
        	DATE=`date +%Y%m%d%H%M%S`
        	cp -f ./so/$2.so ./backup/$2.so.$DATE
		mv -f ./update/$2.so ./so/
		$0 start $2
		;;
	show)
		if [ $# -lt 1 ]
		then
			echo "Usage : $0 show "
			exit
		fi
		# Show Service.
		ps -awef | grep "webcontainer" | grep "\<$ServiceName\>" | grep -v grep
		;;
	deploy)
		if [ $# -lt 1 ]
                then
                        echo "Usage : $0 deploy "
                        exit
                fi
                # Deploy Service.
		echo $ServiceHomeDir
		cd $ServiceHomeDir 
		mv deploy/"$ServiceName"_deploy.tgz deploy/"$ServiceName"_deploy.tgz.bak
		tar cvfzh deploy/"$ServiceName"_deploy.tgz bin/service_manager.sh conf/ log service/
                ;;
	register)
		# Do nothing
		;;
	unregister)
		# Do nothing
                ;;	
	backup)
		if [ $# -lt 2 ]
                then
                        echo "Usage : $0 backup backup_dir "
                        exit
                fi
		$0 deploy
		cp $ServiceHomeDir/deploy/"$ServiceName"_deploy.tgz $2/ -f 
		;;
	help)
		if [ $# -lt 1 ]
                then
                        echo "Usage : $0 help "
                        exit
                fi
		echo ""
		echo "TWS(Tencent Web Server) 1.0 - Web application manager "
		echo ""
		echo "Usage: $0 {start|stop|restart|update|show|deploy|register|unregister|backup|help} "
		echo ""
		echo "start: start web application. "
		echo "stop: stop web application. "
		echo "restart: restart web application, stop first, and start the application. "
		echo "update: update specific xxxx.so, and restart the whole web application. "
		echo "show: show web application's running status. "
		echo "deploy: make a distributed tar.gz(tgz) package, and put it into your_web_app_home/deploy/. "
		echo "register: register some system environment variable. "
		echo "unregister: unregister some system environment variable. "
		echo "backup: make a tgz package, and put it into specific directory. "
		echo "help: display these messages."
		echo ""
		echo "@Any suggestion can be sent to Binqiang Huang(yota@tencent.com) by mail. ^-^"
		echo ""
		echo ""
		;;
	*)
		echo "Usage: $0 {start|stop|restart|update|show|deploy|register|unregister|backup|help} "
		exit 1
esac

exit 0

