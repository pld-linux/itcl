Summary:	[incr Tcl] - object-oriented extension of the Tcl language
Summary(pl.UTF-8):	[incr Tcl] - obiektowo zorientowane rozszerzenie języka Tcl
Name:		itcl
%define	vermaj	3.4
Version:	%{vermaj}.3
Release:	1
License:	Tcl (BSD-like)
Group:		Development/Languages/Tcl
Source0:	http://downloads.sourceforge.net/incrtcl/%{name}%{version}.tar.gz
# Source0-md5:	bea70fc6e6a3fb049fdada405161b934
Patch0:		%{name}-soname.patch
URL:		http://incrtcl.sourceforge.net/itcl/
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	tcl-devel >= 8.4.6
Requires:	tcl >= 8.4.6
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
Summary:	Header files for itcl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki itcl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	tcl-devel >= 8.4.6

%description devel
Header files for itcl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki itcl.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1

%build
%{__autoconf}
%configure \
	--libdir=%{_ulibdir}

%{__make} \
	CFLAGS_DEFAULT=

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_ulibdir}/itcl%{vermaj}/libitcl* $RPM_BUILD_ROOT%{_libdir}

libfile=$(basename $RPM_BUILD_ROOT%{_libdir}/libitcl%{vermaj}.so.0.*)
ln -sf $libfile $RPM_BUILD_ROOT%{_libdir}/libitcl%{vermaj}.so.0
ln -sf $libfile $RPM_BUILD_ROOT%{_libdir}/libitcl%{vermaj}.so
ln -sf $libfile $RPM_BUILD_ROOT%{_libdir}/libitcl.so

%{__sed} -i -e 's#-L[^ ]* ##' \
	-e 's#%{_builddir}/%{name}%{version}#%{_libdir}#' \
	-e 's#%{_ulibdir}/itcl%{vermajor}/lib#%{_libdir}/lib#' \
	$RPM_BUILD_ROOT%{_ulibdir}/itclConfig.sh

%{__sed} -i -e 's#%{_ulibdir}#%{_libdir}#' $RPM_BUILD_ROOT%{_ulibdir}/itcl%{vermaj}/pkgIndex.tcl

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc license.terms
%attr(755,root,root) %{_libdir}/libitcl%{vermaj}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libitcl%{vermaj}.so.0
%dir %{_ulibdir}/itcl%{vermaj}
%{_ulibdir}/itcl%{vermaj}/*.tcl
%{_mandir}/mann/body.n*
%{_mandir}/mann/class.n*
%{_mandir}/mann/code.n*
%{_mandir}/mann/configbody.n*
%{_mandir}/mann/delete.n*
%{_mandir}/mann/ensemble.n*
%{_mandir}/mann/find.n*
%{_mandir}/mann/is.n*
%{_mandir}/mann/itcl.n*
%{_mandir}/mann/itclvars.n*
%{_mandir}/mann/local.n*
%{_mandir}/mann/scope.n*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libitcl%{vermaj}.so
%attr(755,root,root) %{_libdir}/libitcl.so
%{_libdir}/libitclstub%{vermaj}.a
%{_ulibdir}/itclConfig.sh
%{_includedir}/itcl*.h
