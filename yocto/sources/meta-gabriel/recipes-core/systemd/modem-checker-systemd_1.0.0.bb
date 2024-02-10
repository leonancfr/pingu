LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "modem-checker.service"

SRC_URI:append = " file://modem-checker.service"
FILES:${PN} += "${systemd_unitdir}/system/modem-checker.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/modem-checker.service ${D}/${systemd_unitdir}/system
}
