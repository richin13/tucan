
function get_download()
{
	var DESCRIPTION=SRC_VERS+' - '+SRC_PLAT;
	var URL=SRC_URL;
	if (navigator.appVersion.indexOf("Win")!=-1) {
		DESCRIPTION=WIN_VERS+' for '+WIN_PLAT;
		URL=WIN_URL;
	}
	else if (navigator.appVersion.indexOf("Mac")!=-1) {
		DESCRIPTION=OSX_VERS+ ' for '+OSX_PLAT;
		URL=OSX_URL;
	}
	document.write('<a href='+URL+'><b>Tucan Manager</b>');
	document.write('<br />');
	document.write(DESCRIPTION)
	document.write('</a>');
}

var WIN_PLAT="MS Windows";
var WIN_URL="http://forja.rediris.es/frs/download.php/2050/tucan-0.3.10-win32.zip";
var WIN_VERS="0.3.10";
var WIN_MIRROR="http://build-tucan-doc.googlecode.com/files/tucan-0.3.10-win32.zip";

var OSX_PLAT="Mac OS X";
var OSX_URL="http://forja.rediris.es/frs/download.php/2057/tucan-0.3.10.dmg";
var OSX_VERS="0.3.10";
var OSX_MIRROR="http://build-tucan-doc.googlecode.com/files/tucan-0.3.10.dmg";

var SRC_PLAT="Source Code";
var SRC_URL="http://forja.rediris.es/frs/download.php/2051/tucan-0.3.10.tar.gz";
var SRC_VERS="0.3.10";
var SRC_MIRROR="http://build-tucan-doc.googlecode.com/files/tucan-0.3.10.tar.gz";
