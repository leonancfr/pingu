LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "rp2040-stop.service"

SRC_URI:append = " file://rp2040-stop.service"
FILES:${PN} += "${systemd_unitdir}/system/rp2040-stop.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/rp2040-stop.service ${D}/${systemd_unitdir}/system
}