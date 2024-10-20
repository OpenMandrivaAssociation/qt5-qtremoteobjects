%define api %(echo %{version} |cut -d. -f1)
%define major %api
%define beta %{nil}

%define qtremoteobjects %mklibname qt%{api}remoteobjects %{major}
%define qtremoteobjectsd %mklibname qt%{api}remoteobjects -d
%define qtremoteobjects_p_d %mklibname qt%{api}remoteobjects-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtremoteobjects
Version:	5.15.15
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtremoteobjects-everywhere-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtremoteobjects-everywhere-opensource-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
# From KDE
# [currently no patches]
Summary:	Qt Remote Objects library
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		https://www.qt.io
BuildRequires:	qmake5 = %{version}
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	qlalr%{api}
BuildRequires:	qt5-qtqml-private-devel
# For the Provides: generator
BuildRequires:	cmake >= 3.11.0-1

%description
The Qt Remote Objects module provides an easy to use mechanism for sharing
a QObject's API (Properties/Signals/Slots) between processes.

#------------------------------------------------------------------------------
%package -n	%{qtremoteobjects}
Summary:	Qt%{api} Remote Objects Library
Group:		System/Libraries

%description -n %{qtremoteobjects}
Qt%{api} Remote Objects Library.

The Qt Remote Objects module provides an easy to use mechanism for sharing
a QObject's API (Properties/Signals/Slots) between processes.

%files -n	%{qtremoteobjects}
%{_qt5_libdir}/libQt5RemoteObjects.so.%{api}*
%{_qt5_prefix}/qml/QtQml/RemoteObjects
%{_libdir}/qt5/qml/QtRemoteObjects

#------------------------------------------------------------------------------

%package -n	%{qtremoteobjectsd}
Summary:	Devel files needed to build apps based on QtRemoteObjects
Group:		Development/KDE and Qt
Requires:	%{qtremoteobjects} = %version
Requires:	qt5-qtbase-devel = %version

%description -n %{qtremoteobjectsd}
Devel files needed to build apps based on QtRemoteObjects.

%files -n	%{qtremoteobjectsd}
%{_qt5_libdir}/libQt5RemoteObjects.prl
%{_qt5_libdir}/libQt5RepParser.prl
%{_qt5_libdir}/libQt5RemoteObjects.so
%{_qt5_libdir}/pkgconfig/Qt5RemoteObjects.pc
%{_qt5_libdir}/pkgconfig/Qt5RepParser.pc
%{_qt5_includedir}/QtRemoteObjects
%{_qt5_libdir}/cmake/Qt5RemoteObjects
%{_qt5_prefix}/mkspecs/modules/qt_lib_remoteobjects.pri
%{_qt5_exampledir}/remoteobjects
%{_qt5_includedir}/QtRepParser
%{_qt5_prefix}/mkspecs/features/*.pri
%{_qt5_prefix}/mkspecs/features/*.prf
%{_qt5_prefix}/mkspecs/modules/qt_lib_remoteobjects_private.pri
%{_qt5_prefix}/mkspecs/modules/qt_lib_repparser.pri
%{_qt5_prefix}/mkspecs/modules/qt_lib_repparser_private.pri
%{_qt5_prefix}/bin/repc
%{_libdir}/cmake/Qt5RepParser

%prep
%autosetup -n %(echo %qttarballdir|sed -e 's,-opensource,,') -p1
%{_qt5_prefix}/bin/syncqt.pl -version %{version}

%build
%qmake_qt5
%make_build
#------------------------------------------------------------------------------

%install
%make_install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

install -d %{buildroot}/%{_qt5_docdir}
