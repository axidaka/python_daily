Name: unknown_rpm_package
Version: 1
Release: 1
License: Commercial
Group: wxsq_promote
Summary: active unknown_tws
Vendor: Tencent
Packager: jiangkui
Prefix: /usr/local/webapps
Provides: unknown_rpm_package

Buildroot: /data/htdocs/rpm.paipaioa.com/rpm/data_64/rpm_build/wxsq_promote/unknown_rpm_package_1/build_directory

%description
unknown_rpm_package

%files
%defattr (-,webadmin,users)
%config /usr/local/webapps/unknown_rpm_package/conf
%dir /usr/local/webapps/unknown_rpm_package
/usr/local/webapps/unknown_rpm_package/bin
/usr/local/webapps/unknown_rpm_package/log
/usr/local/webserver/conf
/usr/local/webapps/unknown_rpm_package/service
/data/webapps_log/unknown_logdir

%pre

export PATH='/sbin:/usr/sbin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin'
#step0-user check
if ! id webadmin &>/dev/null ;then
echo "Error! User \"webadmin\" NOT found"
exit 1
fi

confdir="/usr/local/webapps/unknown_rpm_package/conf"
[ -d ${confdir}/bak/ ] || mkdir -p ${confdir}/bak/
cd ${confdir} 
find ./ -maxdepth 1 -type f -exec cp -p {} ${confdir}/bak/{} \;
chown webadmin.users ${confdir}/bak/ -R






			

%post

#export PATH='/sbin:/usr/sbin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin'

#if [ "$1" -gt "1" ] ; then
# restart web app 
#su - webadmin -c "cd /usr/local/webapps/unknown_rpm_package/bin/ && ./service_manager.sh restart >/dev/null 2>&1"; 
#else
# add web server vhost 
# restart webapp
#su - webadmin -c "cd /usr/local/webapps/unknown_rpm_package/bin/ && ./service_manager.sh restart >/dev/null 2>&1"; 
# restart webserver 
#cd /usr/local/webserver/bin && ./webserver_manager.sh restart >/dev/null 2>&1;
#fi














%preun

if [ "$1" -eq "0" ] ; then
/usr/local/sbin/crontab-modify.pl -d -u webadmin -c 'unknown_rpm_package/bin/protect.sh'

cd /usr/local/webapps/unknown_rpm_package/bin/ && ./service_manager.sh stop
echo "Waiting 2 seconds for application exit"
sleep 2
find /data/webapps_log/unknown_rpm_package -name "*.log" -type f | xargs rm -f
fi


%postun

if [ "$1" -eq "0" ] ; then
/usr/local/sbin/tws-vhost-modify.pl -d -v unknown.com
cd /usr/local/webserver/bin && ./webserver_manager.sh restart >/dev/null 2>&1
fi


%clean

%verifyscript




%changelog
* Thu Mar 31 2016 p_jdywjyang
- Version: 1 Release: 0
- first install