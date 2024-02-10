LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "modem-manager.service"

SRC_URI:append = " file://modem-manager.service"
FILES:${PN} += "${systemd_unitdir}/system/modem-manager.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/modem-manager.service ${D}/${systemd_unitdir}/system
}
