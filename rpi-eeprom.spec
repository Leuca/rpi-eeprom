# building debug stuff for this package is essentially useless
%global debug_package %{nil}

Name:           {{{ git_dir_name }}}
Version:        {{{ get_verdate }}}
Release:        1%{?dist}
Summary:        Update scripts for Raspberry Pi bootloader

License:        custom, BSD-3
URL:            https://github.com/Leuca/rpi-eeprom
VCS:            {{{ git_dir_vcs }}}

BuildRequires:  systemd-rpm-macros

Requires:       binutils
Requires:       vi
Requires:       vcgencmd
Requires:       (bootloader-2711 or bootloader-2712)
Requires:       flashrom
Provides:       rpi-eeprom-config
Provides:       rpi-eeprom-update
Provides:       rpi-eeprom-digest

Source:         {{{ git_dir_pack }}}

%description
This package contains the scripts needed to update the Raspberry Pi 4 and Raspberry Pi 5 bootloader and VLI USB controller EEPROMs.

%package        -n bootloader-2711
# Require something that is platform exclusive
Requires:       (boot-rpi4-config or uboot-rpi4-config or edk2-rpi4)
Conflicts:      bootloader-2712
Recommends:     %{name}

Summary:        Bootloader binaries for Raspberry Pi 4

%description    -n bootloader-2711
This package contains binaries used to update the Raspberry Pi 4 bootloader and VLI USB controller EEPROMs.

%package        -n bootloader-2712
Requires:       (boot-rpi5-config or uboot-rpi5-config or edk2-rpi5)
Conflicts:      bootloader-2711
Recommends:     %{name}

Summary:        Bootloader binaries for Raspberry Pi 5

%description    -n bootloader-2712
This package contains binaries used to update the Raspberry Pi 5 bootloader

%prep
{{{ git_dir_setup_macro }}}

%build
# Change hint that suggest the use of a tool that is not supported
sed -i 's/Use ${RPI_EEPROM_UPDATE_CONFIG_TOOL} to change the release./Change the release by editing \/etc\/default\/rpi-eeprom-update/g' rpi-eeprom-update
# Change default editor from nano to vi
sed -i 's/nano/vi/g' rpi-eeprom-config
# Customize configuration file
sed -i '/BOOTFS/d' rpi-eeprom-update-default
echo "BOOTFS=/boot/efi" >> rpi-eeprom-update-default

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/config/
mkdir -p %{buildroot}/lib/firmware/raspberrypi/bootloader-2711/backup
mkdir -p %{buildroot}/lib/firmware/raspberrypi/bootloader-2712/backup
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/default
install -m 0700 rpi-eeprom-update %{buildroot}%{_bindir}
install -m 0700 rpi-eeprom-digest %{buildroot}%{_bindir}
install -m 0700 rpi-eeprom-config %{buildroot}%{_bindir}
install -m 0644 rpi-eeprom-update.service %{buildroot}%{_unitdir}
install -m 0700 rpi-eeprom-update-default %{buildroot}%{_sysconfdir}/default/rpi-eeprom-update
cp -r firmware-2711/* %{buildroot}/lib/firmware/raspberrypi/bootloader-2711
cp -r firmware-2712/* %{buildroot}/lib/firmware/raspberrypi/bootloader-2712

%files
%license LICENSE
%doc README.md releases.md firmware-2711/release-notes.md firmware-2712/release-notes.md
%{_bindir}/rpi-eeprom-update
%{_bindir}/rpi-eeprom-digest
%{_bindir}/rpi-eeprom-config
%{_unitdir}/rpi-eeprom-update.service
%config(noreplace) %{_sysconfdir}/default/rpi-eeprom-update

%files      -n bootloader-2711
/lib/firmware/raspberrypi/bootloader-2711
%ghost /lib/firmware/raspberrypi/bootloader-2711/release-notes.md

%files      -n bootloader-2712
/lib/firmware/raspberrypi/bootloader-2712
%ghost /lib/firmware/raspberrypi/bootloader-2712/release-notes.md

# Symlink the new bootloader folders to the legacy folder
%posttrans  -n bootloader-2711
if [ ! -e /lib/firmware/raspberrypi/bootloader ]; then
    ln -s -T bootloader-2711 /lib/firmware/raspberrypi/bootloader
fi

%posttrans  -n bootloader-2712
if [ ! -e /lib/firmware/raspberrypi/bootloader ]; then
    ln -s -T bootloader-2712 /lib/firmware/raspberrypi/bootloader
fi

# Remove bootloader folder symlink if we are uninstalling
# $1 holds how many packages will be left after the transactions
%postun     -n bootloader-2711
if [ $1 -eq 0 ]; then
    unlink /lib/firmware/raspberrypi/bootloader || :
    rm -d /lib/firmware/raspberrypi || :
fi

%postun     -n bootloader-2712
if [ $1 -eq 0 ]; then
    unlink /lib/firmware/raspberrypi/bootloader || :
    rm -d /lib/firmware/raspberrypi || :
fi

%changelog
{{{ git_dir_changelog }}}
