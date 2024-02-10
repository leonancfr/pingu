SUMMARY = "Additional udev rules"
LICENSE = "CLOSED"

SRC_URI = "\
  file://70-persistent-net.rules \
  file://50-usb-realtek-net.rules \
  file://40-block-devices.rules \
"    

do_install () {
  install -d ${D}/etc/udev/rules.d
  install -m 0666 ${WORKDIR}/70-persistent-net.rules  ${D}/etc/udev/rules.d/70-persistent-net.rules
  install -m 0666 ${WORKDIR}/50-usb-realtek-net.rules  ${D}/etc/udev/rules.d/50-usb-realtek-net.rules
  install -m 0666 ${WORKDIR}/40-block-devices.rules  ${D}/etc/udev/rules.d/40-block-devices.rules
}    

FILES_${PN} = "\
  /etc/udev/rules.d/70-persistent-net.rules \
  /etc/udev/rules.d/50-usb-realtek-net.rules \
  /etc/udev/rules.d/40-block-devices.rules \
"
