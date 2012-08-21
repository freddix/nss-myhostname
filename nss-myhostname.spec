Summary:	glibc plugin for local system host name resolution
Name:		nss-myhostname
Version:	0.3
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://0pointer.de/lennart/projects/nss-myhostname/%{name}-%{version}.tar.gz
# Source0-md5:	d4ab9ac36c053ab8fb836db1cbd4a48f
URL:		http://0pointer.de/lennart/projects/nss-myhostname/
Requires(post,postun):	/usr/sbin/ldconfig
Requires(postun):	/usr/sbin/postshell
Requires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2).

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig -X
if [ -f %{_sysconfdir}/nsswitch.conf ]; then
	%{__sed} -i -e '
		/^hosts:/ !b
		/\<myhostname\>/ b
		s/[[:blank:]]*$/ myhostname/
	' %{_sysconfdir}/nsswitch.conf
fi

%preun
if [ "$1" -eq 0 -a -f %{_sysconfdir}/nsswitch.conf ] ; then
	%{__sed} -i -e '
		/^hosts:/ !b
		s/[[:blank:]]\+myhostname\>//
	' %{_sysconfdir}/nsswitch.conf
fi

%postun -p /usr/sbin/postshell
/usr/sbin/ldconfig -X

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libnss_myhostname.so.?

