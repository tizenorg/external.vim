%define vimdir vim73

Summary: The VIM editor
URL:     http://www.vim.org/
Name: vim
Version: 7.3.382
Release: 2
License: Vim
Group: Applications/Editors
Source0: vim-%{version}.tar.bz2
Source4: vimrc
Source5: virc
#Source5: ftp://ftp.vim.org/pub/vim/patches/README.patches
Source11: Changelog.rpm
Source12: vi_help.txt
Source14: spec-template
Source1001: %{name}.manifest

Patch2002: vim-7.0-fixkeys.patch
Patch2003: vim-6.2-specsyntax.patch
Patch2004: vim-7.0-crv.patch

Patch3004: vim-7.0-rclocation.patch
Patch3006: vim-6.4-checkhl.patch
Patch3009: vim-7.0-syncolor.patch
Patch3010: vim-7.0-specedit.patch

BuildRequires: pkgconfig(ncurses)
BuildRequires: libacl-devel autoconf

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package common
Summary: The common files needed by any version of the VIM editor
Group: Applications/Editors
Requires: %{name}-filesystem

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.

%package minimal
Summary: A minimal version of the VIM editor
Group: Applications/Editors
Provides: vi = %{version}-%{release}

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present. NOTE: The online help is only available when the vim-common
package is installed.

%package enhanced
Summary: A version of the VIM editor which includes recent enhancements
Group: Applications/Editors
Requires: vim-common = %{version}-%{release} which
Provides: vim = %{version}-%{release}

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.

%package filesystem
Summary: VIM filesystem layout
Group: Applications/Editors

%Description filesystem
This package provides some directories which are required by other
packages that add vim files, p.e.  additional syntax files or filetypes.


%prep
%setup
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
%patch2002 -p1
%patch2003 -p1
%patch2004 -p1
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

%patch3004 -p1
%patch3006 -p1
%patch3009 -p1
%patch3010 -p1

%build
cp %{SOURCE1001} .
cd src
autoconf

sed -e "s+VIMRCLOC	= \$(VIMLOC)+VIMRCLOC	= /etc+" Makefile > Makefile.tmp
mv -f Makefile.tmp Makefile

export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"

sed -i 's/-l\$with_tlib/-ltinfo -l\$with_tlib/g' configure
sed -i 's/-l\$with_tlib/-ltinfo -l\$with_tlib/g' auto/configure

%configure --prefix=%{_prefix} --with-features=huge --enable-pythoninterp \
 --enable-perlinterp --disable-tclinterp --with-x=no \
 --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
 --enable-cscope --with-modified-by="<bugzilla@meego.com>" \
 --with-compiledby="<bugzilla@meego.com>" \
  --disable-netbeans \
  --disable-selinux \
  --disable-nls \
  --disable-rubyinterp \
  --disable-perlinterp  \
  --disable-pythoninterp 

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim enhanced-vim
make clean

