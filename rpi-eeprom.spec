# building debug stuff for this package is essentially useless
%global debug_package %{nil}

Name:           {{{ git_dir_name }}}
Version:        {{{ git_dir_version lead=0.0 follow=0 }}}
Release:        3%{?dist}
Summary:        This is a test package.

License:        custom, BSD-3
URL:            https://github.com/Leuca/rpi-eeprom
VCS:            {{{ git_dir_vcs }}}

BuildRequires:  systemd-rpm-macros

Requires:       binutils
Requires:       vi
Requires:       rpi-userland
Provides:       rpi-eeprom-config
Provides:       rpi-eeprom-update
Provides:       rpi-eeprom-digest

Source:         {{{ git_dir_pack }}}

%description
This package contains scripts and binaries used to update the Raspberry Pi 4 bootloader and VLI USB controller EEPROMs.

%prep
{{{ git_dir_setup_macro }}}

%build
# Change hint that suggest the use of a tool that is not supported
sed -i 's/Use ${RPI_EEPROM_UPDATE_CONFIG_TOOL} to change the release./Change the release by editing \/etc\/default\/rpi-eeprom-update/g' rpi-eeprom-update
# Change default editor from nano to vi
sed -i 's/nano/vi/g' rpi-eeprom-config
# Create the configuration file
echo "FIRMWARE_ROOT=/lib/firmware/raspberrypi/bootloader
FIRMWARE_RELEASE_STATUS=\"critical\"
FIRMWARE_IMAGE_DIR=\"\${FIRMWARE_ROOT}/\${FIRMWARE_RELEASE_STATUS}\"
FIRMWARE_BACKUP_DIR=\"/var/lib/raspberrypi/bootloader/backup\"
BOOTFS=/boot/efi
USE_FLASHROM=0
EEPROM_CONFIG_HOOK=" > rpi-eeprom-update.conf

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/config/
mkdir -p %{buildroot}/lib/firmware/raspberrypi/bootloader/backup
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/default
install -m 0700 rpi-eeprom-update %{buildroot}%{_bindir}
install -m 0700 rpi-eeprom-digest %{buildroot}%{_bindir}
install -m 0700 rpi-eeprom-config %{buildroot}%{_bindir}
install -m 0644 rpi-eeprom-update.service %{buildroot}%{_unitdir}
install -m 0700 rpi-eeprom-update.conf %{buildroot}%{_sysconfdir}/default/rpi-eeprom-update
cp -r firmware/* %{buildroot}/lib/firmware/raspberrypi/bootloader

%files
%license LICENSE
%doc README.md releases.md firmware/release-notes.md
%{_bindir}/rpi-eeprom-update
%{_bindir}/rpi-eeprom-digest
%{_bindir}/rpi-eeprom-config
%{_unitdir}/rpi-eeprom-update.service
%config(noreplace) %{_sysconfdir}/default/rpi-eeprom-update
/lib/firmware/raspberrypi
/lib/firmware/raspberrypi/*

%changelog
{{{ git_dir_changelog }}}
