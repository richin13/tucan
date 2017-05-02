import os.path

from ConfigParser import SafeConfigParser

HEADER = """
<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
        <meta http-equiv="Content-Type" content= "text/html; charset=utf-8" />
        <link href="css/main.css" rel="stylesheet" type="text/css" />
		<link rel="stylesheet" href="css/lightbox.css" type="text/css" media="screen" />
        <link rel="icon" href="images/tucan.ico" type="image/x-icon" />
        <script type="text/javascript" src="js/translate.js"></script>
        <script type="text/javascript" src="js/misc.js"></script>

        <title>Tucan Manager - %%TITLE%%</title>
</head>

<body>

<div id="container">
        <div id="header">
        <a href="index.html"><img src="images/logo.png" alt="Tucan logo" /></a>
        </div>
        
        <div id="menu">
        <ul>
                <li><a href="development.html">Development</a></li>
                <li><a href="downloads.html">Downloads</a></li>
                <li><a href="features.html">Features</a></li>
                <li><a href="screenshots.html">Screenshots</a></li>
                <li><a href="support.html">Support</a></li>
        </ul>
        </div>
        
        <div id="google_translate_element"></div>
        <script src="http://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
"""
	
FOOTER = """
        <div id="footer">
        <br />
        <p>Copyright &copy; 2008-2011 The Tucan Project</p>
        <p>Designed by Paco Salido.</p>
        <br />
        </div>
</body> 
</html>
"""

INDEX = """
	            
	    <div id="right">
	            <div id="box">
	            <h3>Download Now</h3>
	            <div id="dlbutton">
	            <script type="text/javascript">get_download()</script>
	            </div>
	            <div id="others">
	            <a href="downloads.html">Other downloads &raquo;</a>
	            </div>
	            </div>
	    </div>  

	    <div id="content">
	    <img src="images/screenshot.png" alt="Screenshot" />
	    <div>
	    <p><b>File sharing as free and open as it should be.</b></p>
	    <p>Tucan Manager is a free file sharing application designed for 1-Click Hosters. 
	    Fast and lightweight, Tucan is fully open-source and compatible with Windows, GNU/Linux, and MacOSX.</p>
	    <p>With Tucan's modular support for the principal Hosters, captcha resolution, interchangeable links, 
	    premium user accounts, and many other great features, you'll learn why users 
	    around the world are making the switch to free, open 1-Click Hosted file sharing.</p>
	    <p><a href="features.html">Learn more</a> &raquo;</p>
	    <br />
	    </div>
	    </div>
</div>  
"""

DEVELOPMENT = """
<div id="right">
	            <div id="box">
	            <h3>Development News</h3>
	            <div class="twitters" id="twitter">

	            <script type="text/javascript" src="js/twitter.js"></script>
	            <script type="text/javascript" charset="utf-8">
	            getTwitters('twitter', {
	                    id: 'tucaneando', 
	                    count: 4, 
	                    withFriends: true,
	                    ignoreReplies: false,
	                    template: '<a href="http://twitter.com/%user_screen_name%"><img src="images/twitter.png"/></a>"%text%"<br /><b>%time%</b>',
	                    });
	            </script>
	            <p><img src="images/lightbox2/loading.gif" /><strong>Loading, please wait.</strong></p>
	            </div>
	            </div>
	    </div>  

	    <div id="content">
	    <div>

	            <h3>Source Code Repository</h3>
	            <p>The code is hosted at <a href="http://code.google.com/p/tucan/">Google Code</a>
	             using <a href="http://subversion.tigris.org/">Mercurial</a>.
	             To get a working copy of the development version use the following command:</p>
	            <p><code>hg clone https://tucan.googlecode.com/hg/ tucan-hg</code></p>
	    </div>

	    <div>
	            <h3>Bug Reporting</h3>
	            <p>Anybody can report bugs or request new features at our 
	            <a href="http://code.google.com/p/tucan/issues/list">Tracker</a>. Read throughout the open issues 
	            and avoid making duplicates.</p>
	            <p>When reportig a bug use our <b>report dialog</b> from 
	            <a href="images/screenshots/large/logs.png" rel="lightbox" title="Log View">LogView</a>

	            and remember to paste the <b>Report ID</b> on the summary field.</p>
	            <p>Thanks for your help in keeping the database clean and useful for all.</p>
	    </div>
	    <div>
	            <h3>Contribute</h3>
	            <p>We always need a hand or two. So if you are willing to help with the development, why not
	            <a href="http://code.google.com/p/tucan/wiki/HowToContribute">join</a> the team?</p>

	            <p>There are also other areas where you could be of great help, like 
	            <a href="http://code.google.com/p/tucan/wiki/HowToDocStrings">documentation</a> and
	            <a href="http://code.google.com/p/tucan/wiki/HowToLocalize">localization</a>.</p>
	            <p>Even if you don't feel confident with the code, we need your assistance <b>testing</b> 
	            the development version or <b>helping</b> other users at the 
	            <a href="http://forums.tucaneando.com">forum</a>.</p>

	    </div>
	    </div>
	    
</div>
"""

