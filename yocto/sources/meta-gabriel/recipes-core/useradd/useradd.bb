SUMMARY = "Recipe for using inherit useradd"
DESCRIPTION = "Recipe for using inherit useradd using features from useradd.bbclass"
SECTION = "USR"
LICENSE = "CLOSED"

RDEPENDS:${PN} = "bash"

SRC_URI = "\
file://.bashrc \
file://.gitconfig \
file://.docker/config.json \
file://bash_completion.d/docker \
file://patcher/data/success \
file://patcher/bin/1-fix-block-devices \
file://patcher/bin/2-super-patch \
file://patcher/bin/3-disable-eee \
file://patcher/bin/4-update-device-monitor \
file://patcher/bin/5-edge-crane \
file://patcher/bin/6-send-board-rev-info \
file://patcher/bin/7-support-to-quectell-modem \
file://patcher/bin/8-move-buried-files \
file://patcher/bin/9-update-socket-xp \
file://patcher/bin/13-rollback-socketxp-v1.3.9 \
"

S = "${WORKDIR}"

EXCLUDE_FROM_WORLD = "1"

inherit useradd

USERADD_PACKAGES = "${PN}"

USERADD_PARAM:${PN} = "\
	-u 1000 -d /home/gabriel -r -m -s /bin/bash -g gabriel -G dialout,sudo,docker -p '\$6\$11223344\$IxkfmzrFavuzP6OHfy.84cXhiK3pHEaFA.c93YDoEDhEKge/2rceAvjoDE2b3TSDKvjF.vWyKNBlKvJGQLSNU0' gabriel; \
"
                                                                                                 
GROUPADD_PARAM:${PN} = "-g 1000 gabriel; -g 995 docker"

do_install:append () {
	install -d -m 755 ${D}${base_prefix}/home/gabriel

	install -p -m 644 .bashrc ${D}${base_prefix}/home/gabriel/
	install -p -m 644 .gitconfig ${D}${base_prefix}/home/gabriel/

	install -d -m 755 ${D}${base_prefix}/home/gabriel/.docker
	install -p -m 644 .docker/config.json ${D}${base_prefix}/home/gabriel/.docker

	install -d -m 755 ${D}${base_prefix}/etc/bash_completion.d/
	install -p -m 644 bash_completion.d/docker ${D}${base_prefix}/etc/bash_completion.d/docker

	install -d -m 755 ${D}${base_prefix}/home/gabriel/.apps/patcher/data
	install -p -m 644 patcher/data/success ${D}${base_prefix}/home/gabriel/.apps/patcher/data

	install -d -m 755 ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -d -m 755 ${D}${base_prefix}/home/gabriel/.apps/patcher/log
	install -p -m 644 patcher/bin/1-fix-block-devices ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -p -m 644 patcher/bin/2-super-patch ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -p -m 644 patcher/bin/3-disable-eee ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -p -m 644 patcher/bin/4-update-device-monitor ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -p -m 644 patcher/bin/5-edge-crane ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -p -m 644 patcher/bin/6-send-board-rev-info ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -p -m 644 patcher/bin/7-support-to-quectell-modem ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -p -m 644 patcher/bin/8-move-buried-files ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -p -m 644 patcher/bin/9-update-socket-xp ${D}${base_prefix}/home/gabriel/.apps/patcher/bin
	install -p -m 644 patcher/bin/13-rollback-socketxp-v1.3.9 ${D}${base_prefix}/home/gabriel/.apps/patcher/bin

	chown -R gabriel ${D}${base_prefix}/home/gabriel

	chgrp -R gabriel ${D}${base_prefix}/home/gabriel
}

FILES:${PN} = "\
	${base_prefix}/home/gabriel/.bashrc \
	${base_prefix}/home/gabriel/.gitconfig \
	${base_prefix}/home/gabriel/.docker/config.json \
	${base_prefix}/home/gabriel/.apps/patcher/data/success \
	${base_prefix}/home/gabriel/.apps/patcher/log \
	${base_prefix}/home/gabriel/.apps/patcher/bin/1-fix-block-devices \
	${base_prefix}/home/gabriel/.apps/patcher/bin/2-super-patch \
	${base_prefix}/home/gabriel/.apps/patcher/bin/3-disable-eee \
	${base_prefix}/home/gabriel/.apps/patcher/bin/4-update-device-monitor \
	${base_prefix}/home/gabriel/.apps/patcher/bin/5-edge-crane \
	${base_prefix}/home/gabriel/.apps/patcher/bin/6-send-board-rev-info \
	${base_prefix}/home/gabriel/.apps/patcher/bin/7-support-to-quectell-modem \
	${base_prefix}/home/gabriel/.apps/patcher/bin/8-move-buried-files\
	${base_prefix}/home/gabriel/.apps/patcher/bin/9-update-socket-xp\
	${base_prefix}/home/gabriel/.apps/patcher/bin/13-rollback-socketxp-v1.3.9\
	${base_prefix}/etc/bash_completion.d/docker \
"

# Prevents do_package failures with:
# debugsources.list: No such file or directory:
INHIBIT_PACKAGE_DEBUG_SPLIT = "1"