perl -pi -e "s/help.txt/vi_help.txt/"  os_unix.h ex_cmds.c
perl -pi -e "s/\/etc\/vimrc/\/etc\/virc/"  os_unix.h
%configure --prefix=%{_prefix} --with-features=small --with-x=no \
  --enable-multibyte \
  --disable-netbeans \
  --disable-nls \
  --disable-selinux \
  --disable-pythoninterp --disable-perlinterp --disable-tclinterp \
  --enable-gui=no --disable-gpm --exec-prefix=/ \
  --with-compiledby="<bugzilla@meego.com>" \
  --with-modified-by="<bugzilla@meego.com>"

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/bin
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/{after,autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/after/{autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
cp -f %{SOURCE11} .
cp -f %{SOURCE14} $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/template.spec
cp runtime/doc/uganda.txt LICENSE
# Those aren't Linux info files but some binary files for Amiga:
rm -f README*.info


cd src
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=/bin VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
make installgtutorbin  DESTDIR=$RPM_BUILD_ROOT BINDIR=/bin VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
mv $RPM_BUILD_ROOT/bin/xxd $RPM_BUILD_ROOT/%{_bindir}/xxd
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m755 enhanced-vim $RPM_BUILD_ROOT/%{_bindir}/vim

( cd $RPM_BUILD_ROOT
  mv ./bin/vimtutor ./%{_bindir}/vimtutor
  mv ./bin/vim ./bin/vi
  rm -f ./bin/rvim
  ln -sf vi ./bin/ex
  ln -sf vi ./bin/rvi
  ln -sf vi ./bin/rview
  ln -sf vi ./bin/view
  ln -sf vim ./%{_bindir}/ex
  ln -sf vim ./%{_bindir}/rvim
  ln -sf vim ./%{_bindir}/vimdiff
)

# Dependency cleanups
chmod 644 $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/doc/vim2html.pl \
 $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/tools/*.pl \
 $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/tools/vim132
chmod 644 ../runtime/doc/vim2html.pl

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
cat >$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.sh <<EOF
if [ -n "\$BASH_VERSION" -o -n "\$KSH_VERSION" -o -n "\$ZSH_VERSION" ]; then
  [ -x /%{_bindir}/id ] || return
  [ \`/%{_bindir}/id -u\` -le 200 ] && return
  # for bash and zsh, only if no alias is already set
  alias vi >/dev/null 2>&1 || alias vi=vim
fi
EOF
cat >$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.csh <<EOF
[ -x /%{_bindir}/id ] || exit
[ \`/%{_bindir}/id -u\` -gt 200 ] && alias vi vim
EOF
chmod 0644 $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/*
install -p -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/vimrc
install -p -m644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/virc
(cd $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/doc;
 gzip -9 *.txt
 gzip -d help.txt.gz version7.txt.gz sponsor.txt.gz
 cp %{SOURCE12} .
 cat tags | sed -e 's/\t\(.*.txt\)\t/\t\1.gz\t/;s/\thelp.txt.gz\t/\thelp.txt\t/;s/\tversion7.txt.gz\t/\tversion7.txt\t/;s/\tsponsor.txt.gz\t/\tsponsor.txt\t/' > tags.new; mv -f tags.new tags
cat >> tags << EOF
vi_help.txt	vi_help.txt	/*vi_help.txt*
vi-author.txt	vi_help.txt	/*vi-author*
vi-Bram.txt	vi_help.txt	/*vi-Bram*
vi-Moolenaar.txt	vi_help.txt	/*vi-Moolenaar*
vi-credits.txt	vi_help.txt	/*vi-credits*
EOF
LANG=C sort tags > tags.tmp; mv tags.tmp tags
 )
(cd ../runtime; rm -rf doc; ln -svf ../../vim/%{vimdir}/doc docs;) 
rm -f $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/macros/maze/maze*.c
rm -rf $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/tools
rm -rf $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/doc/vim2html.pl
rm -f $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/tutor/tutor.gr.utf-8~

rm -rf %{buildroot}/bin/gvimtutor
rm -rf %{buildroot}%{_bindir}/vimtutor

%remove_docs


%files common
%defattr(-,root,root)
%manifest %{name}.manifest
%config(noreplace) %{_sysconfdir}/vimrc
%doc README* LICENSE
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/vimfiles/template.spec
%{_datadir}/%{name}/%{vimdir}/autoload
%{_datadir}/%{name}/%{vimdir}/colors
%{_datadir}/%{name}/%{vimdir}/compiler
%{_datadir}/%{name}/%{vimdir}/doc
%{_datadir}/%{name}/%{vimdir}/*.vim
%{_datadir}/%{name}/%{vimdir}/ftplugin
%{_datadir}/%{name}/%{vimdir}/indent
#%{_datadir}/%{name}/%{vimdir}/keymap
%{_datadir}/%{name}/%{vimdir}/macros
%{_datadir}/%{name}/%{vimdir}/plugin
%{_datadir}/%{name}/%{vimdir}/print
%{_datadir}/%{name}/%{vimdir}/syntax
%{_datadir}/%{name}/%{vimdir}/tutor
%{_datadir}/%{name}/%{vimdir}/spell
/%{_bindir}/xxd


%files minimal
%defattr(-,root,root)
%manifest %{name}.manifest
%config(noreplace) %{_sysconfdir}/virc
/bin/ex
/bin/vi
/bin/view
/bin/rvi
/bin/rview

%files enhanced
%defattr(-,root,root)
%manifest %{name}.manifest
%{_bindir}/vim
%{_bindir}/rvim
%{_bindir}/vimdiff
%{_bindir}/ex
%config(noreplace) %{_sysconfdir}/profile.d/vim.*

%files filesystem
%defattr(-,root,root)
%manifest %{name}.manifest
%dir %{_datadir}/%{name}/vimfiles
%dir %{_datadir}/%{name}/vimfiles/after
%dir %{_datadir}/%{name}/vimfiles/after/*
%dir %{_datadir}/%{name}/vimfiles/autoload
%dir %{_datadir}/%{name}/vimfiles/colors
%dir %{_datadir}/%{name}/vimfiles/compiler
%dir %{_datadir}/%{name}/vimfiles/doc
%dir %{_datadir}/%{name}/vimfiles/ftdetect
%dir %{_datadir}/%{name}/vimfiles/ftplugin
%dir %{_datadir}/%{name}/vimfiles/indent
#%dir %{_datadir}/%{name}/vimfiles/keymap
%dir %{_datadir}/%{name}/vimfiles/lang
%dir %{_datadir}/%{name}/vimfiles/plugin
%dir %{_datadir}/%{name}/vimfiles/print
%dir %{_datadir}/%{name}/vimfiles/spell
%dir %{_datadir}/%{name}/vimfiles/syntax
%dir %{_datadir}/%{name}/vimfiles/tutor

