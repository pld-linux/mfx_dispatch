#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Intel Media SDK dispatcher library
Summary(pl.UTF-8):	Biblioteka dispatchera z Intel Media SDK
Name:		mfx_dispatch
Version:	1.25
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/lu-zero/mfx_dispatch/releases
Source0:	https://github.com/lu-zero/mfx_dispatch/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bf743b4b9adbe55bd7154274eddb6af6
URL:		https://github.com/lu-zero/mfx_dispatch
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libva-drm-devel
BuildRequires:	libva-x11-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Intel Media SDK dispatcher library.

%description -l pl.UTF-8
Biblioteka dispatchera z Intel Media SDK.

%package devel
Summary:	Header files for MFX library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MFX
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	libva-drm-devel
Requires:	libva-x11-devel

%description devel
Header files for MFX library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MFX.

%package static
Summary:	Static MFX library
Summary(pl.UTF-8):	Statyczna biblioteka MFX
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MFX library.

%description static -l pl.UTF-8
Statyczna biblioteka MFX.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-shared \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmfx.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libmfx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmfx.so.1

%files devel
%defattr(644,root,root,755)
%doc readme-dispatcher.rtf
%attr(755,root,root) %{_libdir}/libmfx.so
%{_includedir}/mfx
%{_pkgconfigdir}/libmfx.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmfx.a
%endif
