Name: unknown_rpm_package
Version: 1
Release: 1
License: Commercial
Group: wxsq_promote
Summary: unknown_rpm_package
Vendor: Tencent
Packager: jiangkui
Prefix: /data/bossapp
Provides: unknown_rpm_package
Requires: appserver-boss
Buildroot: /data/htdocs/rpm.paipaioa.com/rpm/data_64/rpm_build/wxsq_promote/unknown_rpm_package_1/build_directory

%description
unknown_rpm_package module for boss
The package is built on SUSE Linux Enterprise Server 10 (i586).

%files
%defattr (-,bossapp,users)
%dir /data/bossapp/unknown_rpm_package
%dir /data/bossapp/monitor/
%config(noreplace) /data/bossapp/unknown_rpm_package/conf/*
/data/bossapp/unknown_rpm_package/bin
/data/bossapp/unknown_rpm_package/conf
/data/bossapp/unknown_rpm_package/logs
/data/bossapp/logs/unknown_rpm_package
/data/bossapp/monitor/data/

%pre

export PATH='/sbin:/usr/sbin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin'
#step0-user check
if ! id bossapp &>/dev/null ;then
   echo "Error! User \"bossapp\" NOT found"
   exit 1
fi








%post

export PATH='/sbin:/usr/sbin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin'

#step1-enable coredump
ulimit -c unlimited











%preun




%postun




%clean

%verifyscript




%changelog
* Wed Mar 01 2017 jiangkui
- Version: 1 Release: 1
- ¿¿¿¿

