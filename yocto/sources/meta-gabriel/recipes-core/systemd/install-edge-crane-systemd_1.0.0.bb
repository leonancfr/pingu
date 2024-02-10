LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "install-edge-crane.service"

SRC_URI:append = " file://install-edge-crane.service "
FILES:${PN} += "${systemd_unitdir}/system/install-edge-crane.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/install-edge-crane.service ${D}/${systemd_unitdir}/system
}
