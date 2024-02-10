LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "block-device-change@.service"

SRC_URI:append = " file://block-device-change@.service"
FILES:${PN} += "${systemd_unitdir}/system/block-device-change@.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/block-device-change@.service ${D}/${systemd_unitdir}/system
}
