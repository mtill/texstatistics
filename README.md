texstatistics
=============

Python script to depict daily progress in writing a LaTex document.

## requirements
 * gnuplot (http://gnuplot.sourceforge.net/; in Ubuntu, install the gnuplot-x11 package)
 * texcount.pl (http://app.uio.no/ifi/texcount/; in Ubuntu, install the texlive-extra-utils package)

## configuration
 * edit config.py and set the following variables appropriately:

   * sshserver = 'Webserver-URI:/var/www/stat'
   * approxWordsPerPage = 335
   * datadir = "/home/user/workspace/Project-Dir"


## usage

 * ./stat.py Your-Project-Name Main-TeX-File (add this to your Makefile or GIT/SVN hooks)
 * go to http://your-webserver/stat/Your-Project-Name.html

