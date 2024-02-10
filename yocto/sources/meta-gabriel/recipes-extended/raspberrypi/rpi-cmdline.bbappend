do_deploy:append() {
    install -d ${DEPLOYDIR}/${BOOTFILES_DIR_NAME}
    CMDLINE=${DEPLOYDIR}/${BOOTFILES_DIR_NAME}/cmdline.txt
    sed -i 's/$/ logo.nologo/' $CMDLINE
    sed -i 's/$/ quiet/' $CMDLINE
}
