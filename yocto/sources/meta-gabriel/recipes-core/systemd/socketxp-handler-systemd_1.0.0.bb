LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "socketxp-handler.service"

SRC_URI:append = " file://socketxp-handler.service"
FILES:${PN} += "${systemd_unitdir}/system/socketxp-handler.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/socketxp-handler.service ${D}/${systemd_unitdir}/system
}
