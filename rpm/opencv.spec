Name:          opencv
Version:       4.0.1
Release:       1
Summary:       Open Source Computer Vision Library
Group:         Development/Libraries
URL:           http://opencv.org
Source:        %{name}-%{version}.tar.gz
Patch0:        opencv-4.0.1-sailfish-build-fix.patch
License:       BSD-3-Clause
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-app-1.0)
BuildRequires: pkgconfig(gstreamer-pbutils-1.0)
BuildRequires: pkgconfig(gstreamer-riff-1.0)
BuildRequires: pkgconfig(gstreamer-video-1.0)
BuildRequires: libjpeg-devel
BuildRequires: libogg-devel
BuildRequires: libpng-devel
BuildRequires: libtheora-devel
BuildRequires: libtiff-devel
BuildRequires: libvorbis-devel
BuildRequires: libxml2-devel
BuildRequires: protobuf-devel
BuildRequires: python2-devel
BuildRequires: python3-devel
BuildRequires: python-numpy-devel
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Concurrent)
BuildRequires: pkgconfig(Qt5OpenGL)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: zlib-devel

%description
OpenCV (Open Source Computer Vision) is a library of programming functions for real time computer vision.

%package devel
Summary:       Devel package for %{name}
License:       BSD-3-Clause
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
OpenCV (Open Source Computer Vision) is a library of programming functions for real time computer vision. 
This package contains static libraries and header files need for development.

%package       doc
Summary:       docs files
License:       BSD-3-Clause
Requires:      opencv-devel = %{version}-%{release}
BuildArch:     noarch

%description   doc
This package contains the OpenCV documentation, samples and examples programs.

%package       -n python2-opencv
Summary:       Python2 bindings for apps which use OpenCV
License:       BSD-3-Clause
Requires:      opencv%{_isa} = %{version}-%{release}
Requires:      python-numpy
Provides:      %{name}-python = %{version}-%{release}
Provides:      %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes:     %{name}-python < %{version}-%{release}

%description   -n python2-opencv
This package contains Python bindings for the OpenCV library.

%prep
%setup -q -n %{name}-%{version}/opencv
%patch0 -p1

%build
[ -e build ] && rm -rf build
mkdir build
cd build
cmake \
 -DBUILD_DOCS=ON \
 -DBUILD_PERF_TESTS=OFF \
 -DBUILD_TESTS=OFF \
 -DCMAKE_INSTALL_PREFIX=%{_prefix} \
 -DINSTALL_C_EXAMPLES=ON \
 -DINSTALL_PYTHON_EXAMPLES=ON \
 -DOPENCV_GENERATE_PKGCONFIG=ON \
 -DWITH_ADE=OFF \
 -DWITH_OPENGL=ON \
 -DWITH_QT=ON \
 ..
make gen_opencv_python_source
make %{?_smp_mflags}

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
cd build
make install DESTDIR=%{buildroot}

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/opencv_*
%{_bindir}/setup_vars_opencv4.sh
%{_libdir}/libopencv_*.so.*
%{_datadir}/opencv4/haarcascades
%{_datadir}/opencv4/lbpcascades

%files devel
%defattr(-,root,root)
%{_includedir}/opencv4/opencv2
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/opencv4/*.cmake
%{_datadir}/opencv4/*.supp
%{_datadir}/opencv4/haarcascades/*
%{_datadir}/opencv4/lbpcascades/*

%files doc
%{_datadir}/opencv4/samples
%{_datadir}/doc/opencv4
%{_datadir}/licenses/opencv4

%files -n python2-opencv
%{_libdir}/python%{python_version}*/site-packages/cv2/*

%changelog
