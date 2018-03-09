Name:          opencv
Version:       3.4.5
Release:       1
Summary:       Open Source Computer Vision Library
Group:         Development/Libraries
URL:           http://opencv.org
Source:        %{name}-%{version}.tar.gz
License:       BSD
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
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
OpenCV (Open Source Computer Vision) is a library of programming functions for real time computer vision. 
This package contains static libraries and header files need for development.

%package       doc
Summary:       docs files
Requires:      opencv-devel = %{version}-%{release}
BuildArch:     noarch

%description   doc
This package contains the OpenCV documentation, samples and examples programs.

%package       -n python2-opencv
Summary:       Python2 bindings for apps which use OpenCV
Requires:      opencv%{_isa} = %{version}-%{release}
Requires:      python-numpy
Provides:      %{name}-python = %{version}-%{release}
Provides:      %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes:     %{name}-python < %{version}-%{release}

%description   -n python2-opencv
This package contains Python bindings for the OpenCV library.

%prep
%setup -q -n %{name}-%{version}/opencv

%build
[ -e build ] && rm -rf build
mkdir build
cd build
cmake \
 -DCMAKE_INSTALL_PREFIX=%{_prefix} \
 -DBUILD_TESTS=OFF \
 -DBUILD_PERF_TESTS=OFF \
 -DENABLE_PRECOMPILED_HEADERS=ON \
 -DBUILD_DOCS=ON \
 -DWITH_OPENGL=ON \
 -DWITH_QT=ON \
 -DOPENCV_SKIP_PYTHON_LOADER=ON \
 -DINSTALL_C_EXAMPLES=ON \
 -DINSTALL_PYTHON_EXAMPLES=ON \
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
%{_bindir}/*
%{_libdir}/libopencv_*.so.*
%{_datadir}/OpenCV/haarcascades
%{_datadir}/OpenCV/lbpcascades

%files devel
%defattr(-,root,root)
%{_includedir}/opencv
%{_includedir}/opencv2
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/opencv.pc
%{_datadir}/OpenCV/*.cmake
%{_datadir}/OpenCV/*.supp
%{_datadir}/OpenCV/haarcascades/*
%{_datadir}/OpenCV/lbpcascades/*

%files doc
%{_datadir}/OpenCV/samples
%{_datadir}/OpenCV/doc
%{_datadir}/OpenCV/licenses

%files -n python2-opencv
%{_libdir}/python%{python_version}*/site-packages/cv2.so

%changelog
