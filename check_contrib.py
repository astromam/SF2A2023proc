#!/Users/siebert/anaconda3/envs/astroconda/bin/python
# -*- coding: latin-1 -*-
# This program verifies the latex contribution
#   - checks the proper formatting of the authors names
#   - checks the names of the figures
#   - checks the encoding of the text (no non standard ascii)
#   - checks the number of pages
#
# Usage: python check_contrib SXX author
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
import shutil
from pathlib import Path
import unicode2latex as u2l

class bcolors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    
def check_author(s):
    '''
    Check the author encoding in string s: must be A.~B.~C. Name
    Based on extract_names in sf2a_utils.py
    '''
    # extract the name
    a = extract('author',s)
    a = re.sub(r'\$.*\$',"",a)
    a = re.sub(r"^ {1,}","",re.sub(r" {1,}$","",a)) # on enleve les blancs à la fin et aux débuts


    team = re.compile(r'^the .*|.* team( ,)*|.* teams( ,)|.* consortium( ,)*|.*\\consortium{.*}.*|.* group( ,)*',re.I)
    a3 = re.match('([A-Z]\..*[A-Z]\..*[A-Z]\.)(.*)',a) # 3 prenoms
    a2 = re.match('([A-Z]\..*[A-Z]\.)(.*)',a) # 2 prenoms
    a1 = re.match('([A-Z]\.)(.*)',a) # 1 prenoms
    if(a3):
        surname = a3.group(2)
        names = a3.group(1)
    elif(a2):
        surname = a2.group(2)
        names = a2.group(1)
    elif(a1):
        surname = a1.group(2)
        names = a1.group(1)
    elif team.match(a):
        surname = a
        names = ''
    else: # does not match the standard naming convention for SF2A proceedings, try to correct it
        mylist = a.split()
        n = len(mylist)
        surname = mylist[n-1]
        names=[]
        for i in range(n-1):
            prenom = list(mylist[i])
            initial = prenom[0].upper()+'.'
            for k in range(len(prenom)):
                if prenom[k]=='-':
                    initial = initial+prenom[k]+prenom[k+1].upper()+'.'
                #elif prenom[k]=='\.' and k<(len(prenom)-1):
                #    initial.append('~')
                #    initial.append(prenom[k+1])
                 
            names.append(initial)
        names=names[0]

    # Remove whitespace and tildes at the beginning of the strings and try to conform to the required format
    # this should be done in a cleaner way
    surname = re.sub(r"^~{1,}","",surname)
    surname = re.sub(r"^ {1,}","",surname)
    regexp = re.compile(r"\\\,",re.DOTALL)
    names = regexp.sub("",names)
    regexp = re.compile(r"\.",re.DOTALL)
    names = regexp.sub(".~",names)
    names = re.sub(r" {1,}$","",names)
    names = re.sub(r"\s","",names)
    names = re.sub(r"~$","",names)
    names = re.sub(r"\.~-",".-",names)
    names = re.sub(r"~~","~",names)

    corrected_name= names+" "+surname
    if corrected_name != a:
        return corrected_name
    else:
        return 'OK'

def check_pagecounter(myfile):
    '''
    Checks that \setcounter{page}{xxx} is there
    '''

    found = False
    regexp = re.compile(r'\\setcounter{page}{(.*)}')
    idx = re.search(regexp,myfile)
    if idx is not None:
        found = True
    return found
    

def check_pages(myfile):
    '''
    Checks that the number of pages matches the size allowed for the contribution
    '''
    regexp = re.compile(r'\\setcounter{page}{*}')
    res = re.findall(regexp,myfile)
    print(res)


def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(^%.*?\n|^%%.*?\n)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)


