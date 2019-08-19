# Define global variables
%global _hardened_build 1
%define debug_package %{nil}

# Preventing binary stripping, weird things happen when it's not stripped
%global __os_install_post %{nil}

# They don't do releases yet. Remove when we move to releases.
%global commit c64519b5e74e1838b5837e1404e59da09b78fe6a
%global gittag refs/heads/master
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%define gitURL https://github.com/darlinghq/darling

# When there's no release, the proper way to version anything out is via
# the commit date and version and leaving the package version as 0.
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/Versioning/#_snapshots
%global releaseVer 20190816git%{shortcommit}

Name:		darling
Version:	0
Release:	%{releaseVer}%{?dist}
Summary:	macOS translation layer for Linux

License:	GPLv3
URL:		https://www.darlinghq.org

# Change on true release
#Source0:	https://github.com/darlinghq/darling/...
Source1:	darling-dkms.conf

BuildRequires:	git
BuildRequires:	dkms
BuildRequires:	make
BuildRequires:	flex
BuildRequires:	cmake
BuildRequires:	clang
BuildRequires:	bison
BuildRequires:	python2
BuildRequires:	systemd-devel
BuildRequires:	kernel-devel
BuildRequires:	libglvnd-devel

BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(libbsd)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(libxml-2.0)

# Multiarch dependencies
BuildRequires:	freetype-devel(x86-64)
BuildRequires:	freetype-devel(x86-32)
BuildRequires:	fontconfig-devel(x86-64)
BuildRequires:	fontconfig-devel(x86-32)
BuildRequires:	glibc-devel(x86-64)
BuildRequires:	glibc-devel(x86-32)
BuildRequires:	libjpeg-turbo-devel(x86-64)
BuildRequires:	libjpeg-turbo-devel(x86-32)
BuildRequires:	libtiff-devel(x86-64)
BuildRequires:	libtiff-devel(x86-32)

AutoReqProv:	no

%description
Darling is a translation layer that lets you run macOS software on Linux

Darling runs macOS software directly without using a hardware emulator. Like
Linux, Darling is free and open-source software. It is developed openly on
GitHub and distributed under the GNU GPL lincense version 3. Darling implements
a complete Darwin environment. Mach, dyld, launchd - everything you'd expect.

Darling does most of the setup for you. Sit back and enjoy using your favorite
software.

We aim to fully integrate apps running under Darling into the Linux desktop
experience by making them look, feel, and behave just like native Linux apps.

%package	mach
Summary:	Kernel Module for Darling
Requires:	kernel-devel
Requires:	dkms

%description	mach
Linux kernel module for darling-mach, required to use darling.

%prep
# Remove and replace with setup after releases
rm -rf %{name}-%{commit} %{name}
git clone --recurse-submodules %{gitURL} %{name}-%{releaseVer}
# End

%build
# Remove after releases
cd %{name}-%{releaseVer}
# End

# Following the methodology of their build page
%{__mkdir} build
pushd build
  %{__cmake} -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DOpenGL_GL_PREFERENCE=GLVND \
    ..
  make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}-%{releaseVer}

pushd build
  %make_install
  make %{?_smp_mflags} lkm_generate
  %{__install} -d -m 755 ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/miggen
  %{__install} -d -m 755 ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/lkm/darling

  cp -dr src/lkm/osfmk \
    ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/miggen/osfmk

  cp src/startup/rtsig.h \
    ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/lkm/darling/
popd

%{__install} -m 644 %{SOURCE1} %{?buildroot}%{_usrsrc}/%{name}-mach-%{version}/dkms.conf

cp -dr src/lkm \
  ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/lkm

%preun mach
%{_sbin}/dkms remove -m %{name}-mach -v %{version} --all || :

%post mach
numbersOf=$(%{_sbin}/dkms status | grep "%{name}" | grep "%{version}" | wc -l)

if [ ! ${numbersOf} -gt 0 ]; then
  %{_sbin}/dkms add -m %{name}-mach -v %{version} || :
fi

%{_sbin}/dkms build -m %{name}-mach -v %{version} || :
%{_sbin}/dkms install -m %{name}-mach -v %{version} || :

%files
%defattr(-, root, root, -)
#%doc LICENSE
%{_bindir}/darling
%{_libexecdir}/darling

%files mach
%defattr(-, root, root, -)
%{_usrsrc}/%{name}-mach-%{version}

%changelog
* Fri Aug 16 2019 Louis Abel <tucklesepk@gmail.com> - 0-20190816gitc64519b
- Update to commit c64519

* Tue Aug 13 2019 Louis Abel <tucklesepk@gmail.com> - 0-20190812gitf7b8ad3
- Initial version following the RPM packaging guidelines

