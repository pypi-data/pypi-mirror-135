%define modname glue
%define srcname lscsoft-%{modname}

# -- srpm metadata ----------

Name:     python-%{srcname}
Summary:  The Grid LSC User Environment
Version:  3.0.1
Release:  1%{?dist}
Packager: Duncan Macleod <duncan.macleod@ligo.org>

License:  GPLv2+
Prefix:   %{_prefix}
Source0:  %pypi_source
Url:      https://lscsoft.docs.ligo.org/glue/

# -- requirements -----------

BuildRequires: python-srpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python3-rpm-macros

# build requirements
BuildRequires: gcc
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools

# runtime requirements as buildrequires for help2man
BuildRequires: help2man
BuildRequires: python%{python3_pkgversion}-lal
BuildRequires: python%{python3_pkgversion}-ligo-segments
BuildRequires: python%{python3_pkgversion}-six
BuildRequires: python%{python3_pkgversion}-numpy

# testing requirements
BuildRequires: make
BuildRequires: python%{python3_pkgversion}-ligo-segments
BuildRequires: python%{python3_pkgversion}-matplotlib
BuildRequires: python%{python3_pkgversion}-numpy
BuildRequires: python%{python3_pkgversion}-pyRXP
BuildRequires: python%{python3_pkgversion}-six

%description
Glue (Grid LSC User Environment) is a suite of python modules and programs to
allow users to run LSC codes on the grid.

# -- python3 ----------------

%package -n python%{python3_pkgversion}-%{srcname}
Summary: Python %{python3_version} libraries for the Grid LSC User Environment
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-ligo-segments
Requires: python%{python3_pkgversion}-numpy
Requires: python%{python3_pkgversion}-pyRXP
Requires: python%{python3_pkgversion}-six
Obsoletes: python%{python3_pkgversion}-%{modname} < 2.0.0-5
Provides: python%{python3_pkgversion}-%{modname} = %{version}-%{release}
Obsoletes: python%{python3_pkgversion}-%{modname}-common < 2.0.0-5
Provides: python%{python3_pkgversion}-%{modname}-common = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%description -n python%{python3_pkgversion}-%{srcname}
Glue (Grid LSC User Environment) is a suite of python modules and programs to
allow users to run LSC codes on the grid.
This package provides the Python %{python3_version} library.

# -- command-line -----------

%package -n %{srcname}-utils
Summary: Grid LSC User Environment (GLUE) command-line scripts
Requires: python%{python3_pkgversion}-%{srcname} = %{version}-%{release}
Obsoletes: glue < 2.0.0-5
Obsoletes: python2-glue < 2.0.0-5
%description -n %{srcname}-utils
Glue (Grid LSC User Environment) is a suite of python modules and programs to
allow users to run LSC codes on the grid.
This package provides the command-line interface scripts.

# -- build ------------------

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

# generate man pages with help2man
mkdir -p %{buildroot}%{_mandir}/man1
export PYTHONPATH="%{buildroot}%{python3_sitearch}:%{buildroot}%{python3_sitelib}:${PYTHONPATH}"
ls %{buildroot}%{_bindir}/ | xargs --verbose -I @ \
help2man \
	--output %{buildroot}%{_mandir}/man1/@.1 \
	--no-info \
	--no-discard-stderr \
	--section 1 \
	--source %{srcname} \
	--version-string %{version} \
	%{buildroot}%{_bindir}/@

%check
PYTHONPATH="%{buildroot}%{python3_sitearch}" \
PYTHON=%{__python3} \
make -C test

%clean
rm -rf $RPM_BUILD_ROOT

