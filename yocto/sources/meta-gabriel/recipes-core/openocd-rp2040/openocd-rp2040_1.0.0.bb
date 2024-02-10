DESCRIPTION = "OpenOCD for Raspberry Pi with FTDI, sysfs GPIO, and BCM2835 GPIO support"
SECTION = "devel/debug"
LICENSE = "CLOSED"

DEPENDS += "libusb1 libftdi libtool automake autoconf pkgconfig"

SRC_URI = "git://github.com/raspberrypi/openocd.git;protocol=https;branch=rp2040"
SRCREV = "${AUTOREV}"

S = "${WORKDIR}/git"

inherit autotools pkgconfig

EXTRA_OECONF = " --prefix=${prefix} --enable-ftdi --enable-sysfsgpio --enable-bcm2835gpio"

do_configure() {
    cd ${S}
    git init submodule
    git submodule update
    ./bootstrap
    oe_runconf
}

do_compile() {
    cd ${S}
    make
}

do_install() {
    cd ${S}
    make install 'DESTDIR=${D}'
}

FILES:${PN} = "\
                ${bindir}/openocd \
                ${datadir}/openocd \
"
