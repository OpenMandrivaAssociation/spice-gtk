%define build_vala	1

%define glibapi		2.0
%define glibmajor	8
%define libglib		%mklibname spice-client-glib %{glibapi} %{glibmajor}
%define glibgir		%mklibname spice-client-glib-gir %{glibapi}
%define gtkapi		3.0
%define gtkmajor	4
%define libgtk		%mklibname spice-client-gtk %{gtkapi} %{gtkmajor}
%define libgtk2		%mklibname spice-client-gtk 2.0 1
%define gtkgir		%mklibname spice-client-gtk-gir %{gtkapi}
%define gtk2gir		%mklibname spice-client-gtk-gir 2.0
%define controllermajor	0
%define libcontroller	%mklibname spice-controller %{controllermajor}
%define develname	%mklibname -d %{name}

Name:		spice-gtk
Version:	0.20
Release:	7
Summary:	A GTK client widget for accessing SPICE desktop servers
Group:		Networking/Remote access
URL:		http://spice-space.org/page/Spice-Gtk
License:	LGPLv2+
Source0:	http://www.spice-space.org/download/gtk/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(cairo) >= 1.2.0
BuildRequires:	pkgconfig(celt051) >= 0.5.1.1
BuildRequires:	pkgconfig(gio-2.0) >= 2.10.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.22
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.9.4
BuildRequires:	pkgconfig(gthread-2.0) > 2.0.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.91.3
BuildRequires:	pkgconfig(gtk+-x11-3.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libcacard) >= 0.1.2
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libpulse-mainloop-glib)
BuildRequires:	pkgconfig(libusb-1.0) >= 1.0.9
BuildRequires:	pkgconfig(libusbredirhost) >= 0.3.3
BuildRequires:	pkgconfig(libusbredirparser-0.5)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(pixman-1) >= 0.17.7
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(spice-protocol) >= 0.10.1
#BuildRequires:	pkgconfig(spice-client-glib-2.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	sasl-devel
BuildRequires:	jpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	perl-Text-CSV
BuildRequires:	intltool
BuildRequires:	ldetect-lst
BuildRequires:	python-parsing
# for virtmanager
BuildRequires:	pygtk2.0-devel

%if %{build_vala}
BuildRequires:	vala
BuildRequires:	vala-tools
%endif

%track
prog %name = {
	url = http://www.spice-space.org/download/gtk/
	regex = %name-(__VER__)\.tar\.bz2
	version = %version
}

%description
Spice-GTK is a GTK client widget for accessing SPICE desktop 
servers. This package contains two simple clients based on the 
library:
  spicy is a client to access SPICE desktops.
  snappy is a tool to capture screen-shots of a SPICE desktop.

%package -n %{libglib}
Summary: Runtime libraries for %{name}
Group: System/Libraries
Conflicts: %{_lib}spice-gtk3.0_1 < 0.7.81-2

%description -n %{libglib}
Runtime libraries for %{name}.

%package -n %{glibgir}
Summary: GObject introspection interface library for %{name}
Group: System/Libraries
Requires: %{libglib} = %{version}-%{release}
Conflicts: %{_lib}spice-gtk3.0_1 < 0.7.81-2

%description -n %{glibgir}
GObject introspection interface library for %{name}.

%package -n %{libgtk}
Summary: Runtime libraries for %{name}
Group: System/Libraries
Obsoletes: %{_lib}spice-gtk3.0_1 < 0.7.81-2

%description -n %{libgtk}
Runtime libraries for %{name}.

%package -n %{gtkgir}
Summary: GObject introspection interface library for %{name}
Group: System/Libraries
Requires: %{libgtk} = %{version}-%{release}
Conflicts: %{_lib}spice-gtk3.0_1 < 0.7.81-2

%description -n %{gtkgir}
GObject introspection interface library for %{name}.

%package -n %{libcontroller}
Summary: Runtime libraries for %{name}
Group: System/Libraries
Conflicts: %{_lib}spice-gtk3.0_1 < 0.7.81-2

%description -n %{libcontroller}
Runtime libraries for %{name}.

%package -n %{libgtk2}
Summary: Runtime libraries for %{name}
Group: System/Libraries

%description -n %{libgtk2}
GTK2 Runtime libraries for %{name}.

%package -n %{gtk2gir}
Summary: GTK2GObject introspection interface library for %{name}
Group: System/Libraries
Requires: %{libgtk2} = %{version}-%{release}

%description -n %{gtk2gir}
GTK2 GObject introspection interface library for %{name}.

