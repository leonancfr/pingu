LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "xdisk.service"

SRC_URI:append = " file://xdisk.service "
FILES:${PN} += "${systemd_unitdir}/system/xdisk.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/xdisk.service ${D}/${systemd_unitdir}/system
}
