do_deploy:append() {
    install -d ${DEPLOYDIR}/${BOOTFILES_DIR_NAME}
    CONFIG=${DEPLOYDIR}/${BOOTFILES_DIR_NAME}/config.txt
    echo "disable_splash=1" >> $CONFIG
    echo "usbcore.quirks=0bda:8153:k" >> $CONFIG
    echo "enable_uart=1" >> $CONFIG
}
