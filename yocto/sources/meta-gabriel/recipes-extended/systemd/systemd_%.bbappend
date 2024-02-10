FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += "file://systemd-udevd.service"

do_install:append() {
    cp ${WORKDIR}/systemd-udevd.service ${D}/lib/systemd/system
}
