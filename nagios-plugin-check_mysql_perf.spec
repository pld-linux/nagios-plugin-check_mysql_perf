%define		plugin	check_mysql_perf
Summary:	Nagios plugin: monitor various performance-related characteristics of a MySQL db
Name:		nagios-plugin-%{plugin}
Version:	1.3.2.3
Release:	2
License:	GPL v2+
Group:		Networking
Source0:	http://www.consol.com/fileadmin/opensource/Nagios/%{plugin}-%{version}.tar.gz
# Source0-md5:	7f6476a15ecb48e2aaacf103d829f104
Patch0:		nagios-plugin-check_mysql_perf-np.patch
URL:		http://www.consol.com/opensource/nagios/check-mysql-perf
BuildRequires:	mysql-devel
BuildRequires:	nagios-plugins-devel
Requires:	nagios-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin which allows you to monitor various performance-related
characteristics of a MySQL database.

%prep
%setup -q -n %{plugin}-%{version}
%patch0 -p1

# see plugin --help (-m option) for list of these
cat > nagios.cfg <<'EOF'
define command {
	command_name    %{plugin}_slave_lag
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m slave-lag
}
define command {
	command_name    %{plugin}_slave_io_running
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m slave-io-running
}
define command {
	command_name    %{plugin}_slave_sql_running
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m slave-sql-running
}
define command {
	command_name    %{plugin}_threads_connected
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m threads-connected
}
define command {
	command_name    %{plugin}_threadcache_hitrate
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m threadcache-hitrate
}
define command {
	command_name    %{plugin}_querycache_hitrate
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m querycache-hitrate
}
define command {
	command_name    %{plugin}_keycache_hitrate
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m keycache-hitrate
}
define command {
	command_name    %{plugin}_bufferpool_hitrate
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m bufferpool-hitrate
}
define command {
	command_name    %{plugin}_tablecache_hitrate
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m tablecache-hitrate
}
define command {
	command_name    %{plugin}_table_lock_contention
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m table-lock-contention
}
define command {
	command_name    %{plugin}_temp_disk_tables
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m temp-disk-tables
}
define command {
	command_name    %{plugin}_connection_time
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m connection-time
}
define command {
	command_name    %{plugin}_slow_queries
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m slow-queries
}
define command {
	command_name    %{plugin}_qcache_lowmem_prunes
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m qcache-lowmem-prunes
}
define command {
	command_name    %{plugin}_bufferpool_wait_free
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m bufferpool-wait-free
}
define command {
	command_name    %{plugin}_log_waits
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$ -u $ARG1$ -p $ARG2$ -m log-waits
}
EOF

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios \
	--with-officialplugins=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{plugindir},%{_sysconfdir}}
install plugins/%{plugin} $RPM_BUILD_ROOT%{plugindir}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
