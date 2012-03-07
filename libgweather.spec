Summary:	Library to access weather information from online services for numerous locations
Summary(pl.UTF-8):	Biblioteka dostępu do informacji pogodowych z serwisów internetowych dla różnych miejsc
Name:		libgweather
Version:	3.4.0
Release:	1
License:	GPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgweather/3.4/%{name}-%{version}.tar.xz
# Source0-md5:	9420d521f7dfdf2d210190bb52e3313a
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.26.0
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common >= 2.20.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.40.6
BuildRequires:	libsoup-gnome-devel >= 2.26.0
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	gnome-icon-theme
Requires(post,postun):	gnome-icon-theme-symbolic
Requires(post,postun):	gtk-update-icon-cache
Requires(post,preun):	GConf2
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgweather is a library to access weather information from online
services for numerous locations.

%description -l pl.UTF-8
libgweather to biblioteka pozwalająca na dostęp do informacji
pogodowych z serwisów internetowych dla różnych miejsc.

%package devel
Summary:	Header files for libgweather
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgweather
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	GConf2-devel >= 2.26.0
Requires:	gtk+3-devel >= 3.0.0
Requires:	libsoup-devel >= 2.26.0
Requires:	libxml2-devel >= 1:2.6.30
Obsoletes:	gnome-applets-devel <= 2.21.4

%description devel
Header files for libgweather.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgweather.

%package static
Summary:	Static libgweather library
Summary(pl.UTF-8):	Statyczna biblioteka libgweather
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libgweather library.

%description static -l pl.UTF-8
Statyczna biblioteka libgweather.

%package apidocs
Summary:	libgweather API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libgweather
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libgweather API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libgweather.

%prep
%setup -q

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-zoneinfo-dir=%{_datadir}/zoneinfo \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--disable-silent-rules \
	--enable-static

%{__make} -j1 -C data
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/es_ES
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang libgweather-3.0

find $RPM_BUILD_ROOT -name "Locations.*.xml" | sed 's:'"$RPM_BUILD_ROOT"'::
s:\(.*\)/Locations\.\([^.]*\)\.xml:%lang(\2) \1/Locations.\2.xml:' >> libgweather-3.0.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_icon_cache gnome
%gconf_schema_install gweather.schemas

%preun
%gconf_schema_uninstall gweather.schemas

%postun
/sbin/ldconfig
%update_icon_cache gnome

%files -f libgweather-3.0.lang
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_libdir}/libgweather-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgweather-3.so.0
%{_sysconfdir}/gconf/schemas/gweather.schemas
%dir %{_datadir}/libgweather
%{_datadir}/libgweather/Locations.xml
%{_datadir}/libgweather/locations.dtd
%{_iconsdir}/gnome/*/status/*.png
%{_iconsdir}/gnome/scalable/status/*.svg
%{_libdir}/girepository-1.0/GWeather-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgweather-3.so
%{_includedir}/libgweather-3.0
%{_pkgconfigdir}/gweather-3.0.pc
%{_datadir}/gir-1.0/GWeather-3.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libgweather-3.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libgweather-3.0
