SUMMARY = "Firmware RP2040"
LICENSE = "CLOSED"
PR = "r0"

RDEPENDS:${PN} = "bash libusb1"

SRC_URI = "\
	file://rp2040.elf \
"

S = "${WORKDIR}"

do_install:append() {
    install -d ${D}${base_prefix}/opt/gabriel/bin/firmware-rp2040/
    install -m 0644 rp2040.elf ${D}${base_prefix}/opt/gabriel/bin/firmware-rp2040/
}

FILES:${PN} = "\
	${base_prefix}/opt/gabriel/bin/firmware-rp2040/rp2040.elf \
"