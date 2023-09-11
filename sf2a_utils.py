# -*- coding: latin-1 -*-

import string
import re
import sys
from sf2a_utils import *
import sys, tty, termios
import os
import shutil, tempfile

def sed_inplace(filename, pattern, repl):
    '''
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
    '''
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(repl, line))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)

def getchar():
    ch=None
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def PdfpagesFormat(nomfichier):
    # transforme le nom de fichier au format pdfpages-friendly (un seul '.')
    tmp = string.replace(nomfichier,'.','_')
    return tmp

def extract_names(s):
    
    a3 = re.match('([A-Z]\..*[A-Z]\..*[A-Z]\.)(.*)',s) # 3 prenoms
    a2 = re.match('([A-Z]\..*[A-Z]\.)(.*)',s) # 2 prenoms
    a1 = re.match('([A-Z]\.)(.*)',s) # 1 prenoms
    if(a3):
        surname = a3.group(2)
        names = a3.group(1)
    elif(a2):
        surname = a2.group(2)
        names = a2.group(1)
    elif(a1):
        surname = a1.group(2)
        names = a1.group(1)
    else:
        surname = ''
        names = ''
    surname = re.sub(r"^~{1,}","",surname)
    surname = re.sub(r"^ {1,}","",surname)
    names = re.sub(r" {1,}$","",names)
    return (names,surname)
    

def extract(commande,fichier):
    # On cherche le début de la commande
    debut = fichier.find('\\'+commande+'{')
    # On tronque le fichier
    fichier = fichier[debut + len(commande) + 2:]
    balance = 1
    pas = 0
    while (balance != 0):
        if fichier[pas] == '{' :
            balance +=1
        if fichier[pas] == '}':
            balance -= 1
        pas += 1
    return fichier[:pas-1]

def abstract(fichier):
    buffer=''
    regexp = re.compile(r'[^%]\\begin{abstract}(.*)\\end{abstract}',re.DOTALL)
    try:
        a = re.findall(regexp,fichier)[0]
        a=a.split('\n')
        for line in a:
            line=re.sub(re.compile(r'\r{1,}'),r"",line) # on vire les caractères \r (générés sous Windows)
            # on vire les lignes commentees
            regexp = re.compile(r'^%.*',re.DOTALL)
            line = regexp.sub('',line)
            regexp = re.compile(r'[^\\]%.*',re.DOTALL)
            line = regexp.sub('',line)
            if(len(line)>0):
                buffer=buffer+ line +' '
        
#        regexp = re.compile(r'\n{1,}')
#        buffer = regexp.sub(' ',buffer)

        # on enleve les espaces repetes
        regexp = re.compile(r' {2,}')
        buffer = regexp.sub(' ',buffer)

        # on supprime l'espace eventuel qui serait place à la fin 
        regexp = re.compile(r' $')
        buffer = regexp.sub('',buffer)
     
        # on supprime l'espace eventuel qui serait place au début
        regexp = re.compile(r'^ ')
        buffer = regexp.sub('',buffer)
 
    except IndexError:
        buffer = ''
    return buffer

def keywords(fichier):
    buffer=''
    regexp = re.compile(r'[^%]\\begin{keywords}(.*)\\end{keywords}',re.DOTALL)
    try:
        a = re.findall(regexp,fichier)[0]
        a=a.split('\n')
        for line in a:
            line=re.sub(re.compile(r'\r{1,}'),r"",line) # on vire les caractères \r (générés sous Windows)
            # on vire les lignes commentees
            regexp = re.compile(r'^%.*',re.DOTALL)
            line = regexp.sub('',line)
            regexp = re.compile(r'[^\\]%.*',re.DOTALL)
            line = regexp.sub('',line)
            buffer=buffer+line
    except IndexError:
        buffer = ''
    return buffer

    
def nombre_pages(fichier):
    regexp = re.compile('Output written on.*\((.*)page.')
    list = re.findall(regexp,fichier)
    return int(list[0])

