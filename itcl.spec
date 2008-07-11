# TODO: libitclstub*.a should exist in %{_libdir} not %{_ulibdir}

%define	iwidgets_version 4.0.2

%define _snap	20080403

Summary:	[incr Tcl] - object-oriented extension of the Tcl language
Summary(pl.UTF-8):	[incr Tcl] - obiektowo zorientowane rozszerzenie języka Tcl
Name:		itcl
Version:	3.4
Release:	0.%{_snap}.2
License:	distributable
Group:		Development/Languages/Tcl
#Source0:	http://dl.sourceforge.net/incrtcl/%{name}%{version}.tar.gz
Source0:	%{name}-CVS-%{_snap}.tar.bz2
# Source0-md5:	8ac37bc9a01b25253e193e8b6a53a98d
#Source1:	http://dl.sourceforge.net/incrtcl/iwidgets%{iwidgets_version}.tar.gz
Source1:	iwidgets-CVS-%{_snap}.tar.bz2
# Source1-md5:	7741d7e0b231a4875b0998d6b5c00615
Patch0:		%{name}-soname.patch
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
%patch0 -p0

ln -s incrTcl/itcl itcl
ln -s incrTcl/itk itk

%build
cd incrTcl
%{__autoconf}
%configure \
	--libdir=%{_ulibdir}

%{__make} \
	CFLAGS_DEFAULT="%{rpmcflags} -D__NO_STRING_INLINES -D__NO_MATH_INLINES"

cd ../iwidgets
%{__autoconf}
%configure \
	--libdir=%{_ulibdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-iwidgets-%{iwidgets_version}

%{__make} -C incrTcl install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C iwidgets install \
	DESTDIR=$RPM_BUILD_ROOT

install -d iwidgets-docs
cp -f iwidgets/{CHANGES,ChangeLog,README,license.terms} iwidgets-docs

ln -sf %{_ulibdir}/iwidgets%{iwidgets_version} $RPM_BUILD_ROOT%{_ulibdir}/iwidgets

mv $RPM_BUILD_ROOT%{_ulibdir}/iwidgets%{iwidgets_version}/demos/* \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-iwidgets-%{iwidgets_version}

mv -f $RPM_BUILD_ROOT%{_ulibdir}/itcl%{version}/lib*.so* $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT%{_ulibdir}/itk%{version}/lib*.so* $RPM_BUILD_ROOT%{_libdir}

cd $RPM_BUILD_ROOT%{_libdir}
ln -sf libitcl*.so.*.* libitcl%{version}.so.0
ln -sf libitcl*.so.*.* libitcl%{version}.so
ln -sf libitcl*.so.*.* libitcl.so
ln -sf libitk*.so.*.* libitk%{version}.so.0
ln -sf libitk*.so.*.* libitk%{version}.so
ln -sf libitk*.so.*.* libitk.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc incrTcl/{CHANGES,ChangeLog,INCOMPATIBLE,README,TODO,license.terms} iwidgets-docs
%attr(755,root,root) %{_libdir}/libitcl%{version}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libitcl%{version}.so.0
%attr(755,root,root) %{_libdir}/libitk%{version}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libitk%{version}.so.0
%dir %{_ulibdir}/itcl%{version}
%{_ulibdir}/itcl%{version}/*.tcl
%dir %{_ulibdir}/itk%{version}
%{_ulibdir}/itk%{version}/*.itk
%{_ulibdir}/itk%{version}/*.tcl
%{_ulibdir}/itk%{version}/tclIndex
%{_ulibdir}/iwidgets
%dir %{_ulibdir}/iwidgets%{iwidgets_version}
%{_ulibdir}/iwidgets%{iwidgets_version}/*.tcl
%{_ulibdir}/iwidgets%{iwidgets_version}/scripts
%{_mandir}/mann/*.n*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libitcl%{version}.so
%attr(755,root,root) %{_libdir}/libitcl.so
%attr(755,root,root) %{_libdir}/libitk%{version}.so
%attr(755,root,root) %{_libdir}/libitk.so
%{_ulibdir}/itclConfig.sh
%{_ulibdir}/itcl%{version}/libitclstub%{version}.a
%{_includedir}/itcl*.h
%{_includedir}/itk*.h
%{_examplesdir}/%{name}-iwidgets-%{iwidgets_version}
