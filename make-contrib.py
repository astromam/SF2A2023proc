#!/usr/bin/python
# -*- coding: latin-1 -*-
# This program compiles the tex files of the individual contributions
# from the file book-setup.py
# It runs the sequence pdflatex,bibtex,pdflatex,pdflatex
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

# Test for Python version
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3+, your system is using Python "+str(sys.version_info[0]))

# Open setup file
with open("book-setup.py") as myf:
    code = compile(myf.read(), "book-setup.py", 'exec')
    exec(code)

#  Open file handle for logs
log = open('make-contrib.log','w')

# Start actual work
wd = os.getcwd() # get current directory
mypattern = re.compile(r'^S\d+$')
print(mypattern)

list_error=[]

for num in range(len(sessions)):
    session = sessions[num]
    session_name = list(session.keys())[0]
    print("----------------------------------------")
    print(session_name)
    print("----------------------------------------")
    log.write("----------------------------------------\n")
    log.write(session_name+'\n')
    log.write("----------------------------------------\n")

    session_num = list(session.values())[0][0]
    print(list(session.values())[0])
        
    for nom in list(session.values())[0]:
        print(f'\nnom: {nom}')
        match = mypattern.match(nom)
        print(f'match: {match}')
        
        # Composition des noms de fichiers
        if match:
            path = 'contrib/' + session_num 
            filebase = 'contrib/' + session_num + '/' + nom
            bibtex = False
        else:
            path = 'contrib/' + session_num + '/' + nom
            filebase = 'contrib/' + session_num + '/' + nom + '/' + nom
            bibtex = True
           

        print('Processing '+filebase)
        log.write('Processing '+filebase+'\n')
        fullpath  = wd +'/'+path
        print(f'fullpath: {fullpath}')

        # copying bst and cls files to location
        process = subprocess.run(['cp', bstfile, fullpath+'/.'])
        process = subprocess.run(['cp', clsfile+'.cls', fullpath+'/.'])

        # from that point onwards, we are always working in the directory of the tex files
        os.chdir(fullpath)
        log.write('Changing to directory '+fullpath+'\n')
        
        process = subprocess.run(['pdflatex', nom],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        if process.stderr:
            print('Error while processing '+filebase+' using pdflatex \nCheck compilation manually:\n')
            print(process.stderr)
            log.write('Error while processing '+filebase+' using pdflatex \nCheck compilation manually:\n')
            log.write(process.stderr+'\n')
            list_error.append(filebase)
            continue
        else:
            print('pdflatex ok')
            log.write('pdflatex ok \n')

        if bibtex:
            bibpath = Path(nom+'.bib')
            if bibpath.is_file():
                process = subprocess.run(['bibtex', nom],
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE,
                                         universal_newlines=True,
                                         cwd=wd+'/'+path)
                if process.stderr:
                    print('Error while processing '+filebase+' using bibtex \nCheck compilation manually:\n')
                    print(process.stderr)
                    log.write('Error while processing '+filebase+' using bibtex \nCheck compilation manually:\n')
                    log.write(process.stderr+'\n')
                    list_error.append(filebase)
                    continue
                else:
                    print('Bibtex ok')
                    log.write('Bibtex ok\n')
            else:
                print('No bibtex file')
                log.write('No bibtex file\n')
                
        process = subprocess.run(['pdflatex', nom],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True,
                                 cwd=wd+'/'+path)
        if process.stderr:
            print('Error while processing '+filebase+' using pdflatex \nCheck compilation manually:\n')
            print(process.stderr)
            log.write('Error while processing '+filebase+' using pdflatex n2\nCheck compilation manually:\n')
            log.write(process.stderr+'\n')
            list_error.append(filebase)
            continue
        
        process = subprocess.run(['pdflatex', nom],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True,
                                 cwd=wd+'/'+path)
        if process.stderr:
            print('Error while processing '+filebase+' using pdflatex \nCheck compilation manually:\n')
            print(process.stderr)
            log.write('Error while processing '+filebase+' using pdflatex n3\nCheck compilation manually:\n')
            log.write(process.stderr+'\n')
            list_error.append(filebase)
            continue

if len(list_error):
    print("We have encountered some errors while processing the contributions\nPlease check the following directories (more information in the logfile make-contrib.log):\n")
    for contrib in list_error:
        print(contrib+'\n')
else:
    print("Apparently no errors were reported! Good news!\n Check the logfile make-contrib.log anyway...\n")
log.close()
