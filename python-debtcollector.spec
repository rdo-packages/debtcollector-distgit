%global pypi_name debtcollector

%if 0%{?fedora} >=24
%global with_python3 1
%endif

Name:        python-%{pypi_name}
Version:     XXX
Release:     XXX
Summary:     A collection of Python deprecation patterns and strategies

License:     ASL 2.0
URL:         https://pypi.python.org/pypi/%{pypi_name}
Source0:     http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-master.tar.gz

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
# test dependencies
BuildRequires:   python-hacking
BuildRequires:   python-coverage
BuildRequires:   python-subunit
BuildRequires:   python-oslotest
BuildRequires:   python-testrepository
BuildRequires:   python-testscenarios
BuildRequires:   python-testtools
BuildRequires:   python-fixtures

Requires:    python-babel
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
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-six

%description -n python-%{pypi_name}-doc
Documentation for the debtcollector module

%package -n python-%{pypi_name}-tests
Summary:   Test subpackage for the debtcollector module

Requires:  python-%{pypi_name} = %{version}-%{release}
Requires:   python-hacking
Requires:   python-coverage
Requires:   python-subunit
Requires:   python-oslotest
Requires:   python-testrepository
Requires:   python-testscenarios
Requires:   python-testtools
Requires:   python-fixtures

%description -n python-%{pypi_name}-tests
Test subpackage for the debtcollector module

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:     A collection of Python deprecation patterns and strategies
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
# test dependencies
BuildRequires:   python3-hacking
BuildRequires:   python3-coverage
BuildRequires:   python3-subunit
BuildRequires:   python3-oslotest
BuildRequires:   python3-testrepository
BuildRequires:   python3-testscenarios
BuildRequires:   python3-testtools
BuildRequires:   python3-fixtures

Requires:    python3-babel
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
%setup -q -n %{pypi_name}-%{upstream_version}

# let RPM handle deps
rm -rf requirements.txt

%build
%py2_build

# doc
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
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

%check
# FIXME python-fixtures >= 1.3.1 is not available
# Once it is available, remove || to pass the tests
%{__python2} setup.py test ||
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test ||
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

%files -n python-%{pypi_name}-tests
%{python2_sitelib}/%{pypi_name}/tests

%changelog
