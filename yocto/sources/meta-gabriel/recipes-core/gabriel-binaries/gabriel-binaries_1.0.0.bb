SUMMARY = "Gabriel Binaries"
LICENSE = "CLOSED"

RDEPENDS:${PN} = "bash libusb1"

SRC_URI = "\
	file://prepare-data-apps \
	file://pingu-updater \
	file://install-edge-crane \
	file://populate-device-info \
	file://update-hostname \
	file://prepare-system-rev \
	file://usb-reset \
	file://socket_xp_handler.py \
	file://hardware-bridge.py	\
	file://modem-checker.py	\
	file://modem-manager.py	\
	file://block-device-attach.sh	\
	file://block-device-checker.sh	\
	file://block-device-change.sh	\
	file://block-device-detach.sh	\
	file://check_eth_usb	\
	file://check_eth_native	\
	file://board-rev-info.sh	\
	file://reset-cameras.sh	\
	file://reset-switch.sh	\
	file://rp2040start.py	\
	file://rp2040stop.py	\
	file://move-buried-files.sh	\
"

S = "${WORKDIR}"

do_install:append() {
	install -d ${D}${base_prefix}/opt/gabriel/bin
	install -m 0755 prepare-data-apps ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 pingu-updater ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 install-edge-crane ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 populate-device-info ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 block-device-attach.sh ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 block-device-change.sh ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 block-device-checker.sh ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 block-device-detach.sh ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 update-hostname ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 prepare-system-rev ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 usb-reset ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 check_eth_usb ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 check_eth_native ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 board-rev-info.sh ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0644 socket_xp_handler.py ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0644 hardware-bridge.py ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0644 modem-checker.py ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0644 modem-manager.py ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 reset-cameras.sh ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 reset-switch.sh ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0644 rp2040start.py ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0644 rp2040stop.py ${D}${base_prefix}/opt/gabriel/bin/
	install -m 0755 move-buried-files.sh ${D}${base_prefix}/opt/gabriel/bin/
}

FILES:${PN} = "\
	${base_prefix}/opt/gabriel/bin/prepare-data-apps \
	${base_prefix}/opt/gabriel/bin/pingu-updater \
	${base_prefix}/opt/gabriel/bin/install-edge-crane \
	${base_prefix}/opt/gabriel/bin/populate-device-info \
	${base_prefix}/opt/gabriel/bin/block-device-attach.sh \
	${base_prefix}/opt/gabriel/bin/block-device-change.sh \
	${base_prefix}/opt/gabriel/bin/block-device-detach.sh \
	${base_prefix}/opt/gabriel/bin/block-device-checker.sh \
	${base_prefix}/opt/gabriel/bin/update-hostname \
	${base_prefix}/opt/gabriel/bin/check_eth_usb \
	${base_prefix}/opt/gabriel/bin/check_eth_native \
	${base_prefix}/opt/gabriel/bin/board-rev-info.sh \
	${base_prefix}/opt/gabriel/bin/prepare-system-rev \
	${base_prefix}/opt/gabriel/bin/usb-reset \
	${base_prefix}/opt/gabriel/bin/socket_xp_handler.py \
	${base_prefix}/opt/gabriel/bin/hardware-bridge.py \
	${base_prefix}/opt/gabriel/bin/modem-checker.py \
	${base_prefix}/opt/gabriel/bin/modem-manager.py \
	${base_prefix}/opt/gabriel/bin/reset-cameras.sh \
	${base_prefix}/opt/gabriel/bin/reset-switch.sh \
	${base_prefix}/opt/gabriel/bin/rp2040start.py \
	${base_prefix}/opt/gabriel/bin/rp2040stop.py \
	${base_prefix}/opt/gabriel/bin/move-buried-files.sh \
"