
%define	iwidgets_version 4.0.1

%define _snap	20080403

Summary:	[incr Tcl] - object-oriented extension of the Tcl language
Summary(pl.UTF-8):	[incr Tcl] - obiektowo zorientowane rozszerzenie języka Tcl
Name:		itcl
Version:	3.3
Release:	2.%{_snap}.0.1
License:	distributable
Group:		Development/Languages/Tcl
#Source0:	http://dl.sourceforge.net/incrtcl/%{name}%{version}.tar.gz
Source0:	%{name}-CVS-%{_snap}.tar.bz2
# Source0-md5:	8ac37bc9a01b25253e193e8b6a53a98d
#Source2:	http://dl.sourceforge.net/incrtcl/iwidgets%{iwidgets_version}.tar.gz
Source2:	iwidgets-CVS-%{_snap}.tar.bz2
# Source2-md5:	7741d7e0b231a4875b0998d6b5c00615
Patch0:		%{name}-iwidgets-config.patch
Patch1:		%{name}-soname.patch
#Patch2:		%{name}-libdir.patch
URL:		http://incrtcl.sourceforge.net/itcl/
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	tcl-devel >= 8.4.6
BuildRequires:	tk-devel >= 8.4.6
Requires:	tcl >= 8.4.6
Requires:	tk >= 8.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	%{_prefix}/lib

%description
[incr Tcl] provides the extra language support needed to build large
Tcl/Tk applications. It introduces the notion of objects, which act as
building blocks for an application. Each object is a bag of data with
a set of procedures or "methods" that are used to manipulate it.
Objects are organized into "classes" with identical characteristics,
and classes can inherit functionality from one another. This
object-oriented paradigm adds another level of organization on top of
the basic variable/procedure elements, and the resulting code is
easier to understand and maintain.

%description -l pl.UTF-8
[incr Tcl] dostarcza dodatkowe wsparcie języka potrzebne przy
tworzeniu dużych aplikacji Tcl/Tk. Wprowadza pojęcie obiektów, które
służą jako bloki do budowania aplikacji. Każdy obiekt jest workiem
danych ze zbiorem procedur lub "metod", które służą do manipulowania
tymi danymi. Obiekty są organizowane w "klasy" o identycznej
charakterystyce, a klasy mogą dziedziczyć funkcjonalność z innych
klas. Ten paradygmat orientacji obiektowej dodaje dodatkowy poziom
zorganizowania do podstawowych elementów zmiennych i procedur, a
wynikający z tego kod jest łatwiejszy do zrozumienia i utrzymania.

%package devel
Summary:	Header files for itcl/itk libraries
Summary(pl.UTF-8):	Pliki nagłówkowe dla itcl/itk libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	tcl-devel >= 8.4.6
Requires:	tk-devel >= 8.4.6

%description devel
Header files for itcl/itk libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla itcl/itk libraries.

%prep
%setup -q -c -a1
%patch0 -p1
%patch1 -p1
#%patch2 -p1

%build
cd itcl
%{__autoconf}
%configure

%{__make} \
	CFLAGS_DEFAULT="%{rpmcflags} -D__NO_STRING_INLINES -D__NO_MATH_INLINES"

cd ../iwidgets
%{__autoconf}
%configure

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-iwidgets-%{iwidgets_version}

%{__make} -C itcl%{version} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C itk%{version} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C iwidgets%{iwidgets_version} install \
	INSTALL="install" \
	MKINSTALLDIRS="install -d" \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	MAN_INSTALL_DIR=$RPM_BUILD_ROOT%{_mandir}/mann

#%if "%{_ulibdir}" != "%{_libdir}"
#mv -f $RPM_BUILD_ROOT%{_libdir}/itcl%{version}/pkgIndex.tcl $RPM_BUILD_ROOT%{_ulibdir}/itcl%{version}
#mv -f $RPM_BUILD_ROOT%{_libdir}/itk%{version}/pkgIndex.tcl $RPM_BUILD_ROOT%{_ulibdir}/itk%{version}
#%endif

install -d iwidgets
cp -f iwidgets%{iwidgets_version}/{CHANGES,ChangeLog,README,license.terms} iwidgets

rm $RPM_BUILD_ROOT%{_ulibdir}/iwidgets
ln -sf %{_ulibdir}/iwidgets%{iwidgets_version} $RPM_BUILD_ROOT%{_ulibdir}/iwidgets

mv $RPM_BUILD_ROOT%{_ulibdir}/iwidgets%{iwidgets_version}/demos/* \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-iwidgets-%{iwidgets_version}

mv -f $RPM_BUILD_ROOT%{_libdir}/itcl%{version}/lib*.so* $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT%{_libdir}/itk%{version}/lib*.so* $RPM_BUILD_ROOT%{_libdir}

cd $RPM_BUILD_ROOT%{_libdir}
ln -sf libitcl*.so.* libitcl%{version}.so
ln -sf libitcl*.so.* libitcl.so
ln -sf libitk*.so.* libitk%{version}.so
ln -sf libitk*.so.* libitk.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc itcl%{version}/{CHANGES,ChangeLog,INCOMPATIBLE,README,TODO,license.terms} iwidgets
%attr(755,root,root) %{_libdir}/lib*.so.*
%{_libdir}/iwidgets
%dir %{_libdir}/itcl*
%dir %{_libdir}/itk*
%dir %{_libdir}/iwidgets%{iwidgets_version}
%{_libdir}/iwidgets%{iwidgets_version}/*.tcl
%{_libdir}/iwidgets%{iwidgets_version}/scripts
%{_libdir}/itcl*/*.tcl
%{_libdir}/itk*/*
%{_mandir}/mann/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/itclConfig.sh
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/itcl*/lib*stub*.a
%{_includedir}/*.h
%{_examplesdir}/%{name}-iwidgets-%{iwidgets_version}
