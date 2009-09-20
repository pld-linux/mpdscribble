#
# TODO:
# - the author seazed to maintain this project, yet this is the only scrobbler for mpd I've found; look for s/b maintaining it
#
Summary:	Scrobbler for mpd
Summary(pl.UTF-8):	Scrobbler dla mpd
Name:		mpdscribble
Version:	0.18.1
Release:	1
License:	GPL v2+
Group:		Daemons
Source0:	http://dl.sourceforge.net/musicpd/%{name}-%{version}.tar.gz
# Source0-md5:	f3ab2ef721426362f2ebc27a165b1cba
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-path.patch
URL:		http://mpd.wikia.com/wiki/Client:Mpdscribble
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libsoup-devel >= 2.2
BuildRequires:	pkgconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.0.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mpdscribble is a music player daemon client which submits information
about tracks being played to audioscrobbler.

%description -l pl.UTF-8
Mpdscrible to klient demona odtwarzania muzyki, który wysyła
informacje o odtwarzanych utworach do audioscrobblera.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -Im4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-http-client=soup
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_sysconfdir}/mpdscribble \
	$RPM_BUILD_ROOT/etc/sysconfig \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/var/{log,cache/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mpdscribble
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/mpdscribble

install -d $RPM_BUILD_ROOT/var/log/mpdscribble
touch $RPM_BUILD_ROOT/var/log/mpdscribble/%{name}.log
touch $RPM_BUILD_ROOT/var/cache/%{name}/%{name}.cache

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_sysconfdir}/mpdscribble
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mpdscribble/mpdscribble.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man1/mpdscribble.1*
%dir /var/log/mpdscribble
%attr(640,root,root) %ghost /var/log/mpdscribble/%{name}.log
%dir %attr(750,root,root) /var/cache/%{name}
/var/cache/%{name}/%{name}.cache
