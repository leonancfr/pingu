SUMMARY = "Recipe for using config envs"
LICENSE = "CLOSED"

RDEPENDS:${PN} = "bash"

SRC_URI = "\
file://gabriel_profile.sh \
"

S = "${WORKDIR}"

do_install:append () {
	install -d -m 755 ${D}${base_prefix}/etc/profile.d/
	install -p -m 644 gabriel_profile.sh ${D}${base_prefix}/etc/profile.d/
}

FILES:${PN} = "\
	${base_prefix}/etc/profile.d/gabriel_profile.sh \
"