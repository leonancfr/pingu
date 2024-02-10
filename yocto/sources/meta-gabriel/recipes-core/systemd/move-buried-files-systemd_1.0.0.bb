LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "move-buried-files.service"

SRC_URI:append = " file://move-buried-files.service "
FILES:${PN} += "${systemd_unitdir}/system/move-buried-files.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/move-buried-files.service ${D}/${systemd_unitdir}/system
}
