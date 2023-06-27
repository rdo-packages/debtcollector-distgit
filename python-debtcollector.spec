%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

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

License:     Apache-2.0
URL:         https://pypi.python.org/pypi/%{pypi_name}
Source0:     https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:   noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires: git-core
BuildRequires: openstack-macros

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:     A collection of Python deprecation patterns and strategies

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros

%description -n python3-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        Documentation for the debtcollector module

%description -n python-%{pypi_name}-doc
Documentation for the debtcollector module
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# doc
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%files -n python3-%{pypi_name}
%doc README.rst CONTRIBUTING.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.dist-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
