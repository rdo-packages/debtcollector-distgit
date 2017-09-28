%global pypi_name debtcollector

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora} >=24
%global with_python3 1
%endif

Name:        python-%{pypi_name}
Version:     1.17.1
Release:     1%{?dist}
Summary:     A collection of Python deprecation patterns and strategies

License:     ASL 2.0
URL:         https://pypi.python.org/pypi/%{pypi_name}
Source0:     https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:   noarch
%description
It is a collection of functions/decorators which is used to signal a user when
*  a method (static method, class method, or regular instance method) or a class
    or function is going to be removed at some point in the future.
* to move a instance method/property/class from an existing one to a new one
* a keyword is renamed
* further customizing the emitted messages

%package -n python2-%{pypi_name}
Summary:     A collection of Python deprecation patterns and strategies
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: git

Requires:    python-babel
Requires:    python-funcsigs
Requires:    python-pbr
Requires:    python-six
Requires:    python-wrapt


%description -n python2-%{pypi_name}
It is a collection of functions/decorators which is used to signal a user when
*  a method (static method, class method, or regular instance method) or a class
    or function is going to be removed at some point in the future.
* to move a instance method/property/class from an existing one to a new one
* a keyword is renamed
* further customizing the emitted messages

%package -n python-%{pypi_name}-doc
Summary:        Documentation for the debtcollector module

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-wrapt
BuildRequires:  python-fixtures
BuildRequires:  python-six

%description -n python-%{pypi_name}-doc
Documentation for the debtcollector module

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:     A collection of Python deprecation patterns and strategies
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

Requires:    python3-babel
Requires:    python3-funcsigs
Requires:    python3-pbr
Requires:    python3-six
Requires:    python3-wrapt

%description -n python3-%{pypi_name}
It is a collection of functions/decorators which is used to signal a user when
*  a method (static method, class method, or regular instance method) or a class
    or function is going to be removed at some point in the future.
* to move a instance method/property/class from an existing one to a new one
* a keyword is renamed
* further customizing the emitted messages
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# let RPM handle deps
rm -rf requirements.txt

%build
%py2_build

# doc
%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install

%if 0%{?with_python3}
%py3_install
%endif

%files -n python2-%{pypi_name}
%doc README.rst CONTRIBUTING.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}*.egg-info
%exclude %{python2_sitelib}/%{pypi_name}/tests

%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst CONTRIBUTING.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.egg-info
%exclude %{python2_sitelib}/%{pypi_name}/tests
%endif

%changelog
* Thu Sep 28 2017 rdo-trunk <javier.pena@redhat.com> 1.17.1-1
- Update to 1.17.1

* Thu Aug 10 2017 Alfredo Moralejo <amoralej@redhat.com> 1.17.0-1
- Update to 1.17.0

