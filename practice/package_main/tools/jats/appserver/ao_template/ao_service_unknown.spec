Name: unknown_rpm_package
Version: 1
Release: 0
License: Commercial
Group: wxsq_promote
Summary: unknown_rpm_package
Vendor: Tencent
Packager: zhengqingsong
Prefix: /data/bossapp
Provides: unknown_rpm_package
Requires: appserver-boss
Buildroot: /data/htdocs/rpm.paipaioa.com/rpm/data_64/rpm_build/wxsq_promote/unknown_rpm_package_1/build_directory

%description
unknown_rpm_package module for boss
The package is built on SUSE Linux Enterprise Server 10 (i586).

%files
%defattr (-,bossapp,users)
%config(noreplace) /data/bossapp/unknown_rpm_package/conf/*
%config(noreplace) /data/bossapp/monitor/data/*
%dir /data/bossapp/unknown_rpm_package
%dir /data/bossapp/monitor/
%dir /data/bossapp/monitor/data/
%dir /data/bossapp/logs/
/data/bossapp/unknown_rpm_package/bin
/data/bossapp/unknown_rpm_package/log
/data/bossapp/unknown_rpm_package/plugin
/data/bossapp/logs/unknown_rpm_package

%pre

export PATH='/sbin:/usr/sbin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin'
if ! id bossapp &>/dev/null ;then
   echo "Error! User \"bossapp\" NOT found"
   exit 1
fi








%post

ulimit -Sc unlimited















%preun




%postun




%clean

%verifyscript




%changelog
* Tue Jul 04 2018 zhengqingsong
- Version: 1 Release: 0
- ≥ı º∞Ê±æ