%package python
Summary: Python bindings for the spice-gtk-2.0 library
Group: System/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description python
SpiceClientGtk module provides a SPICE viewer widget for GTK2.

A module allowing use of the spice-gtk-2.0 widget from python

%package -n %{develname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libglib} = %{version}-%{release}
Requires: %{libgtk} = %{version}-%{release}
Requires: %{libcontroller} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %{_lib}spice-gtk3.0-devel < 0.7.81-2

%description -n %{develname}
Development files for %{name}.

%prep
%setup -q  -n spice-gtk-%{version} -c
cp -a spice-gtk-%{version} spice-gtk3-%{version}

%build
cd spice-gtk-%{version}
autoreconf -ifv
%configure --with-gtk=2.0 --enable-gtk-doc
make
cd ..

cd spice-gtk3-%{version}
autoreconf -ifv
%configure2_5x \
	--with-gtk=%{gtkapi} \
	--disable-static \
%if %{build_vala}
	--enable-vala \
%else
	--disable-vala \
%endif
	--enable-introspection=yes \
	--enable-usbredir \
	--with-pnp-ids-path=%{_datadir}/misc/pnp.ids
#% make V=1
#make LIBS='-lrt'
%make
cd ..

%install
cd spice-gtk-%{version}
%makeinstall_std
cd ..

cd spice-gtk3-%{version}
%makeinstall_std
cd ..

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.a
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.la

%if ! %{build_vala}
	rm -rf %{buildroot}%{_datadir}/vala/
%endif

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/spicy
%{_bindir}/spicy-screenshot
%{_bindir}/spicy-stats
%{_bindir}/spice-client-glib-usb-acl-helper
%{_datadir}/polkit-1/actions/org.spice-space.lowlevelusbaccess.policy

%files -n %{libglib}
%{_libdir}/libspice-client-glib-%{glibapi}.so.%{glibmajor}
%{_libdir}/libspice-client-glib-%{glibapi}.so.%{glibmajor}.*

%files -n %{glibgir}
%{_libdir}/girepository-1.0/SpiceClientGLib-%{glibapi}.typelib

%files -n %{libgtk}
%{_libdir}/libspice-client-gtk-%{gtkapi}.so.%{gtkmajor}
%{_libdir}/libspice-client-gtk-%{gtkapi}.so.%{gtkmajor}.*

%files -n %{gtkgir}
%{_libdir}/girepository-1.0/SpiceClientGtk-%{gtkapi}.typelib

%files -n %{libcontroller}
%{_libdir}/libspice-controller.so.%{controllermajor}
%{_libdir}/libspice-controller.so.%{controllermajor}.*

%files -n %{libgtk2}
%{_libdir}/libspice-client-gtk-2.0.so.4
%{_libdir}/libspice-client-gtk-2.0.so.4.*

%files -n %{gtk2gir}
%{_libdir}/girepository-1.0/SpiceClientGtk-2.0.typelib

%files python
%{_libdir}/python*/site-packages/SpiceClientGtk.so

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/spice-gtk
%{_includedir}/spice-client-glib-2.0
%{_includedir}/spice-client-gtk-3.0/
%{_includedir}/spice-client-gtk-2.0/
%{_includedir}/spice-controller/
%{_libdir}/libspice-client-glib-2.0.so
%{_libdir}/libspice-client-gtk-3.0.so
%{_libdir}/libspice-client-gtk-2.0.so
%{_libdir}/libspice-controller.so
%{_libdir}/pkgconfig/spice-client-glib-2.0.pc
%{_libdir}/pkgconfig/spice-client-gtk-3.0.pc
%{_libdir}/pkgconfig/spice-client-gtk-2.0.pc
%{_libdir}/pkgconfig/spice-controller.pc
%{_datadir}/gir-1.0/SpiceClientGLib-2.0.gir
%{_datadir}/gir-1.0/SpiceClientGtk-3.0.gir
%{_datadir}/gir-1.0/SpiceClientGtk-2.0.gir
%if %{build_vala}
%{_datadir}/vala/vapi/spice-protocol.vapi
%{_datadir}/vala/vapi/spice-client-glib-%{glibapi}.deps
%{_datadir}/vala/vapi/spice-client-glib-%{glibapi}.vapi
%{_datadir}/vala/vapi/spice-client-gtk-%{gtkapi}.deps
%{_datadir}/vala/vapi/spice-client-gtk-%{gtkapi}.vapi
%endif
