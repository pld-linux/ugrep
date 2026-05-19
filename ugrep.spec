#
# Conditional build:
%bcond_without	pcre2		# PCRE2 support (Perl regex)
%bcond_without	zlib		# gzip support
%bcond_without	bzip2		# bzip2 support
%bcond_without	xz		# xz/lzma support
%bcond_without	zstd		# zstd support
%bcond_without	lz4		# lz4 support
%bcond_without	brotli		# brotli support
%bcond_without	bzip3		# bzip3 support
%bcond_without	p7zip		# 7zip support

Summary:	Ultra fast grep with interactive TUI
Name:		ugrep
Version:	7.8.2
Release:	1
License:	BSD
Group:		Applications/Text
#Source0Download: https://github.com/Genivia/ugrep/releases
Source0:	https://github.com/Genivia/ugrep/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0bd511ebad9c4c035f909c382c925889
Patch0:		%{name}-no-lib-reach-in.patch
# Patch0-md5:	205c7d1c5203cb5d790cf3961cf8f50a
URL:		https://ugrep.com/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.12
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?with_bzip2:BuildRequires:	bzip2-devel}
%{?with_bzip3:BuildRequires:	bzip3-devel}
%{?with_brotli:BuildRequires:	libbrotli-devel}
%{?with_lz4:BuildRequires:	lz4-devel}
%{?with_pcre2:BuildRequires:	pcre2-8-devel}
%{?with_xz:BuildRequires:	xz-devel}
%{?with_zlib:BuildRequires:	zlib-devel}
%{?with_zstd:BuildRequires:	zstd-devel}
%{?with_p7zip:Suggests:	p7zip}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ugrep is a user-friendly, ultra fast grep replacement with an
interactive TUI, fuzzy search, Boolean query patterns, recursive
search of archives and compressed files, hexdump search, and much
more.

ugrep is compatible with GNU grep and BSD grep: uses POSIX basic and
extended regular expression syntax by default, with common grep
options, plus modern Unicode/UTF-8, PCRE2, and Perl regex support.

%package -n bash-completion-%{name}
Summary:	bash-completion for ugrep
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-%{name}
bash-completion for ugrep.

%package -n fish-completion-%{name}
Summary:	fish-completion for ugrep
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-%{name}
fish-completion for ugrep.

%package -n zsh-completion-%{name}
Summary:	zsh-completion for ugrep
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-%{name}
zsh-completion for ugrep.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_p7zip:--disable-7zip} \
	%{?with_bzip3:--with-bzip3} \
	--with-bash-completion-dir=%{bash_compdir} \
	--with-fish-completion-dir=%{fish_compdir} \
	--with-zsh-completion-dir=%{zsh_compdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md LICENSE.txt README.md
%attr(755,root,root) %{_bindir}/ug
%attr(755,root,root) %{_bindir}/ug+
%attr(755,root,root) %{_bindir}/ugrep
%attr(755,root,root) %{_bindir}/ugrep+
%attr(755,root,root) %{_bindir}/ugrep-indexer
%dir %{_datadir}/ugrep
%{_datadir}/ugrep/patterns
%{_mandir}/man1/ug.1*
%{_mandir}/man1/ugrep.1*
%{_mandir}/man1/ugrep-indexer.1*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/ug
%{bash_compdir}/ug+
%{bash_compdir}/ugrep
%{bash_compdir}/ugrep+
%{bash_compdir}/ugrep-indexer

%files -n fish-completion-%{name}
%defattr(644,root,root,755)
%{fish_compdir}/ug.fish
%{fish_compdir}/ug+.fish
%{fish_compdir}/ugrep.fish
%{fish_compdir}/ugrep+.fish
%{fish_compdir}/ugrep-indexer.fish

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{zsh_compdir}/_ug
%{zsh_compdir}/_ug+
%{zsh_compdir}/_ugrep
%{zsh_compdir}/_ugrep+
%{zsh_compdir}/_ugrep-indexer
