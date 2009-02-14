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

cat > nagios.cfg <<'EOF'
define command {
	command_name    check_mysql_perf
	command_line    $USER1$/check_mysql_perf -H $HOSTADDRESS$
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
