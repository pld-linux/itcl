%define	iwidgets_version 4.0.1
Summary:	[incr Tcl] - object-oriented extension of the Tcl language
Summary(pl):	[incr Tcl] - obiektowo zorientowane rozszerzenie j�zyka Tcl
Name:		itcl
Version:	3.2.1
Release:	1
License:	distributable
Group:		Development/Languages/Tcl
Source0:	http://dl.sourceforge.net/incrtcl/%{name}%{version}_src.tgz
# Source0-md5:	44dcc2129232329cacd6c8abebf38403
Source1:	http://dl.sourceforge.net/incrtcl/iwidgets%{iwidgets_version}.tar.gz
# Source1-md5:	0e9c140e81ea6015b56130127c7deb03
Patch0:		%{name}-DESTDIR.patch
URL:		http://incrtcl.sourceforge.net/itcl/
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl
[incr Tcl] dostarcza dodatkowe wsparcie j�zyka potrzebne przy
tworzeniu du�ych aplikacji Tcl/Tk. Wprowadza poj�cie obiekt�w, kt�re
s�u�� jako bloki do budowania aplikacji. Ka�dy obiekt jest workiem
danych ze zbiorem procedur lub "metod", kt�re s�u�� do manipulowania
tymi danymi. Obiekty s� organizowane w "klasy" o identycznej
charakterystyce, a klasy mog� dziedziczy� funkcjonalno�� z innych
klas. Ten paradygmat orientacji obiektowej dodaje dodatkowy poziom
zorganizowania do podstawowych element�w zmiennych i procedur, a
wynikaj�cy z tego kod jest �atwiejszy do zrozumienia i utrzymania.

%prep
%setup -qn %{name}%{version} -a1
%patch0 -p1

%build
%configure2_13
%{__make} \
	CFLAGS_DEFAULT="%{rpmcflags} -D__NO_STRING_INLINES -D__NO_MATH_INLINES"

cd iwidgets%{iwidgets_version}
%configure2_13
%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd iwidgets%{iwidgets_version}
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	MAN_INSTALL_DIR=$RPM_BUILD_ROOT%{_mandir}/mann
cd ..

[ -d iwidgets ] || mkdir iwidgets
cp iwidgets%{iwidgets_version}/{CHANGES,ChangeLog,README,license.terms} iwidgets

rm $RPM_BUILD_ROOT%{_libdir}/iwidgets
ln -sf %{_libdir}/iwidgets%{iwidgets_version} \
	$RPM_BUILD_ROOT%{_libdir}/iwidgets

rm -f $RPM_BUILD_ROOT%{_includedir}/*
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES ChangeLog INCOMPATIBLE README TODO license.terms iwidgets
# FIXME: missing sonames
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_libdir}/itcl*
%{_libdir}/itk*
%{_libdir}/iwidgets*
%{_mandir}/mann/*