SUPPORT = """
       <div id="right">
                <div id="box">
                <h3>Make a Suggestion</h3>
                <div id="suggestion">
                <iframe style="display:none;visibility:hidden;" name="hiddenframe" id="hiddenframe"></iframe>
                <form name="suggestion" action="http://crak.appspot.com/add" method="post" target="hiddenframe">
                <input type="hidden" name="uuid" value="26282d94-d468-11de-8b3e-002500d735c2">
                <input type="hidden" name="email" value="">
                <textarea name="comment" cols="22" rows="5"></textarea>
                <input type="hidden" name="log" value="webpage user suggestion">
                <input type="submit" name="submit" value="send" onclick="this.disabled=true">
                </form>
                </div>
                </div>
        </div>

        <div id="content">
        <div>
                <h3>Documentation</h3>
                <p>The first step when you are having trouble is to read the 
                <a href="http://doc.tucaneando.com/readme.html">documentation</a>, it has information
                about instalation, configuration and functionalities.</p>
                <p>There is also a <a href="http://doc.tucaneando.com/faq.html">FAQ</a> and a 
                <a href="http://doc.tucaneando.com/howto.html">tutorial</a> about plugin implementation.</p>
        </div>
        <div>
                <h3>Community Forum</h3>
                <p>If you could not solve your problem with the documentation help, 
                its time to ask at the <a href="http://forums.tucaneando.com/">forum</a>.</p>
                <p>Use the search utility to find previous posts related to the issue. 
                If there isn't any, create a new thread stating as concisely as possible your problem 
                and give the most information so that we can reproduce it.</p>
                <p>Remember that the community is composed by users like you, so be polite and try to help as well.</p>
        </div>
        <div>
                <h3>IRC Channel</h3>
                <p>Join the chat room <code>#tucan</code> at <code>irc.irc-hispano.org</code>
                 using your usual irc client or <a href="webchat.html">webchat</a>.</p>
                <p>There you can discuss with the developer team and other users about bugs, features or anything
                related to Tucan.</p>
        </div>
        </div>
</div>
"""

SCREENSHOTS = """
	<div id="content">
        <h3>Screenshots</h3>
        %%SETS%%
</div>
	<script type="text/javascript" src="js/lightbox2/prototype.js"></script>
	<script type="text/javascript" src="js/lightbox2/scriptaculous.js?load=effects"></script>
	<script type="text/javascript" src="js/lightbox2/lightbox.js"></script>
"""

WEBCHAT = """
		<div id="content">
        <h3>#tucan @ irc.irc-hispano.org</h3>
        <iframe marginWidth="0" marginHeight="0" src="http://minichat.irc-hispano.es/?canal=tucan"
         width="590" height="400" scrolling="no" frameborder="0"></iframe>
        </div>
</div>  
"""

