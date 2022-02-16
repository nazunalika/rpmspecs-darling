# Define global variables
%global _hardened_build 1
%define debug_package %{nil}

# Preventing binary stripping, weird things happen when it's not stripped
%global __os_install_post %{nil}
%global darling_version 0.1.20220213
%global commit 597325bc702e7b0893ade8272000a4086b23f121

Name:		darling
Version:	%{darling_version}
Release:	1
Summary:	macOS translation layer for Linux

License:	GPLv3
URL:		https://www.darlinghq.org

# Change on true release
Source0:	https://github.com/darlinghq/darling/archive/v%{darling_version}.tar.gz
Source1:	darling-dkms.conf

BuildRequires:	git
BuildRequires:	dkms
BuildRequires:	flex
BuildRequires:	llvm
BuildRequires:	make
BuildRequires:	bison
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	python2
BuildRequires:	kernel-devel
BuildRequires:	giflib-devel
BuildRequires:	openssl-devel
BuildRequires:	systemd-devel

BuildRequires:	libxkbfile-devel
BuildRequires:	mesa-libEGL-devel

BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(dri)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libbsd)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(libpulse)
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

# rpmfusion dependencies
BuildRequires:	ffmpeg-devel

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
AutoReqProv:	no

%description	mach
Linux kernel module for darling-mach, required to use darling.

%prep
#%setup -q -n %{name}-%{version}
rm -rf %{name}-%{version} %{name} %{name}-%{commit}
git clone \
  https://github.com/darlinghq/darling.git %{name}-%{version}

%build
cd %{name}-%{version}
git checkout v%{version}
git submodule init
git submodule update --init --recursive
%{__mkdir} build
pushd build
  %{__cmake} -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DOpenGL_GL_PREFERENCE=GLVND \
    ..
  make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}-%{version}

pushd build
  %{make_install}
  %{make_build} lkm_generate
popd

%{__install} -d -m 755 ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/miggen

cp -dr src/external/lkm \
  ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/lkm

cp -dr build/src/external/lkm/osfmk \
  ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/miggen/osfmk

cp build/src/startup/rtsig.h \
  ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/lkm/darling/

sed 's|@@PACKAGE_VERSION@@|%{version}|' %{SOURCE1} > dkms.conf

%{__install} -m 644 dkms.conf \
  ${RPM_BUILD_ROOT}%{_usrsrc}/%{name}-mach-%{version}/dkms.conf

%pre mach
numbersOf=$(%{_sbindir}/dkms status "%{name}/%{version}" | wc -l)
if [ ! ${numbersOf} -gt 0 ]; then
  %{_sbindir}/dkms remove -m %{name}-mach -v %{version} --all --rpm_safe_upgrade || :
fi

%preun mach
%{_sbindir}/dkms remove -m %{name}-mach -v %{version} --all --rpm_safe_upgrade || :

%post mach
%{_sbindir}/dkms add -m %{name}-mach -v %{version} --rpm_safe_upgrade || :
%{_sbindir}/dkms build -m %{name}-mach -v %{version} || :
%{_sbindir}/dkms install -m %{name}-mach -v %{version} || :

%files
%defattr(-, root, root, -)
#%doc LICENSE
%{_bindir}/darling
%dir %{_libexecdir}/darling

%files mach
%defattr(-, root, root, -)
%{_usrsrc}/%{name}-mach-%{version}

%changelog
* Tue Feb 15 2022 Louis Abel <tucklesepk@gmail.com> - 0.1.20220213-1
- Update to alpha release 0.1.20220213

* Mon Oct 25 2021 Louis Abel <tucklesepk@gmail.com> - 0.1.20210801-3
- Update to release 0.1.20210801

* Mon Jun 14 2021 Louis Abel <tucklesepk@gmail.com> - 0.1.20210224-3
- Update to alpha release 0.1.20210224
- Use commit rather than release tar
- Fix macros

* Tue Apr 21 2020 Louis Abel <tucklesepk@gmail.com> - 0.1.20200331-1
- Update to alpha release 0.1.20200331

* Fri Jan 24 2020 Louis Abel <tucklesepk@gmail.com> - 0.1.20200120-1
- Update to alpha release 0.1.20200120

* Fri Aug 16 2019 Louis Abel <tucklesepk@gmail.com> - 0-20190816gitc64519b
- Update to commit c64519

* Tue Aug 13 2019 Louis Abel <tucklesepk@gmail.com> - 0-20190812gitf7b8ad3
- Initial version following the RPM packaging guidelines

