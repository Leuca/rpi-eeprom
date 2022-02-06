Name:       {{{ git_dir_name }}}
Version:    {{{ git_dir_version }}}
Release:    %{?dist}
Summary:    This is a test package.

License:    custom, BSD-3
URL:        https://github.com/Leuca/rpi-eeprom
VCS:        {{{ git_dir_vcs }}}

Requires:   binutils

Source:     {{{ git_dir_pack }}}

%description
This package contains scripts and binaries used to update the Raspberry Pi 4 bootloader and VLI USB controller EEPROMs.

%prep
{{{ git_dir_setup_macro }}}

%build
# Remove hint that suggest the use of a tool that is not supported
sed -i 's/Use ${RPI_EEPROM_UPDATE_CONFIG_TOOL} to change the release.//g' rpi-eeprom-update
# Change default editor from nano to vi
sed -i 's/nano/vi/g' rpi-eeprom-config
# Set BOOTFS to /boot/efi because with default Redhat system configuration that is the path where the FAT partition will be mounted on
sed -i 's/BOOTFS=\/boot/BOOTFS=\/boot\/efi/g' rpi-eeprom-update
# save configuration in a macro for later
%global default_config %(cat rpi-eeprom-update-default)

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/etc/config/
mkdir -p %{buildroot}/lib/firmware/raspberrypi/bootloader/backup
install -m 700 rpi-eeprom-update %{buildroot}/%{_bindir}
install -m 700 rpi-eeprom-digest %{buildroot}/%{_bindir}
install -m 700 rpi-eeprom-config %{buildroot}/%{_bindir}
cp -r firmware/* %{buildroot}/lib/firmware/raspberrypi/bootloader

%files
%license LICENSE
%{_bindir}/rpi-eeprom-update
%{_bindir}/rpi-eeprom-digest
%{_bindir}/rpi-eeprom-config
/lib/firmware/raspberrypi/*

# It is best to create the config with a script. This way the file should not be deleted if the package is uninstalled
%post
if [ -f /etc/default/rpi-eeprom-config ]; then
else
    echo "%default_config" > /etc/default/rpi-eeprom-config
fi

%changelog
{{{ git_dir_changelog }}}
