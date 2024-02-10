LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "block-device-attach@.service"

SRC_URI:append = " file://block-device-attach@.service"
FILES:${PN} += "${systemd_unitdir}/system/block-device-attach@.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/block-device-attach@.service ${D}/${systemd_unitdir}/system
}
