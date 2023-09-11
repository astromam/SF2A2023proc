#!/usr/bin/python
# -*- coding: latin-1 -*-
# This program creates the .tex files for the individual sessions
# from the file book-setup.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Written in python3 by A. Siebert 8.Oct.2021


import string
import re
from sf2a_utils import *
import os
import re
import sys
import codecs
import subprocess
from pathlib import Path

# Check python version, must be at least 3
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3+, your system is using Python "+str(sys.version_info[0]))


# Read setup file
with open("book-setup.py") as myf:
    code = compile(myf.read(), "book-setup.py", 'exec')
    exec(code)

# Create template for file
mytemplate=string.Template('\\documentclass{$MYCLS}\n\
\\usepackage{graphicx}\n\n\
\\newcommand{\sigle}{Session $SES_NUM}\n\
\\newcommand{\\texte}{$SES_NAME}\n\
\n\
\\begin{document}\n\
\n\
\TitreGlobal{SF2A $YEAR}\n\
\n\
\\title{NOTINTOC} \n\
%\n\
\\author{}\\address{}\n\
\\runningtitle{}\n\
%\n\
\setcounter{page}{1}\n\
% Keep this line, even if the page will be settled afterwards...\n\
\n\
\\vspace*{5cm}\n\
\n\
\centering{\huge \sigle}\n\
\n\
\\vspace*{2cm}\n\
\n\
\centering\\begin{minipage}[h]{.9\linewidth}\n\
\centering{\huge \\texte}\n\
\end{minipage}\n\
\n\
\\newpage\n\
\n\
\\, \n\
\n\
%\centering\includegraphics[width = .9\linewidth]{photo}\n\
\n\
%\\textsl{}\n\
\n\
\\vfill\n\
\n\
%\centering\includegraphics[width = .9\linewidth]{photo}\n\
\n\
\\vfill\n\
\n\
\end{document}\n')

# Loop over all sessions to create tex file
for num in range(len(sessions)):
    session = sessions[num]
    session_name = list(session.keys())[0]

    # la contrib generale de la session est toujours en premier, pas la peine de boucler pour la chercher
    session_num = list(session.values())[0][0]
    path = 'contrib/' + session_num
    filename = 'contrib/' + session_num + '/' + session_num + '.tex'
    print("Creating tex file for ",session_name," in ",filename)


    texfile = open(filename,"w")
    print(filename,clsfile,session_num,year,session_name)
    mytext=mytemplate.substitute(MYCLS=clsfile,SES_NUM=session_num, YEAR=year, SES_NAME=session_name)
    texfile.write(mytext)
    texfile.close()
    #print(mytext)
