FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://1-cameras0.network \
    file://2-eth0.network \
    file://3-modem0.network \
"

do_install:append() {
    install -d ${D}${sysconfdir}/systemd/network
    install -m 0644 ${WORKDIR}/1-cameras0.network ${D}${sysconfdir}/systemd/network
    install -m 0644 ${WORKDIR}/2-eth0.network ${D}${sysconfdir}/systemd/network
    install -m 0644 ${WORKDIR}/3-modem0.network ${D}${sysconfdir}/systemd/network
}

FILES:${PN} += " \
    ${sysconfdir}/systemd/network/1-cameras0.network \
    ${sysconfdir}/systemd/network/2-eth0.network \
    ${sysconfdir}/systemd/network/3-modem0.network \
"
