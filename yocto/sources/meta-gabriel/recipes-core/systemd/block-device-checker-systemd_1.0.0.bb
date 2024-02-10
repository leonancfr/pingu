LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "block-device-checker.service"

SRC_URI:append = " file://block-device-checker.service"
FILES:${PN} += "${systemd_unitdir}/system/block-device-checker.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/block-device-checker.service ${D}/${systemd_unitdir}/system
}