# -- files ------------------

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitearch}/*

%files -n %{srcname}-utils
%license LICENSE
%doc README.md
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{srcname}

# -- changelog --------------

%changelog
* Sat Jan 22 2022 Robert Bruntz <robert.bruntz@ligo.org> 3.0.1-1
- Removed Python 2 support and lots of unused code, much cleanup of code base

* Fri Sep 11 2020 Ryan Fisher <ryan.fisher@ligo.org> 2.1.0-1
- Test release with deprecations.

* Fri Dec 6 2019 Duncan Macleod <duncan.macleod@ligo.org> 2.0.0-3
- Rename packages according to EPEL naming conventions

* Wed Feb 20 2019 Ryan Fisher <rpfisher@syr.edu>
- Major version update with many changes and removal of segments subpackage.

* Tue Jun 19 2018 Ryan Fisher <rpfisher@syr.edu>
- 1.59.2 removing old M2Crypto import hiding in LDBDWClient.py.

* Thu Jun 7 2018 Ryan Fisher <rpfisher@syr.edu>
- 1.59.1 adding more python 3 package generation.

* Tue Jun 5 2018 Ryan Fisher <rpfisher@syr.edu>
- Pre O-3 release with removal of old codes, more packaging changes, better testing and more Python 3 compatibility.

* Tue Mar 13 2018 Ryan Fisher <rpfisher@syr.edu>
- Pre O-3 release with packaging changes, better testing and more Python 3 compatibility.

* Tue Jun 13 2017 Ryan Fisher <rpfisher@syr.edu>
- Mid O2 release to include M2Crypto removal and Kipp packaging changes.

* Thu Apr 13 2017 Duncan Macleod <duncan.macleod@ligo.org>
- Switched dependency from M2Crypto -> pyOpenSSL.

* Fri Apr 7 2017 Ryan Fisher <ryan.fisher@ligo.org>
- Added install_requires for pip installations.

* Thu Apr 6 2017 Ryan Fisher <ryan.fisher@ligo.org>
- Cleaned up RPM and debian codes.

* Thu Apr 6 2017 Duncan Brown <duncan.brown@ligo.org>
- O2 mid-run updated release. Change sdist name for PyPi compatibility.

* Wed Jan 25 2017 Ryan Fisher <rpfisher@syr.edu>
- O2 mid-run updated release. Updated python 3 compatibility fix from Leo to fix Debian package build for lalsuite.  Various updates from Kipp.

* Wed Oct 19 2016 Ryan Fisher <rpfisher@syr.edu>
- ER10 updated release. Python 3 compatibility from Leo, various updates from Kipp.

* Tue Sep 13 2016 Ryan Fisher <rpfisher@syr.edu>
- ER10 release. (forgot to update this changelog for last several releases)

* Thu Jul 23 2015 Ryan Fisher <rpfisher@syr.edu>
- Pre-ER8 release, attempt 2.

* Wed Jul 22 2015 Ryan Fisher <rpfisher@syr.edu>
- Pre-ER8 release.

* Fri May 22 2015 Ryan Fisher <rpfisher@syr.edu>
- ER7 release.

* Wed Nov 19 2014 Ryan Fisher <rpfisher@syr.edu>
- ER6 pre-release bug fix for dmt files method of ligolw_segment_query.

* Thu Nov 13 2014 Ryan Fisher <rpfisher@syr.edu>
- ER6 pre-release.

* Tue May 6 2014 Ryan Fisher <rpfisher@syr.edu>
- Version update to match git tag.

* Tue May 6 2014 Ryan Fisher <rpfisher@syr.edu>
- Sub-version release to add datafind to debian package.

* Tue Dec 3  2013 Ryan Fisher <rpfisher@syr.edu>
- ER5 release.

* Tue Jul 2 2013 Ryan Fisher <rpfisher@syr.edu>
- ER4 release, matching spec file.

* Tue Jul 2 2013 Ryan Fisher <rpfisher@syr.edu>
- ER4 release.

* Thu Mar 7 2013 Ryan Fisher <rpfisher@syr.edu>
- Post ER3 release of glue for pegasus 4.2 transition, added new RFC Proxy
    support.

* Fri Mar 1 2013 Ryan Fisher <rpfisher@syr.edu>
- Post ER3 release of glue for pegasus 4.2 transition.

* Mon Nov 19 2012 Ryan Fisher <rpfisher@syr.edu>
- New Release of glue for ER3 with updates to ligolw and lal codes.

* Tue Sep 4 2012 Ryan Fisher <rpfisher@syr.edu>
- New Release of glue with upgrades and bugfixes to segment database infrastructure.

* Fri May 18 2012 Ryan Fisher <rpfisher@syr.edu>
- Bugfix release of 1.39 labelled 1.39.2.  Includes fix to ligolw for URL reading, and packaging fixes.

* Fri May 11 2012 Ryan Fisher <rpfisher@syr.edu>
- Bugfix release of 1.39 labelled 1.39.1

* Thu May 10 2012 Ryan Fisher <rpfisher@syr.edu>
- New release of glue to replace Apr 12 near-release.  This includes ligolw changes and updates for job submission over remote pools.

* Thu Apr 12 2012 Ryan Fisher <rpfisher@syr.edu>
- New release of glue with updates to ligolw library, including some bug fixes for ligowl_sqlite and ligolw_print.

* Wed Nov 16 2011 Ryan Fisher <rpfisher@syr.edu>
- New release of glue with glue-segments and glue-common split from glue, lvalerts, lars and gracedb removed.

* Mon Oct 10 2011 Ryan Fisher <rpfisher@syr.edu>
- New release of glue to fix build issues called 1.36.

* Fri Oct 7 2011 Ryan Fisher <rpfisher@syr.edu>
- New release of glue with Kipp's fixes to ligolw_sqlite bugs, Kipp's checksums added, and Peter and my change to the coalescing script for segment databases.

* Thu Sep 29 2011 Ryan Fisher <rpfisher@syr.edu>
- New release of glue with speedup to string to xml conversion and 10 digit gps fixes.

* Wed Sep 15 2010 Peter Couvares <pfcouvar@syr.edu>
- New release of glue with GEO publishing

* Thu Apr 22 2010 Duncan Brown <dabrown@physics.syr.edu>
- Third S6 release of glue

* Wed Nov 11 2009 Duncan Brown <dabrown@physics.syr.edu>
- Second S6 release of glue

* Mon Jul 27 2009 Duncan Brown <dabrown@physics.syr.edu>
- First S6 release of glue

* Wed Jul 01 2009 Duncan Brown <dabrown@physics.syr.edu>
- Pre S6 release of glue

* Wed Jun 24 2009 Duncan Brown <dabrown@physics.syr.edu>
- Post E14 release of glue

* Thu Jun 11 2009 Duncan Brown <dabrown@physics.syr.edu>
- Allow segment tools to see multiple ifos

* Wed Jun 10 2009 Duncan Brown <dabrown@physics.syr.edu>
- Restored LSCdataFindcheck and fixed debian control files

* Tue Jun 09 2009 Duncan Brown <dabrown@physics.syr.edu>
- Build for glue 1.19-1

* Tue Jun 24 2008 Ping Wei <piwei@syr.edu>
- Build for glue 1.18-1

* Thu Jun 19 2008 Duncan Brown <dabrown@physics.syr.edu>
- Build for glue 1.17

* Fri Nov 04 2005 Duncan Brown <dbrown@ligo.caltech.edu>
- Build for glue 1.6

* Tue Aug 23 2005 Duncan Brown <dbrown@ligo.caltech.edu>
- Initial build for glue 1.0
