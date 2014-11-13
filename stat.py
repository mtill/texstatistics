#!/usr/bin/python3

import sys
import os
import json
import urllib.parse
import urllib.request
import subprocess
import importlib
import time
from operator import itemgetter
import re
from config import *


if len(sys.argv) != 3:
    print('invalid call; usage: projectname mainfile')
    exit(1)


project = re.sub(r"/[^a-zA-Z0-9]+/", "", sys.argv[1])
mainfile = sys.argv[2]

gnuplot = """set terminal pngcairo enhanced dashed color
set output '""" + datadir + project + """.png'
set style line 1 
set key top left
set xdata time
set timefmt "%Y-%m-%d"
set xtics format "%d.%m.%y"
set xtics 24*60*60
set xtics rotate by 45 right
set grid ytics lt 0 lw 1 lc rgb "#bbbbbb"
set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"
set ytics tc lt 1 nomirror
set y2tics 1 tc lt 2
plot '""" + datadir + project + """.gnuplotdata' using 1:2 with linespoints axes x1y1 lt 1 lw 2 title 'words (absolute)',\
 '""" + datadir + project + """.gnuplotdata' using 1:($2/""" + str(approxWordsPerPage) + """) with linespoints axes x1y2 lt 2 lw 2 title 'approx. pages (absolute)'"""

gnuplot_rel = """set terminal pngcairo enhanced dashed color
set output '""" + datadir + project + """_rel.png'
set style line 1 
set key top left
set xdata time
set timefmt "%Y-%m-%d"
set xtics format "%d.%m.%y"
set xtics 24*60*60
set xtics rotate by 45 right
set grid ytics lt 0 lw 1 lc rgb "#bbbbbb"
set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"
set ytics tc lt 1 nomirror
set y2tics 1 tc lt 2
plot '""" + datadir + project + """.gnuplotdata' using 1:3 with linespoints axes x1y1 lt 1 lw 2 title 'words (relative)',\
 '""" + datadir + project + """.gnuplotdata' using 1:($3/""" + str(approxWordsPerPage) + """) with linespoints axes x1y2 lt 2 lw 2 title 'approx. pages (relative)'"""

proc = subprocess.Popen("texcount -total -merge " + mainfile, shell=True, stdout=subprocess.PIPE)
result = {}
for line in proc.stdout:
    row = line.decode('utf-8')
    if '!!! File not found ' in row:
        print("texcount: something went wrong: " + row)
        exit(1)
    if ': ' in row:
        key, value = row.split(': ')
        if key != 'File' and key != 'Encoding':
            result[key] = value.strip()

if proc.wait() != 0:
    print("texcount: something went wrong!");
    exit(1)

jsonpath = datadir + project + ".json"

data = {}
if os.path.isfile(jsonpath):
    with open(jsonpath, 'r') as jsonfile:
        data = json.load(jsonfile)

today = time.strftime("%Y-%m-%d")
data[today] = result

with open(jsonpath, 'w') as jsonfile:
    json.dump(data, jsonfile, sort_keys=True, indent=2)

#jsonfile=open(datadir + project + ".json")
#data = json.load(jsonfile)
#jsonfile.close()


keys = sorted(data.keys())

oldv = {'Words in text': 0}
diff = 0
htmlfilepath = datadir + project + ".html"
gnuplotfilepath = datadir + project + ".gnuplot"
gnuplotfilepath_rel = datadir + project + ".gnuplot_rel"
gnuplotdatapath = datadir + project + ".gnuplotdata"

gnuplotdatafile = open(gnuplotdatapath, 'w')
for k in keys:
    diff = int(data[k]['Words in text']) - int(oldv['Words in text'])
    gnuplotdatafile.write(k + "\t" + data[k]['Words in text'] + "\t" + str(diff) + "\n")

    oldv = data[k]

gnuplotdatafile.close();

donetoday = 'nothing'
if (data[today]):
    donetoday = str(diff) + " words / " + str(round(diff/approxWordsPerPage, 1)) + " pages"

htmlpage = """<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>texstatistics</title>
</head>
<body>
<h3>texstatistics &mdash; """ + project + """</h3>
<p><b>today: """ + donetoday + """</b> (approx. """ + str(approxWordsPerPage) + """ words per page)</p>
<p id="progress"></p>
<p><img src=\"""" + project + """.png"></p>
<p><img src=\"""" + project + """_rel.png"></p>
</body>
</html>
"""

with open(htmlfilepath, 'w') as htmlfile:
    htmlfile.write(htmlpage)

if not os.path.isfile(gnuplotfilepath):
    gnuplotfilefile = open(gnuplotfilepath, 'w')
    gnuplotfilefile.write(gnuplot)
    gnuplotfilefile.close()

    gnuplotfilefile_rel = open(gnuplotfilepath_rel, 'w')
    gnuplotfilefile_rel.write(gnuplot_rel)
    gnuplotfilefile_rel.close()

proc = subprocess.Popen("gnuplot " + gnuplotfilepath + " >/dev/null", shell=True, stdout=subprocess.PIPE)
if proc.wait() != 0:
    print("gnuplot: something went wrong!")
    exit(1)

proc = subprocess.Popen("gnuplot " + gnuplotfilepath_rel + " >/dev/null", shell=True, stdout=subprocess.PIPE)
if proc.wait() != 0:
    print("gnuplot: something went wrong!")
    exit(1)

proc = subprocess.Popen("scp " + htmlfilepath + " " + datadir + project + ".png " + datadir + project + "_rel.png " + sshserver, shell=True, stdout=subprocess.PIPE)
if proc.wait() != 0:
    print("scp: something went wrong!")
    exit(1)

print('texstatistics finished successfully')

