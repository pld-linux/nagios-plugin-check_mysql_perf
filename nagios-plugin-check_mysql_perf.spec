%include	/usr/lib/rpm/macros.perl
Summary:	Nagios plugin: monitor various performance-related characteristics of a MySQL db
Name:		nagios-plugin-check_mysql_perf
Version:	1.3.2.3
Release:	1
License:	GPL v2+
Group:		Networking
Source0:	http://www.consol.com/fileadmin/opensource/Nagios/check_mysql_perf-%{version}.tar.gz
# Source0-md5:	7f6476a15ecb48e2aaacf103d829f104
Source1:	http://dl.sourceforge.net/nagiosplug/nagios-plugins-1.4.13.tar.gz
# Source1-md5:	be6cc7699fff3ee29d1fd4d562377386
URL:		http://www.consol.com/opensource/nagios/check-mysql-perf
BuildRequires:	mysql-devel
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	nagios-core
Conflicts:	nagios-common < 2.9-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_prefix}/lib/nagios/plugins
%define		_sysconfdir	/etc/nagios/plugins

%description
Nagios which allows you to monitor various performance-related
characteristics of a MySQL database.

%prep
%setup -q -n check_mysql_perf-%{version} -a1
ln -s nagios-plugins-* nagios-plugins

# see plugin --help (-m option) for list of these
cat > nagios.cfg <<'EOF'
define command {
	command_name    check_mysql_perf_slave_lag
	command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m slave-lag
}
define command {
        command_name    check_mysql_perf_slave_io_running
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m slave-io-running
}
define command {
        command_name    check_mysql_perf_slave_sql_running
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m slave-sql-running
}
define command {
        command_name    check_mysql_perf_threads_connected
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m threads-connected
}
define command {
        command_name    check_mysql_perf_threadcache_hitrate
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m threadcache-hitrate
}
define command {
        command_name    check_mysql_perf_querycache_hitrate
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m querycache-hitrate
}
define command {
        command_name    check_mysql_perf_keycache_hitrate
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m keycache-hitrate
}
define command {
        command_name    check_mysql_perf_bufferpool_hitrate
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m bufferpool-hitrate
}
define command {
        command_name    check_mysql_perf_tablecache_hitrate
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m tablecache-hitrate
}
define command {
        command_name    check_mysql_perf_table_lock_contention
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m table-lock-contention
}
define command {
        command_name    check_mysql_perf_temp_disk_tables
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m temp-disk-tables
}
define command {
        command_name    check_mysql_perf_connection_time
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m connection-time
}
define command {
        command_name    check_mysql_perf_slow_queries
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m slow-queries
}
define command {
        command_name    check_mysql_perf_qcache_lowmem_prunes
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m qcache-lowmem-prunes
}
define command {
        command_name    check_mysql_perf_bufferpool_wait_free
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m bufferpool-wait-free
}
define command {
        command_name    check_mysql_perf_log_waits
        command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m log-waits
}
EOF

%build
cd nagios-plugins
%configure \
	--disable-perl-modules
%{__make}
cd ..
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios \
	--with-officialplugins=$(pwd)/nagios-plugins
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_prefix}/lib/nagios/plugins,%{_sysconfdir}}

install plugins/check_mysql_perf $RPM_BUILD_ROOT%{_prefix}/lib/nagios/plugins

cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/check_mysql_perf.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/check_mysql_perf.cfg
%attr(755,root,root) %{_prefix}/lib/nagios/plugins/check_mysql_perf
