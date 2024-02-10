LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "rp2040-start.service"

SRC_URI:append = " file://rp2040-start.service"
FILES:${PN} += "${systemd_unitdir}/system/rp2040-start.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/rp2040-start.service ${D}/${systemd_unitdir}/system
}