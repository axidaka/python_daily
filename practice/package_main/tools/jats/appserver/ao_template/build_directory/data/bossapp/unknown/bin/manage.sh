#!/bin/sh

service="ao_unknown_service"

proclist="appchn_$service appsvc_$service"

help()
{
	echo "usage:$0 cmd"
	echo "--cmd  show\start\stop\restart"
}

show()
{
	for procgram in $proclist	
	do
		ps -ef|grep -i "$procgram"|grep -v "grep"
	done

}

start()
{

	for procgram in $proclist
	do
	  ./$procgram  ../conf/$procgram.xml	
	done

}

stop()
{
	for procgram in $proclist	
	do
		pids=$(ps -ef|grep -i "$procgram"|grep -v "grep"|awk '{print $2}')

		for pid in $pids
		do
			#echo $pid
			kill -9 $pid
		done
	done
}

if [ $# != 1 ];then
	help
	exit
fi

case "$1" in
	"show" )
		show
	;;
	"start" )
		echo "start..."
		start
		echo "start done..."
		show
	;;
	"stop" )
		echo "stop... "
		stop
		echo "stop done"
	;;
	"restart" )
		stop
		echo "stop service done."
		start
		echo "start service done."
		show
	;;
	*  )
		echo "$1 is not a valid cmd"
		help
	;;
esac
