%{!?_licensedir:%global license %%doc}
%global sname debtcollector

Name:        python-debtcollector
Version:     0.3.0
Release:     3%{?dist}
Summary:     A collection of Python deprecation patterns and strategies

License:     ASL 2.0
URL:         https://pypi.python.org/pypi/debtcollector
Source0:     https://pypi.python.org/packages/source/d/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:   noarch

Requires:    python-setuptools
Requires:    python-iso8601
Requires:    python-oslo-utils
Requires:    python-six >= 1.9.0
Requires:    python-wrapt
Requires:    python-netaddr
Requires:    python-oslo-i18n
Requires:    python-netifaces
Requires:    python-babel
Requires:    pytz

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
%setup -q -n %{sname}-%{version}

# Remove bundled egg-info
rm -rf %{sname}.egg-info

# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

rm -rf {test-,}requirements.txt

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
%{python2_sitelib}/%{sname}
%{python2_sitelib}/*.egg-info

%files doc
%doc doc/build/html
%doc LICENSE

%changelog
* Fri Mar 27 2015 Chandan Kumar <chkumar246@gmail.com> - 0.3.0-3
- Fixed jquery doc issues

* Wed Mar 25 2015 Chandan Kumar <chkumar246@gmail.com> - 0.3.0-2
- Fixed doc and license macro in spec file

* Tue Mar 10 2015 Chandan Kumar <chkumar246@gmail.com> - 0.3.0-1
- Initial Package
