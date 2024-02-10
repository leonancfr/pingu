SUMMARY = "Quectel Softwares"
LICENSE = "CLOSED"

RDEPENDS:${PN} = "bash libusb1"

SRC_URI = "\
  file://quectel-atc-proxy \
  file://quectel-CM \
  file://quectel-mbim-proxy \
  file://quectel-qmi-proxy \
"    

S = "${WORKDIR}"

do_install:append() {
	install -d ${D}${base_prefix}/opt/quectel/bin
	install -m 0755 quectel-atc-proxy ${D}${base_prefix}/opt/quectel/bin
	install -m 0755 quectel-CM ${D}${base_prefix}/opt/quectel/bin
	install -m 0755 quectel-mbim-proxy ${D}${base_prefix}/opt/quectel/bin
	install -m 0755 quectel-qmi-proxy ${D}${base_prefix}/opt/quectel/bin
}

FILES:${PN} = "\
	${base_prefix}/opt/quectel/bin/quectel-atc-proxy \
	${base_prefix}/opt/quectel/bin/quectel-CM \
	${base_prefix}/opt/quectel/bin/quectel-mbim-proxy \
	${base_prefix}/opt/quectel/bin/quectel-qmi-proxy \
"
