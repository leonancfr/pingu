
# Finalize sudo accesses for AUTHORIZED_USER_NAME
AUTHORIZED_USER_NAME ?= "gabriel"

do_install:append () {
   # Add sudo accesses for user.
    install -d -m 0710 "${D}/etc/sudoers.d"
    echo "${AUTHORIZED_USER_NAME} ALL=(ALL) NOPASSWD: ALL" > "${D}/etc/sudoers.d/0001_${AUTHORIZED_USER_NAME}"
    chmod 0644 "${D}/etc/sudoers.d/0001_${AUTHORIZED_USER_NAME}"
}

FILES:${PN}  +=  "/etc/sudoers.d \
               /etc/sudoers.d/0001_${AUTHORIZED_USER_NAME}"