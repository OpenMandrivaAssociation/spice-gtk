# Please keep this package in sync with FC

%define glibapi		2.0
%define glibmajor	8
%define libglib		%mklibname spice-client-glib %{glibapi} %{glibmajor}
%define glibgir		%mklibname spice-client-glib-gir %{glibapi}
%define gtkmajor	5
%define gtkapi3		3.0
%define libgtk3		%mklibname spice-client-gtk %{gtkapi3} %{gtkmajor}
%define gtkgir3		%mklibname spice-client-gtk-gir %{gtkapi3}
%define develname	%mklibname -d %{name}

Name:		spice-gtk
Version:	0.37
Release:	1
Summary:	A GTK client widget for accessing SPICE desktop servers
Group:		Networking/Remote access
URL:            https://www.spice-space.org/spice-gtk.html
License:	LGPLv2+
Source0:        https://www.spice-space.org/download/gtk/%{name}-%{version}%{?_version_suffix}.tar.bz2
Patch0001:      0001-meson-improve-gtk-doc-build.patch

Patch2:      0001-vmcstream-Fix-buffer-overflow-sending-data-to-task.patch
Patch3:      0001-clipboard-do-not-release-between-client-grabs.patch
Patch4:      0002-clipboard-do-not-release-between-remote-grabs.patch
Patch5:      0003-fixup-clipboard-do-not-release-between-remote-grabs.patch
Patch6:      0004-clipboard-do-not-delay-release-if-agent-has-no-relea.patch
Patch7:      0005-clipboard-pre-condition-on-selection-value-256.patch
Patch8:      0006-clipboard-implement-CAP_CLIPBOARD_GRAB_SERIAL.patch

BuildRequires:	git-core
BuildRequires:	meson
BuildRequires:	pkgconfig(cairo) >= 1.2.0
BuildRequires:	pkgconfig(gio-2.0) >= 2.10.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.43.90
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.9.4
BuildRequires:	pkgconfig(gthread-2.0) > 2.0.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.91.3
BuildRequires:	pkgconfig(gtk+-x11-3.0)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-app-1.0)
BuildRequires:	pkgconfig(gstreamer-audio-1.0)
BuildRequires:	pkgconfig(libcacard) >= 0.1.2
BuildRequires:	pkgconfig(libphodav-2.0)
BuildRequires:	pkgconfig(libusb-1.0) >= 1.0.16
BuildRequires:	pkgconfig(libusbredirhost) >= 0.3.3
BuildRequires:  pkgconfig(libdrm)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(opus) >= 0.9.14
BuildRequires:	pkgconfig(pixman-1) >= 0.17.7
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	sasl-devel
BuildRequires:	jpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	ldetect-lst
BuildRequires:	vala-tools
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	gtk-doc
BuildRequires:	vala
BuildRequires:	usbutils
BuildRequires:	pkgconfig(libsoup-2.4) >= 2.49.91
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	acl-devel
BuildRequires:  json-glib-devel
BuildRequires:	pkgconfig(spice-protocol) >= 0.12.15
BuildRequires:  spice-vdagent
BuildRequires:	python-six
BuildRequires:  python2-six

%description
Spice-GTK is a GTK client widget for accessing SPICE desktop
servers. This package contains two simple clients based on the
library:
  spicy is a client to access SPICE desktops.
  spicy-screenshot is a tool to capture screen-shots of a SPICE desktop.

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

%package -n %{libgtk3}
Summary: Runtime libraries for %{name}
Group: System/Libraries
Obsoletes: %{_lib}spice-gtk3.0_1 < 0.7.81-2

%description -n %{libgtk3}
Runtime libraries for %{name}.

%package -n %{gtkgir3}
Summary: GObject introspection interface library for %{name}
Group: System/Libraries
Requires: %{libgtk3} = %{version}-%{release}
Conflicts: %{_lib}spice-gtk3.0_1 < 0.7.81-2

%description -n %{gtkgir3}
GObject introspection interface library for %{name}.

%package -n %{develname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libglib} = %{version}-%{release}
Requires: %{libgtk3} = %{version}-%{release}
Requires: %{glibgir} = %{version}-%{release}
Requires: %{gtkgir3} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %{_lib}spice-gtk3.0-devel < 0.7.81-2

%description -n %{develname}
Development files for %{name}.

%prep
%autosetup -S git_am

%build
# meson macro has --auto-features=enabled
# gstreamer should be enough, may be deprecated in the future
%global mjpegflag -Dbuiltin-mjpeg=false
# spice-common doesn't use auto feature yet
%global celt051flag -Dcelt051=disabled
# pulse is deprecated upstream
%global pulseflag -Dpulse=disabled
sed -i '/-Werror/d' subprojects/spice-common/meson.build
export LDFLAGS="%{ldflags} -lm"

%meson \
  %{mjpegflag} \
  %{celt051flag} \
  %{pulseflag} \
  -Dusb-acl-helper-dir=%{_libexecdir}/spice-gtk-%{_arch}/

%meson_build

%check
%meson_test

%install
%meson_install

# needed because of the upstream issue described in
# http://lists.freedesktop.org/archives/spice-devel/2012-August/010343.html
# these are unwanted spice-protocol files
rm -rf %{buildroot}%{_includedir}/spice-1
rm -rf %{buildroot}%{_datadir}/pkgconfig/spice-protocol.pc

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/spicy-screenshot
%{_bindir}/spicy
%{_bindir}/spicy-stats
%attr(4755, root, root) %{_libexecdir}/spice-gtk-%{_arch}/spice-client-glib-usb-acl-helper
%{_datadir}/polkit-1/actions/org.spice-space.lowlevelusbaccess.policy
%{_mandir}/man1/spice-client.1.*

%files -n %{libglib}
%{_libdir}/libspice-client-glib-%{glibapi}.so.%{glibmajor}
%{_libdir}/libspice-client-glib-%{glibapi}.so.%{glibmajor}.*

%files -n %{glibgir}
%{_libdir}/girepository-1.0/SpiceClientGLib-%{glibapi}.typelib

%files -n %{libgtk3}
%{_libdir}/libspice-client-gtk-%{gtkapi3}.so.%{gtkmajor}
%{_libdir}/libspice-client-gtk-%{gtkapi3}.so.%{gtkmajor}.*

%files -n %{gtkgir3}
%{_libdir}/girepository-1.0/SpiceClientGtk-%{gtkapi3}.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/spice-gtk
%{_includedir}/spice-client-glib-2.0
%{_includedir}/spice-client-gtk-%{gtkapi3}/
%{_libdir}/libspice-client-glib-2.0.so
%{_libdir}/libspice-client-gtk-%{gtkapi3}.so
%{_libdir}/pkgconfig/spice-client-glib-2.0.pc
%{_libdir}/pkgconfig/spice-client-gtk-%{gtkapi3}.pc
%{_datadir}/gir-1.0/SpiceClientGLib-2.0.gir
%{_datadir}/gir-1.0/SpiceClientGtk-%{gtkapi3}.gir
%{_datadir}/vala/vapi/spice-client-glib-%{glibapi}.deps
%{_datadir}/vala/vapi/spice-client-glib-%{glibapi}.vapi
%{_datadir}/vala/vapi/spice-client-gtk-%{gtkapi3}.deps
%{_datadir}/vala/vapi/spice-client-gtk-%{gtkapi3}.vapi
