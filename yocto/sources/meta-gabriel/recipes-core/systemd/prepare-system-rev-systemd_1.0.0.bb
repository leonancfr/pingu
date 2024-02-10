LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "prepare-system-rev.service"

SRC_URI:append = " file://prepare-system-rev.service "
FILES:${PN} += "${systemd_unitdir}/system/prepare-system-rev.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/prepare-system-rev.service ${D}/${systemd_unitdir}/system
}
