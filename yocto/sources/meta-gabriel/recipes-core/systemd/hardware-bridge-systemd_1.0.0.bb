LICENSE = "CLOSED"
inherit systemd

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "hardware-bridge.service"

SRC_URI:append = " file://hardware-bridge.service"
FILES:${PN} += "${systemd_unitdir}/system/hardware-bridge.service"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/hardware-bridge.service ${D}/${systemd_unitdir}/system
}