#-----------------------------------------
if __name__ == "__main__":
    
    # Test for Python version
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3+, your system is using Python "+str(sys.version_info[0]))

    # reconstruct file name from arguments
    session = sys.argv[1]
    author = sys.argv[2]

    mydir = 'contrib/'+session+'/'+author+'_'+session+'/'
    contribution = mydir+author+'_'+session+'.tex'
    bibtexname = author+'_'+session
    filename = author+'_'+session+'.tex'
    logfile = author+'_'+session+'.log'
    backup_dir = mydir+'orig'

    if Path(contribution).is_file():
        print ("Checking ",contribution)
    else:
        raise Exception(f"{bcolors.FAIL}"+contribution+f" is not found on your system{bcolors.ENDC}")
        

    # check for existence of a backup in orig, if not creates a copy of the contribution
    if not Path(backup_dir).is_dir():
        print('\n - No backup found, creating backup')
        os.makedirs(backup_dir)
        shutil.copy2(contribution,backup_dir)
        tmp = mydir+author+'_'+session+'.bib'
        if Path(tmp).is_file():
            shutil.copy2(tmp,backup_dir)
        else:
            print(f"{bcolors.WARNING}No bibtex file found!{bcolors.ENDC}")

        k=0
        for i in range(10):
            j= i+1
            tmp = mydir+author+'_fig'+str(j)+'.pdf'
            if Path(tmp).is_file():
                # copy file with figure to backup
                shutil.copy2(tmp,backup_dir)
                # check the size if not too large
                k=k+1
        if k==0:
            print(f"{bcolors.WARNING}Found no figure associated with the contribution.\
            Please check that the naming convention is ok{bcolors.ENDC}")
        else:
            print(f"{bcolors.OK}Found "+str(k)+f" figures associated to the contribution{bcolors.ENDC}")
        
    # Load tex file
    with open(contribution,'r') as t:
        ts = t.read()
    t.close()
    id = identification(ts)

    # remove all comments
    ts = remove_comments(ts)
        
    # check if \setcounter{page}{3} is present
    print('\n- Checking for \setcounter{page}{}')
    if check_pagecounter(ts):
        print(f"{bcolors.OK}Page counter found, ok{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}Error : \\setcounter{page}{3} missing! This will cause failure in make-book.py{bcolors.ENDC}")
    
    # check author names
    print('\n- Checking authors\' names\nAuthors identified in the contribution:')
    auteurs = re.compile(r'\\author{.*}')
    #auteurs = id['auteurs']
    for name in auteurs.findall(ts):
        newname=check_author(name)
        a = extract('author',name)
        a = re.sub(r'\$.*\$',"",a)
        a = re.sub(r"^ {1,}","",re.sub(r" {1,}$","",a)) # on enleve les blancs à la fin et aux débuts

        if newname == 'OK':
            line = f"{bcolors.OK}" + a + f" OK {bcolors.ENDC}"
            print(line)
        else:
            line = f"{bcolors.FAIL}" + a + " changed to " + newname + f" {bcolors.ENDC}"
            print(line)
            ts = re.sub(a,newname,ts)


    # Check encoding and transforms to pure latex
    print('\n- Changing all accentuated characters to plain latex\nIf any red comment, please search for the character(s) manually and replace them adequately ')
    translation_table = {}

    for line in open('utf8ienc.dtx'):
        m = re.match(r'%.*\DeclareUnicodeCharacter\{(\w+)\}\{(.*)\}', line)
        if m:
            codepoint, latex = m.groups()
            latex = latex.replace('@tabacckludge', '') # remove useless (??) '@tabacckludge'
            translation_table[int(codepoint, 16)] = str(latex)

    ts = ts.translate(translation_table)
    res = u2l.uni2tex(ts)
    #print(res)
    

    # Test compile and check the number of pages of the contribution
    # overwrites file with corrected version
    with open(contribution,'w') as t:
        t.write(res)
    t.close()

    # change dir to location of the contribution
    os.chdir(mydir)
        
    # first passage with pdflatex
    print('- First pass with pdflatex')
    process = subprocess.run(['pdflatex', filename],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
    if process.stderr:
        line = f"{bcolors.FAIL}Error while processing "+filename+f" using pdflatex \nCheck compilation manually:\n{bcolors.ENDC}"
        raise Exception(line)
        print(process.stderr)
        
    # look for bibtex entry and run bibtex if exists
    if Path(bibtexname+'.bib').is_file():
        print ("\n- Checking for ",bibtexname)

        print('\n- Running bibtex')
        process = subprocess.run(['bibtex', bibtexname],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)

        if process.stderr:
            line = f"{bcolors.FAIL}Error while processing "+bibtexname+f" using bibtex \nCheck compilation manually:\n{bcolors.ENDC}"
            raise Exception(line)
            print(process.stderr)
    

        # second and third passage with pdflatex
        print('\n- Second and third pdflatex runs')
        process = subprocess.run(['pdflatex', filename],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        if process.stderr:
            line = f"{bcolors.FAIL}Error while processing "+filename+f" using pdflatex \nCheck compilation manually:\n{bcolors.ENDC}"
            raise Exception(line)
            print(process.stderr)

        process = subprocess.run(['pdflatex', filename],
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        if process.stderr:
            line = f"{bcolors.FAIL}Error while processing "+filename+f" using pdflatex \nCheck compilation manually:\n{bcolors.ENDC}"
            raise Exception(line)
            print(process.stderr)
    else:
        print(f"{bcolors.WARNING}"+bibtexname+f" is not found on your system{bcolors.ENDC}")


    # look in logs for the number of pages of the contribution
    log = open(logfile,"r")
    pattern = "Output written on"
    for line in log:
        if re.search(pattern,line):
            npages = re.search(r'\(\d+ pages, \d+ bytes\)',line)
    print('- Number of pages and size : ',npages.group())
    
    print("Done")
    
