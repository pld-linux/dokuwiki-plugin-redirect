%define		subver	2017-11-05
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		redirect
%define		php_min_version 5.3.0
Summary:	DokuWiki redirect plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/splitbrain/dokuwiki-plugin-redirect/archive/%{subver}/%{plugin}-%{subver}.tar.gz
# Source0-md5:	9a75af351d1d2352d7903c57a3c2f82e
URL:		https://www.dokuwiki.org/plugin:redirect
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20131208
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
Redirects page accesses to other pages or external sites using a
central configuration file.

%prep
%setup -qc
mv *-%{plugin}-*/* .

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/README
%{__rm} $RPM_BUILD_ROOT%{plugindir}/*/.gitignore

install -d $RPM_BUILD_ROOT%{dokuconf}
touch $RPM_BUILD_ROOT%{dokuconf}/%{plugin}.conf

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{dokuconf}/%{plugin}.conf
%dir %{plugindir}
%{plugindir}/*.php
%{plugindir}/*.svg
%{plugindir}/*.txt
%{plugindir}/conf
