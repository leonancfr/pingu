SUMMARY = "Expand disk recipe"
DESCRIPTION = "Recipe for increase rootfs in startup if necessary"
LICENSE = "CLOSED"

SRC_URI = "file://xdisk"

S = "${WORKDIR}"

do_install() {
	install -d ${D}${bindir}
	install -m 0755 xdisk ${D}${bindir}
}