def references(fichier,fullpathtofile):
    regexp = re.compile(r'[^%]\\begin{thebibliography}(.*)\\end{thebibliography}',re.DOTALL)
    buffer = re.findall(regexp,fichier)
    if(len(buffer) == 0):
        # pas de références dans le fichier tex
        # on regarde si le fichier contrib/nom.bbl contient les références
        if(fullpathtofile != ''):
            if( os.access(fullpathtofile + '.bbl',os.F_OK) ):
                t = open(fullpathtofile + '.bbl',"r")
                ts = t.read ()
                t.close()
                regexp = re.compile(r'\\begin{thebibliography}(.*)\\end{thebibliography}',re.DOTALL)
                buffer = re.findall(regexp,ts)
        if(len(buffer) == 0): # aucunes références, on retourne une chaine vide
            return ''

    buffer=buffer[0]
    
    # on vire les lignes commentees
    regexp = re.compile(r'^%.*')
    buffer = regexp.sub('',buffer)
    regexp = re.compile(r'[^\\]%.*')
    buffer = regexp.sub('',buffer)

    # on vire les retours a la ligne 
    regexp = re.compile(r'\\\\',re.DOTALL)
    buffer = regexp.sub('',buffer)
    regexp = re.compile(r'\n',re.DOTALL)
    buffer = regexp.sub('',buffer)
    # on vire les caractères \r (générés sous Windows)
    regexp = re.compile(r'\r{1,}',re.DOTALL)
    buffer = regexp.sub('',buffer)
    a =  buffer.split('\\bibitem')
    if(len(a)<2):
        return ''
    buffer = ''
    for line in a[1:]:
        #        a=re.sub(re.compile(r'\[.*\]'),r"",line)
        pos=line.find(']')
        if(pos > -1):
            line=line[pos+1:]
        pos=line.find('}')
        if(pos > -1):
            line=line[pos+1:]
        # on supprime les tabulations
        line = re.sub('\t{1,}','',line)
        # on supprime les espaces eventuels qui seraient placés à la fin
        line = re.sub(r' {1,}$','',line)
        # on supprime les espaces eventuels qui seraient placés au début
        line = re.sub(r'^ {1,}','',line)

        buffer=buffer + line +'\n'
#        a=re.sub(re.compile(r'^\{[a-zA-Z0-9\.\_]{0,}\}'),r"",a)
#        print line


    # on enleve les espaces repetes
    regexp = re.compile(r' {2,}')
    buffer = regexp.sub(' ',buffer)
        
    return buffer
  
def identification(fichier):
    #
    # Handle title
    #
    titre = extract('title',fichier)

    # on vire les footnotes eventuelles
    regexp = re.compile(r'\\footnote{.*}',re.DOTALL)
    titre = regexp.sub('',titre)

    # on vire les $^()$
    regexp = re.compile(r'\$\^.*\$',re.DOTALL)
    titre = regexp.sub('',titre)
    # on vire les retours a la ligne 
    regexp = re.compile(r'\\\\',re.DOTALL)
    titre = regexp.sub('',titre)

    titre=re.sub(re.compile(r'\r{1,}',re.DOTALL),r"",titre) # on vire les caractères \r (générés sous Windows)
    titre=re.sub(re.compile(r' {1,}$',re.DOTALL),r"",titre) # on vire les espaces à la fin
    titre=re.sub(re.compile(r'^ {1,}',re.DOTALL),r"",titre) # on vire les espaces au début

    #
    # Handle authors list: list, index and ADS
    #
    auteurs = ''
    n = 0
    auteurs_liste = []
    for s in re.findall(re.compile(r'[^\%](\\author{.*})'),fichier) :
        a = extract('author',s)
        a = re.sub(r'\$.*\$',"",a)
        a = re.sub(r"^ {1,}","",re.sub(r" {1,}$","",a)) # on enleve les blancs à la fin et aux débuts
        if (n>0):
            auteurs += ','
        auteurs += a
        auteurs_liste.append(a)
        n += 1
    
    auteurs_ads = ''
    index = []
    if(n >0):
        consortium = re.compile(r'.* collaboration*| .* team( ,)*|.* teams( ,)|.* consortium( ,)*|.*\\consortium{.*}.*|.* group( ,)*',re.I)
        # loop over all authors
        for i in range(0,n):
            # un consortium ne sera pas ajoute dans l'index, ni dans la liste d'entrees pour ADS
            if(not consortium.match(auteurs_liste[i])):
                (names,surname) = extract_names(auteurs_liste[i])
                names=re.sub(re.compile(r'\.([A-Z])\.'),r".~\1.",names) # On rajoute un tilde entre les intiales: A.L. -> A.~L.
                auteurs_ads += surname + ' ' + names
                index.append(surname+", "+names )
                #                print surname+","+ names
            
                if(i < n-1):
                    auteurs_ads +=  '; '
                
    return {'titre':titre,'auteurs':auteurs,'index':index,'auteurs_ads':auteurs_ads}

def set_page(fichier,numero):
    regexp = re.compile(r'\\setcounter{page}{([^}])*}')
    fichier = regexp.sub(r'\\setcounter{page}{'+str(numero)+'}',fichier)
    return fichier

