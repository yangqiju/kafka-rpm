Name:           kafka_2.11
Version:        0.9.0.1
Release:        1%{?dist}
Summary:        Kafka distributed topic based producer consumer queue 

Group:          Applications 
License:        Apache (v2) 
URL:            http://kafka.apache.org  
Source0:        %{name}-%{version}.tgz
Source1:        kafka.init
BuildArch:	noarch
#BuildRequires:  
Requires:       java >= 1.7  
Requires:	zookeeper
Requires(post):	/sbin/chkconfig,/sbin/service
Requires(preun): /sbin/chkconfig,/sbin/service
Provides:	kafka

%description

%define data_dir %{_datadir}/kafka
%define user kafka
%define group kafka
%define home /opt/kafka

%pre
getent group %{group} >/dev/null || groupadd -r %{group} 
getent passwd %{user} >/dev/null || \
    useradd -r -g %{group} -d %{_sharedstatedir}/kafka -s /sbin/nologin \
    -c "User for kafka services" %{user}
exit 0

%preun
/sbin/service kafka stop > /dev/null 2>&1
/sbin/chkconfig --del kafka > /dev/null 2>&1

%postun
rm -rf %{home}
rm -rf %{_sharedstatedir}/kafka
rm -rf %{_localstatedir}/log/kafka
rm -rf %{_sysconfdir}/kafka

%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}%{home}
mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}%{_localstatedir}/lib/kafka
mkdir -p %{buildroot}%{_var}/log/kafka
mkdir -p %{buildroot}%{data_dir}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}%{_sysconfdir}/kafka
cp -R $RPM_BUILD_DIR/%{name}-%{version}/* %{buildroot}%{home}

sed "s,log.dirs=.*,log.dirs=%{_sharedstatedir}/kafka/data," config/server.properties >%{buildroot}%{home}/config/server.properties
cp  %{buildroot}%{home}/config/server.properties %{buildroot}%{_sysconfdir}/kafka/server.properties
install -m 755 %{S:1} %{buildroot}%{_initrddir}/kafka


%post
/sbin/chkconfig kafka on
#/sbin/service zookeeper start
#/sbin/service kafka start

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc

%{_initrddir}/kafka
%config %attr(-,%{user},%{group}) %{home}
%config %attr(-,%{user},%{group}) %{_sharedstatedir}/kafka
%config %attr(-,%{user},%{group}) %{_localstatedir}/log/kafka
%config %attr(-,%{user},%{group}) %{_sysconfdir}/kafka


%changelog
