%define	iwidgets_version 4.0.1
Summary:	[incr Tcl] - object-oriented extension of the Tcl language
Summary(pl):	[incr Tcl] - obiektowo zorientowane rozszerzenie jêzyka Tcl
Name:		itcl
Version:	3.3
Release:	0.5
License:	distributable
Group:		Development/Languages/Tcl
Source0:	http://dl.sourceforge.net/incrtcl/%{name}%{version}.tar.gz
# Source0-md5:	d958b3d1c52fa5336b5aacc1251b5ce3
Source1:	http://dl.sourceforge.net/incrtcl/itk%{version}.tar.gz
# Source1-md5:	a97c17f3cfa5e377f43073c653c501b5
Source2:	http://dl.sourceforge.net/incrtcl/iwidgets%{iwidgets_version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-soname.patch
Patch2:		%{name}-libdir.patch
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
Requires:	tcl-devel >= 8.4.6
Requires:	tk-devel >= 8.4.6

%description devel
Header files for itcl/itk libraries.

%description devel -l pl
Pliki nag³ówkowe dla itcl/itk libraries.

%prep
%setup -qn %{name}%{version} -a1 -a2
#%patch0 -p1
#patch1 -p1
#patch2 -p1

%build
#cd itcl
#{__autoconf}
#cd ../itk
#{__autoconf}
#cd ..
%{__autoconf}
#cp -f /usr/share/automake/config.* config
%configure
%{__make} \
	CFLAGS_DEFAULT="%{rpmcflags} -D__NO_STRING_INLINES -D__NO_MATH_INLINES"

cd itk%{version}
%{__autoconf}
%configure
%{__make}

#cd ../iwidgets%{iwidgets_version}
#{__autoconf}
#configure
#{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd itk%{version}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#{__make} -C iwidgets%{iwidgets_version} install \
#	INSTALL_ROOT=$RPM_BUILD_ROOT \
#	MAN_INSTALL_DIR=$RPM_BUILD_ROOT%{_mandir}/mann

#%if "%{_ulibdir}" != "%{_libdir}"
#mv -f $RPM_BUILD_ROOT%{_libdir}/itcl3.2/pkgIndex.tcl $RPM_BUILD_ROOT%{_ulibdir}/itcl3.2
#mv -f $RPM_BUILD_ROOT%{_libdir}/itk3.2/pkgIndex.tcl $RPM_BUILD_ROOT%{_ulibdir}/itk3.2
#%endif

#install -d iwidgets
#cp -f iwidgets%{iwidgets_version}/{CHANGES,ChangeLog,README,license.terms} iwidgets

#rm $RPM_BUILD_ROOT%{_ulibdir}/iwidgets
#ln -sf %{_ulibdir}/iwidgets%{iwidgets_version} \
#	$RPM_BUILD_ROOT%{_ulibdir}/iwidgets

#cd $RPM_BUILD_ROOT%{_libdir}
#ln -sf libitcl3.2.so.*.* libitcl3.2.so
#ln -sf libitcl3.2.so.*.* libitcl.so
#ln -sf libitk3.2.so.*.* libitk3.2.so
#ln -sf libitk3.2.so.*.* libitk.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES ChangeLog INCOMPATIBLE README TODO license.terms
%attr(755,root,root) %{_libdir}/itcl3.3/lib*.so
%attr(755,root,root) %{_libdir}/itk3.3/lib*.so
%{_libdir}/itcl*/*
%{_libdir}/itk*/*
#{_libdir}/iwidgets*
%{_mandir}/mann/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*/lib*.so
%attr(644,root,root) %{_libdir}/*/*.tcl
%attr(644,root,root) %{_libdir}/itk3.3/*.itk
#{_libdir}/lib*stub*.a
%{_includedir}/*.h