def delatex(chaine):
    chaine = re.sub(r"\\'a","á",chaine)
    chaine = re.sub(r"\\'e","é",chaine)
    chaine = re.sub(r"\\'{e}","é",chaine)
    chaine = re.sub(r"\\'i","í",chaine)
    chaine = re.sub(r"\\'\\i","í",chaine)
    chaine = re.sub(r"\\'o","ó",chaine)
    chaine = re.sub(r"\\'u","ú",chaine)
    chaine = re.sub(r"\\'A","Á",chaine)
    chaine = re.sub(r"\\'E","É",chaine)
    chaine = re.sub(r"\\'I","Í",chaine)
    chaine = re.sub(r"\\'\\I","Í",chaine)
    chaine = re.sub(r"\\'O","Ó",chaine)
    chaine = re.sub(r"\\'U","Ú",chaine)
    chaine = re.sub(r"\\`a","à",chaine)
    chaine = re.sub(r"\\`e","è",chaine)
    chaine = re.sub(r"\\`i","ì",chaine)
    chaine = re.sub(r"\\`o","ò",chaine)
    chaine = re.sub(r"\\`u","ù",chaine)
    chaine = re.sub(r"\\`A","À",chaine)
    chaine = re.sub(r"\\`E","È",chaine)
    chaine = re.sub(r"\\`I","Ì",chaine)
    chaine = re.sub(r"\\`O","Ò",chaine)
    chaine = re.sub(r"\\`U","Ù",chaine)
    chaine = re.sub(r"\\\"a","ä",chaine)
    chaine = re.sub(r"\\\"e","ë",chaine)
    chaine = re.sub(r"\\\"\\i","ï",chaine)
    chaine = re.sub(r"\\\"i","ï",chaine)
    chaine = re.sub(r"\\\"o","ö",chaine)
    chaine = re.sub(r"\\\"u","ü",chaine)
    chaine = re.sub(r"\\\"A","Ä",chaine)
    chaine = re.sub(r"\\\"E","Ë",chaine)
    chaine = re.sub(r"\\\"I","Ï",chaine)
    chaine = re.sub(r"\\\"O","Ö",chaine)
    chaine = re.sub(r"\\\"U","Ü",chaine)		    
    chaine = re.sub(r"\\\^a","â",chaine)
    chaine = re.sub(r"\\\^e","ê",chaine)
    chaine = re.sub(r"\\\^i","î",chaine)
    chaine = re.sub(r"\\\^o","ô",chaine)
    chaine = re.sub(r"\\\^u","û",chaine)
    chaine = re.sub(r"\\\^A","Â",chaine)
    chaine = re.sub(r"\\\^E","Ê",chaine)
    chaine = re.sub(r"\\\^I","Î",chaine)
    chaine = re.sub(r"\\\^O","Ô",chaine)
    chaine = re.sub(r"\\\^U","Û",chaine)
    chaine = re.sub(r"\\c{c}","ç",chaine)
    chaine = re.sub(r"\\\\","",chaine)
    chaine = re.sub(r"~"," ",chaine)
    chaine = re.sub(r"\\&","&",chaine)
    
    chaine = re.escape(chaine)
    return chaine
    
def delatex2latex(chaine):
    '''
    Replaces special caracters by their latex equivalent in string chaine
    '''
    chaine = re.sub("á",r"\\'a",chaine)
    chaine = re.sub("é",r"\\'e",chaine)
#    chaine = re.sub("é",r"\\'{e}",chaine)
    chaine = re.sub("í",r"\\'{\\i}",chaine)
#    chaine = re.sub(r"\\'\\i","í",chaine)
    chaine = re.sub("ó",r"\\'o",chaine)
    chaine = re.sub("ú",r"\\'u",chaine)
    chaine = re.sub("Á",r"\\'A",chaine)
    chaine = re.sub("É",r"\\'E",chaine)
    chaine = re.sub("Í",r"\\'I",chaine)
    chaine = re.sub("Í",r"\\'\\I",chaine)
    chaine = re.sub("Ó",r"\\'O",chaine)
    chaine = re.sub("Ú",r"\\'U",chaine)
    chaine = re.sub("à",r"\\`a",chaine)
    chaine = re.sub("è",r"\\`e",chaine)
    chaine = re.sub("ì",r"\\`i",chaine)
    chaine = re.sub("ò",r"\\`o",chaine)
    chaine = re.sub("ù",r"\\`u",chaine)
    chaine = re.sub("À",r"\\`A",chaine)
    chaine = re.sub("È",r"\\`E",chaine)
    chaine = re.sub("Ì",r"\\`I",chaine)
    chaine = re.sub("Ò",r"\\`O",chaine)
    chaine = re.sub("Ù",r"\\`U",chaine)
    chaine = re.sub("ä",r"\\\"a",chaine)
    chaine = re.sub("ë",r"\\\"e",chaine)
    chaine = re.sub("ï",r"\\\"{\\i}",chaine)
    chaine = re.sub("ï",r"\\\"i",chaine)
    chaine = re.sub("ö",r"\\\"o",chaine)
    chaine = re.sub("ü",r"\\\"u",chaine)
    chaine = re.sub("Ä",r"\\\"A",chaine)
    chaine = re.sub("Ë",r"\\\"E",chaine)
    chaine = re.sub("Ï",r"\\\"I",chaine)
    chaine = re.sub("Ö",r"\\\"O",chaine)
    chaine = re.sub("Ü",r"\\\"U",chaine)		    
    chaine = re.sub("â",r"\\^a",chaine)
    chaine = re.sub("ê",r"\\^e",chaine)
    chaine = re.sub("î",r"\\^{\\i}",chaine)
    chaine = re.sub("ô",r"\\^o",chaine)
    chaine = re.sub("û",r"\\^u",chaine)
    chaine = re.sub("Â",r"\\^A",chaine)
    chaine = re.sub("Ê",r"\\^E",chaine)
    chaine = re.sub("Î",r"\\^I",chaine)
    chaine = re.sub("Ô",r"\\^O",chaine)
    chaine = re.sub("Û",r"\\^U",chaine)
    chaine = re.sub("ç",r"\\c{c}",chaine)
    
    #chaine = re.escape(chaine)
    return chaine
    

