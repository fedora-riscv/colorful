%global repo_name LD25
%global repo_commit 4db365affc9d82ba2d9d84622ec6e7c6ec5152b6
%global shortcommit %(c=%{repo_commit}; echo ${c:0:7})

Name:          colorful
Version:       1.2
Release:       13.20170707.git.%{shortcommit}%{?dist}
Summary:       Side-view shooter game
License:       zlib with acknowledgement

URL:           https://svgames.pl
Source0:       https://github.com/suve/%{repo_name}/archive/%{repo_commit}.tar.gz#/%{repo_name}-%{repo_commit}.tar.gz

Requires:      colorful-data = %{version}-%{release}
Requires:      hicolor-icon-theme

# Needed for compilation
BuildRequires: make, fpc >= 3.0, glibc-devel, SDL-devel, SDL_image-devel, SDL_mixer-devel, mesa-libGL-devel

# Needed to properly build the RPM
BuildRequires: desktop-file-utils, libappstream-glib

# FPC is not available on all architectures
ExclusiveArch:  %{fpc_arches}

%description
Colorful is a simple side-view shooter game, where the protagonist 
travels a maze of caves and corridors in order to collect color artifacts.


%package data
Summary:       Game data for Colorful
BuildArch:     noarch
# BuildRequires: 
# Requires:

%description data
Data files (graphics, maps, sounds) required to play Colorful.


%prep
%setup -q -n %{repo_name}-%{repo_commit}

# According to the readme, these files are only needed when
# building with FPC < 3.0.0 and can otherwise be removed.
rm src/jedi-sdl.inc src/sdl_mixer_bundled.pas

%build 
cd src/
make clean
make package

%install
install -m 755 -d %{buildroot}/%{_bindir}/
install -m 755 -d %{buildroot}/%{_mandir}/man6/
install -m 755 -d %{buildroot}/%{_mandir}/pl/man6/
install -m 755 -d %{buildroot}/%{_datadir}/applications/
install -m 755 -d %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/
install -m 755 -d %{buildroot}/%{_datadir}/appdata/

install -m 755 -p src/%{name} %{buildroot}/%{_bindir}/%{name}

install -m 644 -p pkg/%{name}-english.man  %{buildroot}/%{_mandir}/man6/%{name}.6
install -m 644 -p pkg/%{name}-polish.man   %{buildroot}/%{_mandir}/pl/man6/%{name}.6

desktop-file-install                            \
  --dir=%{buildroot}/%{_datadir}/applications/  \
  pkg/%{name}.desktop

appstream-util validate-relax --nonet pkg/%{name}.appdata.xml
install -m 644 -p pkg/%{name}.appdata.xml %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml

install -m 644 -p pkg/%{name}-32x32.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


# For the -data subpackage
install -m 755 -d %{buildroot}/%{_datadir}/suve/%{name}/
install -m 755 -d %{buildroot}/%{_datadir}/suve/%{name}/gfx/
install -m 755 -d %{buildroot}/%{_datadir}/suve/%{name}/sfx/
install -m 755 -d %{buildroot}/%{_datadir}/suve/%{name}/intro/
install -m 755 -d %{buildroot}/%{_datadir}/suve/%{name}/map/org/
install -m 755 -d %{buildroot}/%{_datadir}/suve/%{name}/map/tut/

cp -a ./gfx/   %{buildroot}/%{_datadir}/suve/%{name}/
cp -a ./sfx/   %{buildroot}/%{_datadir}/suve/%{name}/
cp -a ./intro/ %{buildroot}/%{_datadir}/suve/%{name}/
cp -a ./map/   %{buildroot}/%{_datadir}/suve/%{name}/


# Needed for the icon cache to work correctly
%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
# End of icon cache related stuff


%files
%{_bindir}/%{name}
%{_mandir}/man6/%{name}.6*
%{_mandir}/pl/man6/%{name}.6*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc README.md
%license LICENCE.txt


%files data
%{_datadir}/suve/
%license LICENCE.txt


%changelog
* Sat Jul 08 2017 Artur Iwicki <fedora@svgames.pl> 1.2-13.20170707.git.4db365af
- Update to the most recent upstream snapshot
- Remove the ppc64-fixes patch (issues fixed upstream)
- Remove the "find --exec chmod" call from %%install (issue fixed upstream)
- Remove the bundled-sdl-mixer patch (delete the files in %%prep instead)
- Mark README.md as documentation
- Use the %%{fpc_arches} macro in ExclusiveArch tag
- Add hicolor-icon-theme as dependency

* Sat Jul 08 2017 Artur Iwicki <fedora@svgames.pl> 1.2-12.20170412.git.ee1ca09e
- Modify release number to include snapshot info

* Wed Jun 07 2017 Artur Iwicki <fedora@svgames.pl> 1.2-11
- Rename the SDL_Mixer-removing patch to a more descriptive name
- Add a patch file that addresses build failures on ppc64
- Add an equal-release requirement for the -data package in Requires
- Omit architectures where build fails due to FPC being unavailable
  (done by copy-paste'ing the ExclusiveArch list from fpc.spec)

* Sat May 20 2017 suve <veg@svgames.pl> 1.2-10
- Remove /usr/share/suve/colorful/ from files-list 
  (alredy covered by /usr/share/suve)
- Remove the executable bit from all files in the -data subpackage

* Sat Apr 15 2017 suve <veg@svgames.pl> 1.2-9
- Use the -a option (preserve timestamps & symlinks) instead of -R with cp
- Use the -p option (preserve timestamps) with install
- Fix wrong desktop file install dir (had package name at the end)
- Add an equal-version requirement for the -data package
- Use a patch to avoid using the bundled version of SDL_Mixer
- Add /usr/share/suve to files list (for ownership)

* Fri Apr 14 2017 suve <veg@svgames.pl> 1.2-8
- Validate appstream file during install

* Wed Apr 12 2017 suve <veg@svgames.pl> 1.2-7
- Use fresher upstream commit
- Merge the specs for the main package and -data

* Tue Apr 11 2017 suve <veg@svgames.pl> 1.2-6
- Use desktop-file-validate for the .desktop file
- Add an AppData file
- Add the icon cache scriptlets

* Mon Apr 10 2017 suve <veg@svgames.pl> 1.2-5
- Use the GitHub tarball as Source0
- List the manpage and desktop file as Sources instead of putting them in Patch0
- Reduce amount of stuff put in Patch0
- Add license in the files section 
- Use the binary release from the site in -data Source0
- Only list the main directory in -data files listing

