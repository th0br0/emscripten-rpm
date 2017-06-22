# We need to install it all in its own prefix.
%define _prefix /usr/lib/emscripten
Name: emscripten-fastcomp
Version: 1.37.15
Release: 1%{?dist}
Summary: The clang+llvm backend for Emscripten

License: NCSA
URL: https://github.com/kripken/emscripten-fastcomp

#Source0: https://github.com/kripken/%{name}/archive/%{version}.tar.gz
Source0: %{name}-%{version}/%{name}-%{version}.tar.gz
#Source1: https://github.com/kripken/%{name}-clang/archive/%{version}.tar.gz
Source1: %{name}-%{version}/%{name}-clang-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  zlib-devel
BuildRequires:  libffi-devel
BuildRequires:  ncurses-devel
BuildRequires:  libxml2-devel


%description
emscripten-fastcomp is the clang+llvm backend for Emscripten to
compile C/C++ code into asm.js.

This is a fork of clang and llvm specific to Emscripten.

%package devel
Summary: Development header files for emscripten-fastcomp.
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development header files for emscripten-fastcomp clang+llvm.

%prep
%setup -q -n %{name}-%{version}/%{name}-clang-%{version} -D -b 1
%setup -q -n %{name}-%{version}/%{name}-%{version} -b 0
mv ../%{name}-%{version}/%{name}-clang-%{version} tools/clang

%build
mkdir -p _build
cd _build

cmake .. \
       -DCMAKE_BUILD_TYPE=Release \
       -DLLVM_TARGETS_TO_BUILD="X86;JSBackend" \
       -DLLVM_INCLUDE_EXAMPLES=OFF \
       -DLLVM_INCLUDE_TESTS=OFF \
%if 0%{?__isa_bits} == 64
       -DLLVM_LIBDIR_SUFFIX=64 \
%else
       -DLLVM_LIBDIR_SUFFIX= \
%endif
       -DCLANG_INCLUDE_EXAMPLES=OFF \
       -DCLANG_INCLUDE_TESTS=OFF \
       -DCLANG_ENABLE_ARCMT:BOOL=OFF \
       -DCLANG_ENABLE_STATIC_ANALYZER:BOOL=OFF \
       -DBUILD_SHARED_LIBS:BOOL=OFF \
       -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DINCLUDE_INSTALL_DIR:PATH=%{_prefix}/include -DLIB_INSTALL_DIR:PATH=%{_prefix}/lib64 -DSYSCONF_INSTALL_DIR:PATH=/etc -DSHARE_INSTALL_PREFIX:PATH=%{_prefix}/share -DLIB_SUFFIX=

make %{?_smp_mflags}

%install
cd _build
make install DESTDIR=%{buildroot}

# from clang.spec
# remove editor integrations (bbedit, sublime, emacs, vim)
rm -vf %{buildroot}%{_datadir}/clang/clang-format-bbedit.applescript
rm -vf %{buildroot}%{_datadir}/clang/clang-format-sublime.py*
rm -vf %{buildroot}%{_datadir}/clang/clang-format.el
rm -vf %{buildroot}%{_datadir}/clang/clang-format.py*
# remove diff reformatter
rm -vf %{buildroot}%{_datadir}/clang/clang-format-diff.py*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/*
%{_libdir}/BugpointPasses.so
%{_libdir}/LLVMHello.so
%{_libdir}/libLTO.so
%{_libdir}/*.so.*

%files devel
%{_includedir}/clang/
%{_includedir}/clang-c/
%{_libdir}/cmake/
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/clang/
%{_includedir}/llvm
%{_includedir}/llvm-c


%changelog
* Thu Jun 22 2017 Andreas C. Osowski <andreas@osowski.de> 1.37.15-1
- 

* Thu Jun 22 2017 Andreas C. Osowski <th0br0@mkdir.name> - 1.37.15-1
* Updated version to 1.37.15

* Wed Feb  1 2017 Hubert Figuiere <hub@figuiere.net> - 1.37.2-2
- Move %{_libdir}/clang/ to the -devel package.

* Wed Feb  1 2017 Hubert Figuiere <hub@figuiere.net> - 1.37.2-1
- Initial release for Fedora.
