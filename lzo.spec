Name:           lzo
Version:        2.10
Release:        1
Summary:        a real-time data compression library
License:        GPLv2+
URL:            http://www.oberhumer.com/opensource/lzo/
Source0:        http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  zlib-devel

%description
LZO is a data compression library which is suitable for data
de-/compression in real-time. This means it favours speed
over compression ratio.

%package minilzo
Summary:        miniLZO is a very lightweight subset of the LZO library.
Group:          System Environment/Libraries

%description minilzo
miniLZO is a very lightweight subset of the LZO library intended for
easy inclusion with your application. It is generated automatically
from the LZO source code and contains the most important LZO functions.


%package devel
Summary:        Development files for the lzo library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-minilzo = %{version}-%{release}
Requires:       zlib-devel

%description devel
LZO is a data compression library which is suitable for data
de-/compression in real-time. This means it favours speed
over compression ratio.

%package_help

%prep
%setup -q

%build
%configure --disable-dependency-tracking --disable-static --enable-shared
%make_build

gcc %{optflags} -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
gcc -g -shared -Wl,-z,now -o libminilzo.so.0 -Wl,-soname,libminilzo.so.0 minilzo/minilzo.o

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
%delete_la 
install -m 755 libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}
install -p -m 644 minilzo/minilzo.h $RPM_BUILD_ROOT%{_includedir}/lzo
ln -s libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}/libminilzo.so

%check
make check test

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post minilzo -p /sbin/ldconfig

%postun minilzo -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS THANKS NEWS
%{_libdir}/liblzo2.so.*

%files minilzo
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc minilzo/README.LZO
%{_libdir}/libminilzo.so.*

%files devel
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{_includedir}/lzo
%{_libdir}/libminilzo.so
%{_libdir}/liblzo2.so
%{_libdir}/pkgconfig/lzo2.pc

%files help
%{_pkgdocdir}

%changelog
* Tue Aug 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.10-1
- Package init
