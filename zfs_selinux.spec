# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /usr/sbin/zfs; \
restorecon -R /usr/sbin/zpool; \
restorecon -R /etc/rc\.d/init\.d/zfs; \
restorecon -R /dev/zfs; \

%define selinux_policyver 3.11.1-96

Name:   zfs_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for zfs

Group:	System Environment/Base		
License:	GPLv2+	
# This is an example. You will need to change it.
URL:		http://HOSTNAME
Source0:	zfs.pp
Source1:	zfs.if
Source2:	zfs_selinux.8

Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
Requires(post): zfs
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for zfs.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/

%post
semodule -n -i %{_datadir}/selinux/packages/zfs.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files
fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r zfs
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/zfs.pp
%{_datadir}/selinux/devel/include/contrib/zfs.if
%{_mandir}/man8/zfs_selinux.8.*

%changelog
* Fri May 31 2013 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
- Initial version

