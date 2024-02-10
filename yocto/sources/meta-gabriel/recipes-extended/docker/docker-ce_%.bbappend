SYSTEMD_SERVICE:${PN} += "${@bb.utils.contains('DISTRO_FEATURES','systemd','docker.service','',d)}"

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://docker.service \
    file://docker.socket \
    file://daemon.json \
"

do_install:append() {
  install -d ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/docker.service ${D}/${systemd_unitdir}/system
  install -m 0644 ${WORKDIR}/docker.socket ${D}/${systemd_unitdir}/system

  install -d ${D}/etc/docker
  install -m 0644 ${WORKDIR}/daemon.json ${D}/etc/docker
}

FILES:${PN} += " \
    ${systemd_unitdir}/system/docker.service \
    ${systemd_unitdir}/system/docker.socket \
    /etc/docker/daemon.json \
"