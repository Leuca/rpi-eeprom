Name:       {{{ git_dir_name }}}
Version:    {{{ git_dir_version }}}
Release:    %{?dist}
Summary:    This is a test package.

License:    custom, BSD-3
URL:        https://github.com/Leuca/rpi-eeprom
VCS:        {{{ git_dir_vcs }}}

Source:     {{{ git_dir_pack }}}

%description
This package contains scripts and binaries used to update the Raspberry Pi 4 bootloader and VLI USB controller EEPROMs.

%prep
{{{ git_dir_setup_macro }}}

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/etc/config/
mkdir -p %{buildroot}/lib/firmware/raspberrypi/bootloader/backup
install -m 700 rpi-eeprom-update-default %{buildroot}/etc/config/
mv %{buildroot}/etc/config/rpi-eeprom-update-default %{buildroot}/etc/config/rpi-eeprom-update
install -m 700 rpi-eeprom-update %{buildroot}/%{_bindir}
install -m 700 rpi-eeprom-digest %{buildroot}/%{_bindir}
install -m 700 rpi-eeprom-config %{buildroot}/%{_bindir}
cp -r firmware/* %{buildroot}/lib/firmware/raspberrypi/bootloader

%files
%license LICENSE
%{_bindir}/rpi-eeprom-update
%{_bindir}/rpi-eeprom-digest
%{_bindir}/rpi-eeprom-config
/etc/config/rpi-eeprom-update
/lib/firmware/raspberrypi/*

%changelog
{{{ git_dir_changelog }}}
