# Define global variables
%global _hardened_build 1
%define debug_package %{nil}

# Preventing binary stripping, weird things happen when it's not stripped
%global __os_install_post %{nil}
%global darling_version 0.1.20210224

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
AutoReqProv:	no

%description	mach
Linux kernel module for darling-mach, required to use darling.

%prep
%setup -q -n %{name}-%{version}

%build
# Following the methodology of their build page
#   Use the below when releases work
#   -DOpenGL_GL_PREFERENCE=GLVND \
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
* Fri May 22 2021 Louis Abel <tucklesepk@gmail.com> - 0.1.20210224-1
- Update to alpha release 0.1.20210224

* Tue Apr 21 2020 Louis Abel <tucklesepk@gmail.com> - 0.1.20200331-1
- Update to alpha release 0.1.20200331

* Fri Jan 24 2020 Louis Abel <tucklesepk@gmail.com> - 0.1.20200120-1
- Update to alpha release 0.1.20200120

* Fri Aug 16 2019 Louis Abel <tucklesepk@gmail.com> - 0-20190816gitc64519b
- Update to commit c64519

* Tue Aug 13 2019 Louis Abel <tucklesepk@gmail.com> - 0-20190812gitf7b8ad3
- Initial version following the RPM packaging guidelines

