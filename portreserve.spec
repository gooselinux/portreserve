Summary: TCP port reservation utility
Name: portreserve
Version: 0.0.4
Release: 4%{?dist}
License: GPLv2+
Group: System Environment/Daemons
URL: http://cyberelk.net/tim/portreserve/
Source0: http://cyberelk.net/tim/data/portreserve/stable/%{name}-%{version}.tar.bz2
Patch1: portreserve-infinite-loop.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: xmlto
Obsoletes: portreserve-selinux < 0.0.3-3

%description
The portreserve program aims to help services with well-known ports that
lie in the portmap range.  It prevents portmap from a real service's port
by occupying it itself, until the real service tells it to release the
port (generally in the init script).

%prep
%setup -q
# Prevent infinite loop.
%patch1 -p1 -b .infinite-loop

%build
%configure --sbindir=/sbin
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_localstatedir}/run/portreserve
mkdir -p %{buildroot}%{_initrddir}
install -m755 portreserve.init %{buildroot}%{_initrddir}/portreserve
mkdir -p %{buildroot}%{_sysconfdir}/portreserve

%clean
rm -rf %{buildroot}

%post
# Do this unconditionally to fix up the initscript's start priority.
# Earlier versions had an incorrect dependency (bug #487250).
/sbin/chkconfig --add portreserve

%preun
if [ "$1" = 0 ]; then
  /sbin/service portreserve stop >/dev/null 2>&1
  /sbin/chkconfig --del portreserve
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service portreserve condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root)
%doc ChangeLog README COPYING NEWS
%dir %{_localstatedir}/run/portreserve
%dir %{_sysconfdir}/portreserve
%attr(755,root,root) %{_initrddir}/portreserve
/sbin/*
%{_mandir}/*/*

%changelog
* Thu Mar  4 2010 Tim Waugh <twaugh@redhat.com> 0.0.4-4
- Added comments to all patches.

* Fri Jan 22 2010 Tim Waugh <twaugh@redhat.com> 0.0.4-3
- Walk the list of newmaps correctly (bug #557785).

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.0.4-2.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Tim Waugh <twaugh@redhat.com> 0.0.4-1
- 0.0.4:
  - Fixed initscript so that it will not be reordered to start after
    rpcbind (bug #487250).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Tim Waugh <twaugh@redhat.com> 0.0.3-3
- No longer need SELinux policy as it is now part of the
  selinux-policy package.

* Wed Oct 15 2008 Tim Waugh <twaugh@redhat.com> 0.0.3-2
- New selinux sub-package for SELinux policy.  Policy contributed by
  Miroslav Grepl (thanks!).

* Tue Jul  1 2008 Tim Waugh <twaugh@redhat.com> 0.0.3-1
- 0.0.3:
  - Allow multiple services to be defined in a single configuration
    file.
  - Allow protocol specifications, e.g. ipp/udp.

* Mon Jun 30 2008 Tim Waugh <twaugh@redhat.com> 0.0.2-1
- 0.0.2.

* Fri May  9 2008 Tim Waugh <twaugh@redhat.com> 0.0.1-2
- More consistent use of macros.
- Build requires xmlto.
- Don't use %%makeinstall.
- No need to run make check.

* Thu May  8 2008 Tim Waugh <twaugh@redhat.com> 0.0.1-1
- Default permissions for directories.
- Initscript should not be marked config.
- Fixed license tag.
- Better buildroot tag.

* Wed Sep  3 2003 Tim Waugh <twaugh@redhat.com>
- Initial spec file.
