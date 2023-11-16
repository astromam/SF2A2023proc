#!/usr/bin/python
# -*- coding: latin-1 -*-
# This program generates the list of participants of the conference
# based on a provided csv file containing first name, last name and email
# address (other fields will not be used)
#
# Usage : make_listparticipants.py csvfile
#
# Output : list_participants.tex
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
import csv

def format_name(mystring):
    """ 
    format_name(str)

    Format the first names to have an upper case letter in first place and lowercase afterwards
    Handles spaces and - separations between names

    Input: str, a string containing first name(s)
    Output: formated string
    """

    mylist = list(mystring)
    mylist[0] = mylist[0].upper()

    ll=len(mylist)
    for i in range(1,ll,1):
        if mylist[i-1] in {' ','-'}:
            mylist[i] = mylist[i].upper()
        else:
            mylist[i] = mylist[i].lower()

    mystring= ''.join(mylist)
    return mystring

#--------------------------

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3+, your system is using Python "+str(sys.version_info[0]))


if len(sys.argv)<2:
    raise Exception("Usage: make-listparticipants.py yourcsvfile [delimiter=;]\nDefault delimiter is ';'")

mycsvfile = sys.argv[1]

if len(sys.argv)==2:
    mydel = ';'
else:
    mydel=sys.argv[2]

listparticipants = open('liste_participants.tex','w')
t = string.Template('\\textbf{ $LAST $FIRST } (\\email{ $EMAIL })\\\\\n')

listparticipants.write('\\section*{\\Large\\bf  List of participants}\n\n\\vskip 35truemm\n\n')

with open(mycsvfile, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=mydel)
    seen = []
    for row in reader:
        ff=str(row['First Name'])+'|'+str(row['Last Name'])+'|'+str(row['Email'])
        if not ff in seen:
            seen.append(ff)
            ## TO DO test First Name to add a capital letter for each name
            myline = t.substitute(FIRST=format_name(row['First Name']),LAST = row['Last Name'].upper(), EMAIL = row['Email'])
            listparticipants.write(myline)

listparticipants.close()
csvfile.close()


