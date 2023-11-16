#!/usr/bin/python
# -*- coding: latin-1 -*-
# This program generates an input file for a latex document in order
# to generate accurate index and TOC for proceedings
# It is primarily meant for the SF2A 2004 proceedings
# Copyright (C)  2004  Frédéric Meynadier (Frederic.Meynadier@obspm.fr)
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
# Major modifications performed by R. Samadi 22.Dec.2010
# Modification for python3 by A. Siebert 8.Oct.2021


import string
import re
from sf2a_utils import *
import os
import re
import sys
import codecs

# Test for Python version
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3+, your system is using Python "+str(sys.version_info[0]))

# Read setup file
with open("book-setup.py") as myf:
    code = compile(myf.read(), "book-setup.py", 'exec')
    exec(code)

# Open file handles for outputs
outputlist = open('included.list','w')
outputpdf = open('inputpdf.tex','w')
outputads = open('abstracts_ads.txt','w')
outputhtml = open('index.html','w')

page = start_page

# Header for ADS file
entete = '%%R '+year+'sf2a.conf.....S\n'\
         '%%T SF2A-'+year+": Semaine de l'Astrophysique Francaise\n"\
         '%%A '+editeurs+'\n'\
         '%%J SF2A-'+year+': Proceedings of the Annual meeting of the French Society of Astronomy and Astrophysics. Eds.: '+editeurs+'\n'\
         '%%D 12/'+year+'\n'\
         '%%U '+urlbase_proc+'book.pdf\n'\
         '%%B Abstract (optional description of the proceeding) - None\n\n\n'
         
outputads.write(entete)

string="<H2 id=contrib>Contributions by sessions:</H2>\n"
outputhtml.write(string)
for num in range(len(sessions)):
    session = sessions[num]
    name = list(session.keys())[0]
    delatex2html(name)
    string="<li> <a href=#"+str(num)+ ">" + name +  "</a></li>\n"
    outputhtml.write(string)

string="\n"
outputhtml.write(string)

list_to_update=[]

doupdate = 0 # if =1 -> one or several contribution must be re-compiled 
mypattern = re.compile(r'^S\d+$')

for num in range(len(sessions)):
    session = sessions[num]
    session_name = list(session.keys())[0]
    print("----------------------------------------")
    print(session_name)
    print("----------------------------------------")
    # Générer l'entrée dans la TOC pour les parties (programmes)
    string = '\n\phantomsection\n\\addcontentsline{toc}{part}{' + session_name + '}\n'
    outputpdf.write(string)

    string="<h2 id=" + str(num) +">"+ delatex2html(session_name) +" </h2>\n"
    outputhtml.write(string)

    session_num = list(session.values())[0][0]
        
    for nom in list(session.values())[0]:        
        # Check if a session (True) or a contribution (False) 
        match = mypattern.match(nom)
        
        # Set base directory
        print(f'match: {match}')
        if match:
            filebase = 'contrib/' + session_num + '/' + nom
        else :
            filebase = 'contrib/' + session_num + '/' + nom + '/' + nom
        print(filebase)
        
        with  open(filebase + '.log','r',encoding='latin-1') as p:
            log = p.read()
        p.close()
        
        with open(filebase + '.tex','r') as t:
            ts = t.read()
        t.close()
        
        # Create bibcode -> must be 19 characters by definition (was 18 previously)
        contrib_id = year+ 'sf2a.conf.' + ('%d%s' % (page,nom[0].upper()) ).rjust(4,'.')
        print(contrib_id, nom)

	# Composition des liens relatifs (plus rapide pour la liste)
	# urlbase = './'+year+'/'
        # pdflink = urlbase + contrib_id + '.pdf'

	# Composition des liens absolus (pour ADS)
        urlbase_abs = urlbase_proc
        pdflink_abs = urlbase_abs + contrib_id + '.pdf'
        
        # Substitution du numéro de la page dans le fichier tex
        # ' --> *_final.tex
        regexp = re.compile(r'\\setcounter{page}{(.*)}')
        pagei = re.findall(regexp,ts)[0]
        if(int(pagei) != page ):
            doupdate= 1
            print("\tWe must change the page counter (setcounter) in " + nom)
            print("\tprevious value = ",pagei)
            print("\tnew      value = ",page)
            s = "sed -ibak 's/\\\setcounter{page}{.*}/\\\setcounter{page}{"+str(page)+"}/' "+filebase+".tex"
            list_to_update.append(nom)
            os.system(s)


        s= "\ln -sf "+nom+".pdf contrib/"+contrib_id+".pdf"
        os.system(s)
        s= "\ln -sf "+nom+".pdf contrib/"+contrib_id+".pdf"
        os.system(s)

	# extraction des infos (titre, auteurs, liste des index)
        id = identification(ts)
        # extraction du nombre de pages du PDF
        n = nombre_pages(log)

        if (id['titre'] != 'NOTINTOC') :
            outputlist.write(nom+'\n')

        auteurs= id['auteurs']
        s=auteurs.split(',')
        auteurs=s[0]
        na=min([len(s),10])
        # print first 10 authors
        for line in s[1:na-1]:
            auteurs = auteurs + ", " + line

        # append et al if more than 10 authors, otherwise just end with the last one
        if(len(s)>10):
            auteurs=auteurs  + ', ' + s[na-1] +', et al.'
        else:
            if(len(s)>1):
                auteurs=auteurs  + ", and " + s[na-1]


        if (id['titre'] != 'NOTINTOC') :
            string = '<li><a href='  + pdflink_abs  + '>"' +  delatex2html(id['titre']) + '"</a>, ' + delatex2html(auteurs) +'</li>\n'
            outputhtml.write(string)


        if (id['titre'] != 'NOTINTOC') :
            string = '\phantomsection\n\\tocline{' + id['titre'] + '}{' + auteurs + '}\n'
            outputpdf.write (string)
            for ind in id['index']:
                #here clean index which is the authors name and initials
                outputpdf.write('\\index{' + ind + '}\n')

            # Insertion dans le fichier pour ADS
            string = '%%P %d\n' % page\
                     +'%%L %d\n' % (page+n-1)\
                     +'%%T %s\n' % id['titre']\
                     +'%%A %s\n' % id['auteurs_ads']\
                     +'%%U %s\n' % pdflink_abs\
                     +'%%B %s\n' % abstract(ts)\
                     +'%%K %s\n' % keywords(ts)

            # extraction des references
            s=references(ts,filebase)
            if(s != ''):
                string = string + '%Z ' + s + "\n"

            string = string +"\n"
           
            outputads.write(string)

        outputpdf.write('\includepdf[pages=-]{'+filebase+'.pdf}\n')

        # si le nb de page est impair on ajoute une page vide
        if(n%2 !=0):
            outputpdf.write('\n\\cleardoublepage\n')
            page = page +1

        
        # Incrémentation du numéro de page avant de passer au suivant
        page += n

        if(NOCONTRIB ==1):
            break


outputlist.close()
outputpdf.close()
outputads.close()
outputhtml.close()

if(doupdate):
    string="Warning ! Warning !\nThe page counter of one or several contributions have been modified:\n"
    print(string)
    for contrib in list_to_update:
        print(contrib+'\n')
    string="Shall we re-compile them by executing the command 'make-contrib.py' and reprocess all contributions ? [y/n]\n"
    print(string)
    sys.stderr.write(string)
    a=getchar()
    if( a == 'y' or a =='Y'):
        os.system("./make-contrib.py")
    else:
        exit(1)
