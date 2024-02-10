LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "disable-eee.service"

SRC_URI:append = " file://disable-eee.service "
FILES:${PN} += "${systemd_unitdir}/system/disable-eee.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/disable-eee.service ${D}/${systemd_unitdir}/system
}
