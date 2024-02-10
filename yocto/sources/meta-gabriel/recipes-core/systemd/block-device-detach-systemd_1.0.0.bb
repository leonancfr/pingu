LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "block-device-detach@.service"

SRC_URI:append = " file://block-device-detach@.service"
FILES:${PN} += "${systemd_unitdir}/system/block-device-detach@.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/block-device-detach@.service ${D}/${systemd_unitdir}/system
}
