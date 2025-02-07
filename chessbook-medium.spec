%define	version	0.1
%define release	10

# (Abel)
# 1. This PGN file is originated from crafty site, named gm2600.pgn.
# It is a carefully selected collection of games of grandmasters
# over 2600 ELO points from different openings.
#
# 2. Don't attempt rebuilding if you don't have enough memory, this
# would result in sllllllow rebuilding.
#
# 3. Not noarch, db format depends on endianess of machine
#
# 4. Only sjeng opening book for normal international chess provides
# sjeng-book, for other chess variants this virtual package is NOT provided

# probably I'll build book for phalanx in the future too
%define build_phalanx 0
%define debug_package %{nil}

Summary:	Chess engine opening book
Name:		chessbook-medium
Version:	%{version}
Release:	%{release}
License:	Distributable
Group:		Games/Boards
Source0:	gm2600.pgn.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	sjeng-free
BuildRequires:	pgn-extract
%if %build_phalanx
BuildRequires:	phalanx
%endif

%description
International chess opening book (PGN format, medium size)

%package -n	sjeng-book-normal-medium
Summary:	Sjeng chess engine opening book for normal chess
Group:		Games/Boards
URL:		https://sjeng.sourceforge.net/
Provides:	sjeng-book = 0.1

%description -n	sjeng-book-normal-medium
Sjeng chess engine opening book for international chess (medium size)

%package -n	phalanx-book-medium
Summary:	Phalanx chess engine opening book for normal chess
Group:		Games/Boards
URL:		https://dusan.freeshell.org/phalanx/
Provides:	phalanx-book = 0.1

%description -n	phalanx-book-medium
Phalanx chess engine opening book (medium size)

%prep
#*************************************************************************
#* WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING
#*************************************************************************
#Building this package would not be successful if lmontel logs in. Please
#wait until he logs out before building this RPM, or jobs will be simply
#killed without notice.

%setup -q -c -T
bzip2 -dc %{SOURCE0} > gm2600.pgn

perl -pi -e 's/\r//g' gm2600.pgn
pgn-extract -W -D -s -ogm2600-clean.pgn gm2600.pgn

%build
# === Sjeng ===
# use 1/2 of physical memory for sjeng, should be enough for
# decent machines
mem=`LC_ALL=C free -b | grep '^Mem' | awk '{print $2}' | xargs -i expr {} / 2`

echo -e "book\ngm2600-clean.pgn\n$mem\nquit" | %{_gamesbindir}/sjeng

# === Phalanx ===
# Totally 1562649 positions, multiply it by 36 byte and that's
# the amount of memory needed to sort the buffer in one pass.
# It's not much, so assumes such amount of memory is already
# available.  Otherwise please tune -b option. Using the exact
# number of positions seems to segfault for me, while num+1 is fine.
# DB building time increases exponentially(?) when memory available
# decreses.
#
# Since this file records grandmasters' games, include more
# move to give more variability (50), instead of using the
# default value (80) which includes only better gameplay.
# Only includes common moves would be uninteresting.
%if %build_phalanx
%{_gamesbindir}/phalanx.real bcreate -b 1600000 -g 50 < gm2600-clean.pgn
%endif

%install
rm -rf %{buildroot}
install -D -m 644 nbook.bin %{buildroot}%{_gamesdatadir}/sjeng/nbook-medium.bin
%if %build_phalanx
install -D -m 644 sbook.phalanx %{buildroot}%{_gamesdatadir}/phalanx/sbook-medium.phalanx
%endif

%clean
rm -rf %{buildroot}

%post -n sjeng-book-normal-medium
%{_sbindir}/update-alternatives --install %{_gamesdatadir}/sjeng/nbook.bin \
	nbook.bin %{_gamesdatadir}/sjeng/nbook-medium.bin 20

%preun -n sjeng-book-normal-medium
[ "$1" != 0 ] || %{_sbindir}/update-alternatives --remove nbook.bin \
	%{_gamesdatadir}/sjeng/nbook-medium.bin

%if %build_phalanx
%post -n phalanx-book-medium
%{_sbindir}/update-alternatives --install %{_gamesdatadir}/phalanx/sbook.phalanx \
	sbook.phalanx %{_gamesdatadir}/phalanx/sbook-medium.phalanx 20

%preun -n phalanx-book-medium
[ "$1" != 0 ] || %{_sbindir}/update-alternatives --remove sbook.phalanx \
	%{_gamesdatadir}/phalanx/sbook-medium.phalanx
%endif

%files -n sjeng-book-normal-medium
%defattr(-,root,root)
%{_gamesdatadir}/sjeng/nbook-medium.bin

%if %build_phalanx
%files -n phalanx-book-medium
%defattr(-,root,root)
%{_gamesdatadir}/phalanx/sbook-medium.phalanx
%endif


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-9mdv2011.0
+ Revision: 617023
- the mass rebuild of 2010.0 packages

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 0.1-8mdv2010.0
+ Revision: 424832
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.1-7mdv2009.0
+ Revision: 243878
- rebuild

* Mon Feb 18 2008 Olivier Thauvin <nanardon@mandriva.org> 0.1-5mdv2008.1
+ Revision: 172132
- fix build

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Aug 04 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/04/06 22:24:08 (53031)
- rebuild

* Fri Aug 04 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/04/06 21:55:52 (53021)
Import chessbook-medium

* Thu Aug 25 2005 Abel Cheung <deaddog@mandriva.org> 0.1-2mdk
- Some unfortunate but necessary changes, if anybody want to
  successfully rebuild this package.

* Mon Jul 04 2005 Abel Cheung <deaddog@mandriva.org> 0.1-1mdk
- First Mandriva package

