Summary:	[incr Tcl]
Name:		itcl
Version:	3.2.1
Release:	1
License:	distributable
Group:		Development/Languages/Tcl
Source0:	http://dl.sourceforge.net/%{name}/%{name}%{version}_src.tgz
# Source0-md5:	358bc16e8fd5a335dbf2e855426885d2
Patch0:		%{name}-DESTDIR.patch
URL:		http://incrtcl.sourceforge.net/itcl/
BuildRequires:	tcl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
[incr Tcl] provides the extra language support needed to build large Tcl/Tk
applications. It introduces the notion of objects, which act as building blocks
for an application. Each object is a bag of data with a set of procedures or
"methods" that are used to manipulate it. Objects are organized into "classes"
with identical characteristics, and classes can inherit functionality from one
another. This object-oriented paradigm adds another level of organization on
top of the basic variable/procedure elements, and the resulting code is easier
to understand and maintain.

%prep
%setup -qn %{name}%{version}
%patch0 -p1

%build
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR="$RPM_BUILD_ROOT"

rm -f $RPM_BUILD_ROOT%{_includedir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES ChangeLog INCOMPATIBLE README TODO
%{_libdir}/*
%{_mandir}/mann/*
