# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name debtcollector
%global with_doc 1
%global common_desc \
It is a collection of functions/decorators which is used to signal a user when \
*  a method (static method, class method, or regular instance method) or a class \
    or function is going to be removed at some point in the future. \
* to move a instance method/property/class from an existing one to a new one \
* a keyword is renamed \
* further customizing the emitted messages

Name:        python-%{pypi_name}
Version:     XXX
Release:     XXX
Summary:     A collection of Python deprecation patterns and strategies

License:     ASL 2.0
URL:         https://pypi.python.org/pypi/%{pypi_name}
Source0:     https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:   noarch

BuildRequires: git
BuildRequires: openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{pypi_name}
Summary:     A collection of Python deprecation patterns and strategies
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-pbr

Requires:    python%{pyver}-funcsigs
Requires:    python%{pyver}-pbr
Requires:    python%{pyver}-six
Requires:    python%{pyver}-wrapt

%description -n python%{pyver}-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        Documentation for the debtcollector module

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-wrapt

%description -n python-%{pypi_name}-doc
Documentation for the debtcollector module
%endif


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# let RPM handle deps
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# doc
sphinx-build-%{pyver} -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%files -n python%{pyver}-%{pypi_name}
%doc README.rst CONTRIBUTING.rst
%license LICENSE
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}*.egg-info
%exclude %{pyver_sitelib}/%{pypi_name}/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
