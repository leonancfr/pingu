SUMMARY = "System recipe"
DESCRIPTION = "Recipe to customize system"
LICENSE = "CLOSED"

SRC_URI = "file://sysctl.conf"

S = "${WORKDIR}"

do_install() {
	install -d ${D}/${sysconfdir}
	install -m 0644 ${WORKDIR}/sysctl.conf ${D}${sysconfdir}
}
