SUMMARY = "Firmware ETH1"
LICENSE = "CLOSED"

RDEPENDS:${PN} = "bash libusb1"

SRC_URI = "\
	file://rtl8153a-4.fw \
"

S = "${WORKDIR}"

do_install:append() {
	install -d ${D}${base_prefix}/lib/firmware/rtl_nic/
	install -m 0755 rtl8153a-4.fw ${D}${base_prefix}/lib/firmware/rtl_nic/
	
}

FILES:${PN} = "\
	${base_prefix}/lib/firmware/rtl_nic/rtl8153a-4.fw \
"