FEATURES = """
		<div id="right">
                <div id="box">
                <h3>Supported Services</h3>
                <div id="services">
                %%SERVICES%%
                </div>
                <br />
                </div>
        </div>  

        <div id="content">
        <div>
                <h3>Give us the links, we'll cook the meal!</h3>
                <p>Supporting the main Hosters like <a href="http://rapidshare.com">RapidShare</a>
                 or <a href="http://megaupload.com">MegaUpload</a>, Tucan brings a new experience
                 to users discouraged by other file sharing methods as p2p.</p>
        </div>
        <div id="right-image">
                <img src="images/features/captcha.png" alt="captcha">
                <p><a href="http://code.google.com/p/tesseract-ocr/">
                Tesseract OCR engine</a> in combination with 
                <a href="http://www.pythonware.com/products/pil/">PIL</a> library, grant
                Tucan the ability to solve any <b>captcha</b> whitout user action.</p>
        </div>
        <div>
                <p>Tucan also manages waits between downloads and interchangeable links seamlessly, 
                relieving the user from this nuisance.</p>
                
                <h3>Lightning Fast</h3>
                <p>Since Tucan is designed to be <b>fast</b> and <b>lightweight</b> from the ground up, 
                you can enjoy all of its features without slowing down the rest of your system.</p>
                
                <p>No more heavy runtimes like <i>Java</i> or <i>.Net</i>, 
                Tucan has the smallest footprint you can get.</p>
                
                <h3>A friendly face everywhere</h3>
                <p>Whether you use Windows, GNU/Linux, or a Mac, Tucan is right at home on your desktop. 
                With a simple but fully functional graphical interface, its appearance 
                serves a confortable File Sharing experience on almost any computer.</p>
        </div>
        <div id="left-image">
                <img src="images/features/gtk.png" alt="gtklogo">
                <p>Use of the <a href="http://www.gtk.org/">GTK+</a> toolkit provides 
                top level stability and superb performance.</p>
        </div>
        <div>
                <h3>The power of Open Source</h3>
                <p>Implemented in <a href="http://python.org/">Python</a> with a modular architecture in mind,
                Tucan can be easily extended. Furthermore, the whole source code is publicly available so
                everybody is invited to join and help us improve this amazing software.</p>
                
                <p>Not only anyone can support new hosters with the <b>Plugin Subsystem</b>, 
                but also updates can be deployed instantly by the <b>Update Manager</b>.</p>
                
                <p>Moreover, there is an <b>Addon Subsystem</b> based on events which enables Tucan
                 to grow much farther.</p>
        </div>
</div>

"""

DOWNLOADS = """
<div id="content">
        <h3>Download Tucan Manager</h3>
        <br />
       	%%SRC%%
        %%RC%%
        <h3>Platform specific Binaries</h3>
        <br />
	%%WIN%%
	%%OSX%%     
        <h3>GNU/Linux Distribution Packages</h3>
        <br />
        <div>
                <img src="images/downloads/debian.png" alt="deblogo">
                <b>Debian</b>
                <br /><code># apt-get install tucan</code>
                <br /><a href="http://packages.debian.org/tucan">Official Packages</a>
        </div>
        <div>
                <img src="images/downloads/ubuntu.png" alt="ubulogo">
                <b>Ubuntu</b>
                <br /><code>$ sudo aptitude install tucan</code>
                <br /><a href="http://packages.ubuntu.com/tucan">Official Packages</a>
        </div>
        <div>
                <img src="images/downloads/fedora.png" alt="fedlogo">
                <b>Fedora</b>
                <br /><code># yum install -y tucan</code>
                <br /><a href="https://admin.fedoraproject.org/updates/tucan">Official Packages</a>
        </div>
        <div>
                <img src="images/downloads/gentoo.png" alt="genlogo">
                <b>Gentoo</b>
                <br /><a href="http://bugs.gentoo.org/261907">Official Packages</a>
        </div>
        <div>
                <img src="images/downloads/arch-linux.png" alt="arclogo">
                <b>Arch-Linux</b>
                <br /><code>$ yaourt -S tucan</code>
                <br /><a href="http://www.archlinux.org/packages/community/i686/tucan/">Official Packages</a>
        </div>
                <p><i>For older releases please check the <a href="http://forja.rediris.es/frs/?group_id=408">
                archive</a></i> &raquo;</p>
        </div>
</div>  
"""

MISC = """
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
"""
		
