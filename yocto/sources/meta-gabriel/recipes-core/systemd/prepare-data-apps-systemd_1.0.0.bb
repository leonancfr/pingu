LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "prepare-data-apps.service"

SRC_URI:append = " file://prepare-data-apps.service "
FILES:${PN} += "${systemd_unitdir}/system/prepare-data-apps.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/prepare-data-apps.service ${D}/${systemd_unitdir}/system
}
