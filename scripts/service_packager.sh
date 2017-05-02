#!/bin/bash
# dependencies: bash, lynx, wget, tar, gzip, subversion (and account in all mirrors)

MAIN_REPOSITORY="https://tucan.googlecode.com/hg/src/default_plugins/"

MIRROR1="https://forja.rediris.es/svn/cusl3-tucan/branches/update_manager/0.3.10/"
MIRROR2="https://build-tucan-doc.googlecode.com/svn/branches/update_manager/0.3.10/"

TEMP_DIR="/tmp/tucan_um/"

EXTENSION=".tar.gz"

services_list() {
	for name in $(lynx -dump "${MAIN_REPOSITORY}" | grep "/src/default_plugins/" | cut -d'/' -f7); do
		printf "%s\n" $name
	done
}

info() {
	printf "\nTucan\'s service packager.\n"
	printf "\n\tUsage: %s <service name>\n" $(basename $0)
	printf "\n\nService list:\n\n"
	services_list
	printf "\n"
}

update() {
	printf "\n\nsvn checkout $1 ${TEMP_DIR}$2\n"
	test $(svn checkout $1 ${TEMP_DIR}$2)

	printf "\n\ncat ${TEMP_DIR}$2/updates.conf\n"
	cat ${TEMP_DIR}$2/updates.conf

	SERVICE_UPDATE=$(cat ${TEMP_DIR}$3/service.conf | grep "update" | cut -d' ' -f3)
	SERVICE_NAME=$(cat ${TEMP_DIR}$3/service.conf | grep "name = $3" | cut -d' ' -f3)
	LINE=$(cat ${TEMP_DIR}$2/updates.conf | grep $3)
	if [ -n $LINE ]; then
		printf "\n\necho ${SERVICE_NAME} = ${SERVICE_UPDATE} >> ${TEMP_DIR}$2/updates.conf\n"
		echo "${SERVICE_NAME} = ${SERVICE_UPDATE}" >> ${TEMP_DIR}$2/updates.conf
	else
		printf "\n\nsed -i \"s/${LINE}/${SERVICE_NAME} = ${SERVICE_UPDATE}/\" ${TEMP_DIR}updates.conf\n"
		sed -i "s/${LINE}/${SERVICE_NAME} = ${SERVICE_UPDATE}/" ${TEMP_DIR}$2/updates.conf
	fi

	printf "\n\nrm -f ${TEMP_DIR}$2/$3$EXTENSION\n"
	rm -f ${TEMP_DIR}$2/$3$EXTENSION

	printf "\ncp ${TEMP_DIR}$3$EXTENSION ${TEMP_DIR}$2/\n"
	cp ${TEMP_DIR}$3$EXTENSION ${TEMP_DIR}$2/

	printf "\ncd ${TEMP_DIR}$2/ && svn add $3$EXTENSION/\n"
	cd ${TEMP_DIR}$2/ && svn add $3$EXTENSION

	printf "cd ${TEMP_DIR}$2/ && svn commit --message \"$3 update (${SERVICE_UPDATE})\"\n"
	cd ${TEMP_DIR}$2/ && svn commit --message "$3 update (${SERVICE_UPDATE})"
}

main() {
	if [ -d ${TEMP_DIR} ]; then
		printf "\nrm -rf ${TEMP_DIR}\n"
		rm -rf ${TEMP_DIR}
	fi

	printf "\nmkdir --parents ${TEMP_DIR}$1\n"
	mkdir --parents ${TEMP_DIR}$1

	printf "\nwget --no-verbose --recursive --no-parent --no-host-directories --cut-dirs=3 --reject=\"html\" --directory-prefix=\"${TEMP_DIR}\" ${MAIN_REPOSITORY}$1/\n"
	wget --no-verbose --recursive --no-parent --no-host-directories --cut-dirs=3 --reject="html" --directory-prefix="${TEMP_DIR}" "${MAIN_REPOSITORY}$1/"

	if [ $? -eq 0 ]; then

		printf "\nfind ${TEMP_DIR}$1 -iname \".hg\" -type d -execdir rm -rf \"{}\" \";\" 2> /dev/null\n"
		find ${TEMP_DIR}$1 -iname ".hg" -type d -execdir rm -rf "{}" ";" 2> /dev/null

		printf "\ncd ${TEMP_DIR} && tar zcf $1$EXTENSION $1\n"
		cd ${TEMP_DIR} && tar zcf $1$EXTENSION $1

		#----------

		update $MIRROR1 "forja" $1
		update $MIRROR2 "btd" $1

		#----------

		printf "\n\nls -lF ${TEMP_DIR}\n"
		ls -lF ${TEMP_DIR}
	else
		info
	fi
}

if [ $# -ne 1 ] || [ "$1" == "" ]; then
	info
	exit 1
else
	main $1
fi
