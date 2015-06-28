%{!?_licensedir:%global license %%doc}
%global pypi_name debtcollector

Name:        python-debtcollector
Version:     0.3.0
Release:     4%{?dist}
Summary:     A collection of Python deprecation patterns and strategies

License:     ASL 2.0
URL:         https://pypi.python.org/pypi/%{pypi_name}
Source0:     https://pypi.python.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:   noarch

Requires:    python-setuptools
Requires:    python-babel
Requires:    python-oslo-utils
Requires:    python-pbr
Requires:    python-six >= 1.9.0
Requires:    python-wrapt

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr

%description
It is a collection of functions/decorators which is used to signal a user when
*  a method (static method, class method, or regular instance method) or a class
    or function is going to be removed at some point in the future.
* to move a instance method/property/class from an existing one to a new one
* a keyword is renamed
* further customizing the emitted messages

%package doc
Summary:        Documentation for the debtcollector module

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslo-utils
BuildRequires:  python-six >= 1.9.0
BuildRequires:  dos2unix

%description doc
Documentation for the debtcollector module

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


%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
dos2unix doc/build/html/_static/jquery.js

%files
%doc README.rst CONTRIBUTING.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/*.egg-info

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Chandan Kumar <chkumar246@gmail.com> - 0.3.0-3
- Fixed jquery doc issues

* Wed Mar 25 2015 Chandan Kumar <chkumar246@gmail.com> - 0.3.0-2
- Fixed doc and license macro in spec file

* Tue Mar 10 2015 Chandan Kumar <chkumar246@gmail.com> - 0.3.0-1
- Initial Package
