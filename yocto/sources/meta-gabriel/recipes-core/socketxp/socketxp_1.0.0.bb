SUMMARY = "SocketXP Agent"
DESCRIPTION = "Recipe to install socketxp agent"
LICENSE = "CLOSED"

SRC_URI = "\
	file://socketxp \
"

S = "${WORKDIR}"

do_install() {
	install -d ${D}${base_prefix}/usr/local/bin
	install -m 0755 socketxp ${D}${base_prefix}/usr/local/bin
	install -d -m 755 ${D}${base_prefix}/etc/socketxp
	install -d -m 755 ${D}${base_prefix}/var/lib/socketxp
}

FILES:${PN} = "\
	${base_prefix}/usr/local/bin/socketxp \
	${base_prefix}/etc/socketxp \
	${base_prefix}/var/lib/socketxp \
"