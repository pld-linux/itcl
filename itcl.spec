%define	iwidgets_version 4.0.1
Summary:	[incr Tcl] - object-oriented extension of the Tcl language
Summary(pl):	[incr Tcl] - obiektowo zorientowane rozszerzenie jêzyka Tcl
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
Patch1:		%{name}-soname.patch
URL:		http://incrtcl.sourceforge.net/itcl/
BuildRequires:	tcl-devel >= 8.0.3
BuildRequires:	tk-devel >= 8.0.3
Requires:	tcl >= 8.0.3
Requires:	tk >= 8.0.3
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
[incr Tcl] dostarcza dodatkowe wsparcie jêzyka potrzebne przy
tworzeniu du¿ych aplikacji Tcl/Tk. Wprowadza pojêcie obiektów, które
s³u¿± jako bloki do budowania aplikacji. Ka¿dy obiekt jest workiem
danych ze zbiorem procedur lub "metod", które s³u¿± do manipulowania
tymi danymi. Obiekty s± organizowane w "klasy" o identycznej
charakterystyce, a klasy mog± dziedziczyæ funkcjonalno¶æ z innych
klas. Ten paradygmat orientacji obiektowej dodaje dodatkowy poziom
zorganizowania do podstawowych elementów zmiennych i procedur, a
wynikaj±cy z tego kod jest ³atwiejszy do zrozumienia i utrzymania.

%package devel
Summary:	Header files for itcl/itk libraries
Summary(pl):	Pliki nag³ówkowe dla itcl/itk libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	tcl-devel >= 8.0.3
Requires:	tk-devel >= 8.0.3

%description devel
Header files for itcl/itk libraries.

%description devel -l pl
Pliki nag³ówkowe dla itcl/itk libraries.

%prep
%setup -qn %{name}%{version} -a1
%patch0 -p1
%patch1 -p1

%build
%configure2_13
%{__make} \
	CFLAGS_DEFAULT="%{rpmcflags} -D__NO_STRING_INLINES -D__NO_MATH_INLINES"

cd iwidgets%{iwidgets_version}
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C iwidgets%{iwidgets_version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	MAN_INSTALL_DIR=$RPM_BUILD_ROOT%{_mandir}/mann

[ -d iwidgets ] || mkdir iwidgets
cp -f iwidgets%{iwidgets_version}/{CHANGES,ChangeLog,README,license.terms} iwidgets

rm $RPM_BUILD_ROOT%{_libdir}/iwidgets
ln -sf %{_libdir}/iwidgets%{iwidgets_version} \
	$RPM_BUILD_ROOT%{_libdir}/iwidgets

cd $RPM_BUILD_ROOT%{_libdir}
ln -sf libitcl3.2.so.*.* libitcl3.2.so
ln -sf libitcl3.2.so.*.* libitcl.so
ln -sf libitk3.2.so.*.* libitk3.2.so
ln -sf libitk3.2.so.*.* libitk.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES ChangeLog INCOMPATIBLE README TODO license.terms iwidgets
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_libdir}/itcl*
%{_libdir}/itk*
%{_libdir}/iwidgets*
%{_mandir}/mann/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*stub*.a
%{_includedir}/*.h