def delatex2html(chaine):
    chaine = re.sub(r"\\lowercase","",chaine)
    chaine = re.sub(r"\\'a","á",chaine)
    chaine = re.sub(r"\\'e","é",chaine)
    chaine = re.sub(r"\\'{e}","é",chaine)
    chaine = re.sub(r"\\'i","í",chaine)
    chaine = re.sub(r"\\'\\i","í",chaine)
    chaine = re.sub(r"\\'o","ó",chaine)
    chaine = re.sub(r"\\'u","ú",chaine)
    chaine = re.sub(r"\\'A","Á",chaine)
    chaine = re.sub(r"\\'E","É",chaine)
    chaine = re.sub(r"\\'I","Í",chaine)
    chaine = re.sub(r"\\'\\I","Í",chaine)
    chaine = re.sub(r"\\'O","Ó",chaine)
    chaine = re.sub(r"\\'U","Ú",chaine)
    chaine = re.sub(r"\\`a","à",chaine)
    chaine = re.sub(r"\\`e","è",chaine)
    chaine = re.sub(r"\\`i","ì",chaine)
    chaine = re.sub(r"\\`o","ò",chaine)
    chaine = re.sub(r"\\`u","ù",chaine)
    chaine = re.sub(r"\\`A","À",chaine)
    chaine = re.sub(r"\\`E","È",chaine)
    chaine = re.sub(r"\\`I","Ì",chaine)
    chaine = re.sub(r"\\`O","Ò",chaine)
    chaine = re.sub(r"\\`U","Ù",chaine)
    chaine = re.sub(r"\\\"a","ä",chaine)
    chaine = re.sub(r"\\\"e","ë",chaine)
    chaine = re.sub(r"\\\"\\i","ï",chaine)
    chaine = re.sub(r"\\\"i","ï",chaine)
    chaine = re.sub(r"\\\"o","ö",chaine)
    chaine = re.sub(r"\\\"u","ü",chaine)
    chaine = re.sub(r"\\\"A","Ä",chaine)
    chaine = re.sub(r"\\\"E","Ë",chaine)
    chaine = re.sub(r"\\\"I","Ï",chaine)
    chaine = re.sub(r"\\\"O","Ö",chaine)
    chaine = re.sub(r"\\\"U","Ü",chaine)		    
    chaine = re.sub(r"\\\^a","â",chaine)
    chaine = re.sub(r"\\\^e","ê",chaine)
    chaine = re.sub(r"\\\^i","î",chaine)
    chaine = re.sub(r"\\\^o","ô",chaine)
    chaine = re.sub(r"\\\^u","û",chaine)
    chaine = re.sub(r"\\\^A","Â",chaine)
    chaine = re.sub(r"\\\^E","Ê",chaine)
    chaine = re.sub(r"\\\^I","Î",chaine)
    chaine = re.sub(r"\\\^O","Ô",chaine)
    chaine = re.sub(r"\\\^U","Û",chaine)
    chaine = re.sub(r"\\c{c}","ç",chaine)
    chaine = re.sub(r"\\\w{1,}{","",chaine)
    chaine = re.sub(r"\\:"," ",chaine)
    chaine = re.sub(r"\\\\","",chaine)
    chaine = re.sub(r"\\\~\{n\}","&ntilde;",chaine)
    chaine = re.sub(r"~"," ",chaine)
    chaine = re.sub(r"\\sim","~",chaine)
    chaine = re.sub(r"\\&","&",chaine)
    chaine = re.sub(r"\$","",chaine)
    chaine = re.sub(r"\\,"," ",chaine)
    chaine = re.sub(r"\\","",chaine)

    chaine = re.sub(r"}","",chaine)
    chaine = re.sub(r"{","",chaine)
    
    return chaine
    

