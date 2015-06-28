%{!?_licensedir:%global license %%doc}
%global pypi_name debtcollector

Name:        python-debtcollector
Version:     XXX
Release:     XXX
Summary:     A collection of Python deprecation patterns and strategies

License:     ASL 2.0
URL:         https://pypi.python.org/pypi/%{pypi_name}
Source0:     http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-master.tar.gz

BuildArch:   noarch

Requires:    python-setuptools
Requires:    python-babel
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
BuildRequires:  python-six >= 1.9.0
BuildRequires:  dos2unix

%description doc
Documentation for the debtcollector module

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

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
