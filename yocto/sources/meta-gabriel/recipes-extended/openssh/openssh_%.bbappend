FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://trusted-CA.pem \
"

do_install:append() {
    install -d ${D}${sysconfdir}/ssh
    install -m 0644 ${WORKDIR}/trusted-CA.pem ${D}${sysconfdir}/ssh
}

FILES:${PN} += " \
    ${sysconfdir}/ssh/trusted-CA.pem \
"
