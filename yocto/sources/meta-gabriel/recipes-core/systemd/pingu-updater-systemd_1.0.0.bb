LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "pingu-updater.service"

SRC_URI:append = " file://pingu-updater.service"
FILES:${PN} += "${systemd_unitdir}/system/pingu-updater.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/pingu-updater.service ${D}/${systemd_unitdir}/system
}
