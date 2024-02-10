# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.16.5] - 2024-01-23

### Roolback

- Rollback SocketXP Agent to v1.3.9

## [1.16.4] - 2024-01-19

### Update

- SocketXP Agent v1.4.4
- Update Hardware-Bridge

## [1.16.3] - 2023-12-26

### Update

- Update SocketXP Agent

## [1.16.2] - 2023-11-16

### Update

- Update docker login credentials

## [1.16.1] - 2023-9-11

### Fix

- added of the patches 6, 7 and 8 files in /patcher/
- added new service named move-files-buried and dependencies to check and move buried files to default folder
- service with automatic execution every 30 minutes
- added logging in the ~/.apps/patches/logs folder, whenever a buried file condition occurs with date and number of files moved
- log overwriting logic when it reaches 1000 lines, avoiding unnecessary space occupation

## [1.16.0] - 2023-8-17

### Added
- Support to Quectell EC25-AU*

## [1.15.0] - 2023-8-10

### Added
- Send board rev to influx db

## [1.14.1] - 2023-07-18

### Fix
- Creation of /media/usb0

## [1.14.0] - 2023-07-10

### Added
- RP2040 services
- Addapt hardware-bridge to edge-crane
- Addapt HD scripts to edge-crane
- Script to reset switch and PoE

### Changed
- SocketXP verification interval
- Hardware-bridge modem informations

## [1.13.0] - 2023-06-15

### Added
- Applied patch indicator to monitoring
- Disable EEE
- Update hardware-bridge to send modem info

### Changed
- Network interface names to cameras0 and eth0
- Upgrade scripts that rename ethernet interfaces

### Removed
- Default disk entry of fstable

## [1.12.0] - 2023-04-27

### Added
- Ability for Hardware-Bridge to restart history and device-monitor containers.
- Initialization of Device-Monitor with sdx parameters (previously only sda).
- Ability for block-device-attach to restart device-monitor container.
- Ability for block-device-checker to stop history container when internal storage is over 95%
- block-device-checker can update kernel partition's table.

### Changed
- block-device-attach change disk partitioning. MBR -> GPT
- Upgrade in log messages of service scripts.

### Fixed
- Fix for block-device-attach script when a disk without partition format is encountered.
- Support for disks > 2T in EXFAT.
- Fixes to mount partitions options.
- Disk integrity verification for ext4 and exfat.
- Close an old instance of block-device-attach.
- Identification of '0451:9261' as a valid HD driver.
- Time limit for running block-device-checker.

## [1.11.0] - 2023-03-06

### Added
- Support for RP2040 microcontroller flash burner
- GPIO management support
- prepare-system-rev service responsible for identifying board revision
- EXFAT partition support
- Block device management services
    - block-device-attach@
    - block-device-change@
    - block-device-detach@
    - block-device-checker
- udev rules for disk management

### Update
- Change of license from Pingu MIT to Proprietary
- Camera-monitor container startup options according to board revision
- Device-monitor container startup options according to board revision

### Removed
- GPIO18 control (modem control) from /boot/config.txt file
- Old block device mounting script (usbdevinserted)
- Removal of ext4 formatting script (format_ext_4)
- Removal of device-attach service and udev rule

## [1.10.0] - 2023-03-01

### Added
- Add a udev rule for the usb-realtech-net device
- Change the initialization of the history container
- Add DWC2 support
- Update the firmware for eth1
- Update modem-checker from v1.0.0 -> v0.2.0
    - Implement logger system
    - Use TTY port defined by the driver
    - Restart Portainer and SocketXP when the device goes online
    - Log modem signal strength
    - Check configuration of modem usbnet
- Update hardware_bridge from v0.1.2 -> v0.1.3
    - Integrate with modem-manager
- Modem Manager update
    - Allow the use of SIM cards from Telecall and Arqia (automatically)

## [1.9.0] - 2023-02-07

### Added
- Modem Checker service
- Quectel Modem Manager