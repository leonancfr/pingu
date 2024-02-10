LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "update-hostname.service"

SRC_URI:append = " file://update-hostname.service "
FILES:${PN} += "${systemd_unitdir}/system/update-hostname.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/update-hostname.service ${D}/${systemd_unitdir}/system
}
