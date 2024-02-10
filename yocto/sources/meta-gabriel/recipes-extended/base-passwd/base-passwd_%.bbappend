do_install:append() {
    sed -i '/^root/ s/\/bin\/sh/\/sbin\/nologin/' ${D}${datadir}/base-passwd/passwd.master
}
