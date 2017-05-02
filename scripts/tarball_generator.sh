#!/bin/bash
info() {
	printf "\nTucan\'s tarball generator.\n"
	printf "\nUsage: %s <version>\n\n" $(basename $0)
}

main() {
	VERSION="$1"
	DIRECTORY="tucan-$VERSION"
	URL="https://forja.rediris.es/svn/cusl3-tucan/trunk"
	#URL="https://forja.rediris.es/svn/cusl3-tucan/branches/0.3.8"

	printf "\nsvn checkout $URL $DIRECTORY\n\n"
	svn checkout $URL $DIRECTORY
	REVISION=$(svnversion $DIRECTORY)

	printf "\nrm -rf $DIRECTORY/packages/debian/tmp/\n"
	rm -rf $DIRECTORY/packages/debian/tmp/

	printf "\nrm -rf $DIRECTORY/proof_of_concept/\n"
	rm -rf $DIRECTORY/proof_of_concept/

	printf "\nfind $DIRECTORY/ -iname \".svn\" -type d -execdir rm -rf \"{}\" \";\" 2> /dev/null\n"
	find $DIRECTORY/ -iname ".svn" -type d -execdir rm -rf "{}" ";" 2> /dev/null

	printf "\nprintf \"$VERSION\\ \bnrev $REVISION\\ \bn\" > $DIRECTORY/VERSION\n"
	printf "$VERSION\nrev $REVISION\n" > $DIRECTORY/VERSION

	printf "\nchmod 755 $DIRECTORY/tucan.py\n"
	chmod 755 $DIRECTORY/tucan.py

	printf "\ntar zcf $DIRECTORY.tar.gz $DIRECTORY/\n"
	tar zcf $DIRECTORY.tar.gz $DIRECTORY/

	printf "\ndu -sh $DIRECTORY*\n"
	du -sh $DIRECTORY*
}

if [ $# -ne 1 ] || [ "$1" == "" ]; then
	info
	exit 1
else
	main $1
fi
