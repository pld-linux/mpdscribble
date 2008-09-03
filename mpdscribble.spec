#
# TODO:
# - the author seazed to maintain this project, yet this is the only scrobbler for mpd I've found; look for s/b maintaining it
#
Summary:	Scrobbler for mpd
Summary(pl.UTF-8):	Scrobbler dla mpd
Name:		mpdscribble
Version:	0.2.12
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	http://www.frob.nl/projects/scribble/%{name}-%{version}.tar.gz
# Source0-md5:	7f0e976e7a066df0ddf21f3f4041ef6a
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.conf
Patch0:		%{name}-libsoup.patch
Patch1:		%{name}-warnings_and_operator.patch
Patch2:		%{name}-default_verbose_level.patch
Patch3:		%{name}-memory_corruption.patch
Patch4:		%{name}-path.patch
URL:		http://www.frob.nl/scribble.html
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libsoup-devel >= 2.2
BuildRequires:	pkgconfig
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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
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
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/mpdscribble

touch $RPM_BUILD_ROOT/var/log/%{name}.log
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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/mpdscribble.1*
%dir %{_sysconfdir}/mpdscribble
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mpdscribble/mpdscribble.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %ghost /var/log/%{name}.log
%dir %attr(750,root,root) /var/cache/%{name}
/var/cache/%{name}/%{name}.cache