class Generator(SafeConfigParser):
	""""""
	def __init__(self, conf):
		""""""
		SafeConfigParser.__init__(self)
		self.read(conf)
		if self.has_section("pages"):
			for option in self.options("pages"):
				if self.has_section(option):
					css = None
					if self.has_option(option, "css"):
						css = self.get(option, "css")
					t = Template(self.get(option, "title"), css)
					advanced_options = []
					if self.has_option(option, "advanced"):
						advanced = self.get(option, "advanced")
						if self.has_section(advanced):
							for advanced_option in self.options(advanced):
								tmp = [advanced_option, self.get(advanced, advanced_option)]
								if self.has_section(advanced_option):
									tmp.append(self.items(advanced_option))
								advanced_options.append(tmp)
					t.add_content(option, advanced_options)
					t.save(self.get("pages", option))
class Template:
	""""""
	def __init__(self, title, css):
		""""""
		self.title = title
		self.css = css
		self.html = ""
		
	def add_content(self, option, advanced):
		""""""
		options = {"features": self.add_services, "misc": self.add_js, "screenshots": self.add_screenshots, "downloads": self.add_downloads}

		self.html += globals()[option.upper()]
		if advanced:
			options[option](advanced)

	def add_services(self, services):
		""""""
		div = """
				<img src="images/features/services/%%ICO%%" alt="%%NAME%%"/>
				<a href="http://%%NAME%%"><strong>%%NAME%%</strong></a>
				<br />
		"""
		tmp = ""
		for service in services:
			tmp += div.replace("%%NAME%%", service[0]).replace("%%ICO%%", service[1])
       
		self.html = self.html.replace("%%SERVICES%%", tmp)
		
	def add_js(self, constants):
		""""""
		for plat, desc, info in constants:
			plat = plat.upper()
			self.html += '\nvar %s_PLAT="%s";\n' % (plat, desc)
			for option, value in info:
				self.html += 'var %s_%s="%s";\n' % (plat, option.upper(), value)

	def add_downloads(self, downloads):
		""""""
		div = """<div>
		<img src="images/downloads/%%PLAT%%.png" alt="%%PLAT%%logo">
		<b>%%DESC%%</b>
		<br />
		<a href='%%URL%%'>%%PKG%%</a>
		<br />
		<a href='%%MIRROR%%'><small>Alternative mirror</small></a>
	</div>"""

		for plat, desc, info in downloads:
			tmp = div
			tmp = tmp.replace("%%DESC%%", desc)
			tmp = tmp.replace("%%PLAT%%", plat)
			url = info[0][1]
			tmp = tmp.replace("%%URL%%", url)
			tmp = tmp.replace("%%PKG%%", url.split("/").pop())
			tmp = tmp.replace("%%MIRROR%%", info[2][1])
			self.html = self.html.replace("%%%%%s%%%%" % plat.upper(), tmp)
		if "%%RC%%" in self.html:
			self.html = self.html.replace("%%RC%%", "")

	def add_screenshots(self, screenshots):
		""""""
		div = """
		<div>
                <a href="images/screenshots/large/%%SHOT%%" rel="lightbox[last]" title="%%DESC%%">
                <img src="images/screenshots/thumbs/%%SHOT%%">
                </a>
        </div>
        """
		tmp = ""
		for vers, date, shots in sorted(screenshots):
			tmp += '<img src="images/screenshots/calendar.png"><p>%s - Version %s</p>\n' % (date, vers)
			for shot, desc in shots:
				tmp += div.replace("%%SHOT%%", shot).replace("%%DESC%%", desc)
			tmp += '<p style="clear:both;"></p>'
		self.html = self.html.replace("%%SETS%%", tmp)

	def save(self, file_name):
		""""""
		if ".html" in file_name:
			head = HEADER.replace("%%TITLE%%", self.title)
			css = '<link href="css/main.css" rel="stylesheet" type="text/css" />\n'
			if self.css:
				head = head.replace(css, "%s\t%s" % (css, css.replace("main.css", self.css)))
			self.html = head + self.html
			self.html += FOOTER
		elif ".js" in file_name:
			file_name = os.path.join("js", file_name)
		f = file(os.path.join("homepage", file_name), "w")
		f.write(self.html)
		f.close()

if __name__ == "__main__":
	Generator("web.conf")
