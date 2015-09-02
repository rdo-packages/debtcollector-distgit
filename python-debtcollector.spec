%{!?_licensedir:%global license %%doc}
%global pypi_name debtcollector

%if 0%{?fedora}
%global with_python3 1
%endif

Name:        python-debtcollector
Version:     0.7.0
Release:     2%{?dist}
Summary:     A collection of Python deprecation patterns and strategies

License:     ASL 2.0
URL:         https://pypi.python.org/pypi/%{pypi_name}
Source0:     https://pypi.python.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

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

Requires:    python-babel
Requires:    python-pbr >= 1.3.0
Requires:    python-six >= 1.9.0
Requires:    python-wrapt

%description -n python2-%{pypi_name}
It is a collection of functions/decorators which is used to signal a user when
*  a method (static method, class method, or regular instance method) or a class
    or function is going to be removed at some point in the future.
* to move a instance method/property/class from an existing one to a new one
* a keyword is renamed
* further customizing the emitted messages

%package -n python2-%{pypi_name}-doc
Summary:        Documentation for the debtcollector module

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-six >= 1.9.0
BuildRequires:  dos2unix

%description -n python2-%{pypi_name}-doc
Documentation for the debtcollector module

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:     A collection of Python deprecation patterns and strategies
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

Requires:    python3-babel
Requires:    python3-pbr
Requires:    python3-six >= 1.9.0
Requires:    python3-wrapt

%description -n python3-%{pypi_name}
It is a collection of functions/decorators which is used to signal a user when
*  a method (static method, class method, or regular instance method) or a class
    or function is going to be removed at some point in the future.
* to move a instance method/property/class from an existing one to a new one
* a keyword is renamed
* further customizing the emitted messages
%endif

%if 0%{?with_python3}
%package -n python3-%{pypi_name}-doc
Summary:        Documentation for the debtcollector module

BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-six >= 1.9.0
BuildRequires:  dos2unix

%description -n python3-%{pypi_name}-doc
Documentation for the debtcollector module
%endif


%prep
%setup -q -n %{pypi_name}-%{version}

# let RPM handle deps
rm -rf requirements.txt

%build
%{__python2} setup.py build
# doc
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%if 0%{?with_python3}
%{__python3} setup.py build
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build-3 -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
dos2unix doc/build/html/_static/jquery.js

%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif

%files -n python2-%{pypi_name}
%doc README.rst CONTRIBUTING.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}*.egg-info

%files -n python2-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.egg-info
%endif

%if 0%{?with_python3}
%files -n python3-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Wed Sep 02 2015 Chandan Kumar <chkumar246@gmail.com> 0.7.0-2
- Added python 2 and python 3 subpackage

* Wed Aug 05 2015 Alan Pevec <alan.pevec@redhat.com> 0.7.0-1
- Update to upstream 0.7.0

* Sun Jun 28 2015 Alan Pevec <alan.pevec@redhat.com> 0.5.0-1
- Update to upstream 0.5.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Chandan Kumar <chkumar246@gmail.com> - 0.3.0-3
- Fixed jquery doc issues

* Wed Mar 25 2015 Chandan Kumar <chkumar246@gmail.com> - 0.3.0-2
- Fixed doc and license macro in spec file

* Tue Mar 10 2015 Chandan Kumar <chkumar246@gmail.com> - 0.3.0-1
- Initial Package
