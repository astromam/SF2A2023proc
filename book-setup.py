#
# book-setup.py
# 
# We setup here the book structure and
# define the variables used by the Python script make-book.py  
# 
# Edit this file appropriately
#
# updated by R. Samadi 22.10.2010
#

year ='2022'

bstfile = 'aa.bst'
clsfile = 'sf2a-conf2022'

# the place where the proceedings will be installed
#urlbase_proc="http://lesia.obspm.fr/semaine-sf2a/2012/proceedings/"
#urlbase_proc="http://proc.sf2a.asso.fr/"
#urlbase_proc="http://sf2a.cesr.fr/"
urlbase_proc="http://proceedings.sf2a.eu/" + year + "/"

editeurs='J. Richard, A. Siebert, E. Lagadec, N. Lagarde, O. Venot, J. Malzac, J.-B. Marquette, M. N\'Diaye, D. Briot'

start_page =1

NOCONTRIB=0 # 1 -> the contributions are not inserted, only the chapters are processed

# definition of the 2022 sessions and contribution
# sort out contributions according to Review, Talk, Posters
# (alphabetical order within each subclass)
# comment out sessions with no contribution
S0 = ['S0','Chauvin_S0','Douspis_S0','Knodlseder_S0','Meunier_S0','Ouazzani_S0','Robert_S0']
S1 = ['S1','Boughelilba_S1','DehiwalageDon_S1','ElMellah_S1','Freour_S1','Soudais_S1']
S2 = ['S2','Amard_S2','Cointepas_S2','Dhouib_S2','ElMellah_S2','Maimone_S2','Merle_S2','Meunier_S2','Noraz_S2','Tabone_S2','Thomassona_S2','Thomassonb_S2']
S3 = ['S3','LeGouellec_S3','Schirmer_S3','Taillard_S3']
S4 = ['S4','Boisse_S4','Vienne_S4']
S5 = ['S5','Alkan_S5','Desmars_S5','Robert_S5','Thuillot_S5','Turpin_S5','Delisle_S5','LeCam_S5','Lekic_S5','Marquette_S5','Wullaert_S5']
S6 = ['S6','Webb_S6']
S7 = ['S7','Freour_S7']
S9 = ['S9','Pitout_S9']
S10 = ['S10','Galliano_S10','Seillé_S10']
S11 = ['S11','Breton_S11','Delorme_S11']
S13 = ['S13','Berteaud_S13','Bourgoin_S13','Bruel_S13','Bugli_S13','Contini_S13','Godet_S13','Mignon-Risse_S13','Srinivasan_S13','Webb_S13']
S14 = ['S14','Tresse_S14']
S15 = ['S15','Lemasle_S15']
S16 = ['S16','Dyrek_S16','Malin_S16','Acuna_S16','Desgrange_S16','Ducreux_S16','Jaziri_S16']
S18 = ['S18','Beust_S18','Griveaud_S18','Gry_S18','Benseguane_S18','Cabral_S18','Crida_S18','Gkotsinas_S18','Martel_S18','Michoulier_S18']
S20 = ['S20','Cristofari_S20','Delcamp_S20']
S21 = ['S21','Griessmeier_S21','Cecconi_S21','Bonne_S21','Brionne_S21']
#WARNING : encoding of the ' -> \' and \'e -> \\\'e to keep latex text in the keys
# comment out sessions with no contribution
sessions = [
    {'SF2A --- Plenary session (S0)':S0},
    {'Atelier g\\\'en\\\'eral du PNHE (S1)':S1},
    {'Atelier g\\\'en\\\'eral du PNPS (S2)':S2},
    {'Atelier g\\\'en\\\'eral du PCMI (S3)':S3},
    {'Education \`a l\'astronomie : structuration, activit\\\'es et ressources (S4)': S4},
    {'Collaboration Pro-Am Gemini (S5)': S5},
    {'L\'\\\'egalit\\\'e des genres en A\&A : point sur les jeunes (S6)': S6},
    {'Transition environnementale : quel r\\^ole pour la communaut\\\'e astronomique ? (S7)': S7},
    {'Mesures in-situ et en t\\\'el\\\'ed\\\'etection des plasmas du Syst\\`eme solaire (S9)': S9},
    {'Dust in galaxies: from the local interstellar medium to distant galaxies (S10)': S10},
    {'Le Soleil est-il une \\\'etoile de type solaire ? (S11)': S11},
    {'Gravitational-wave astronomy and multi-messenger astrophysics (S13)': S13},
    {'L\'astrophysique fran\\c{c}aise \\`a l\'heure du JWST : opportunit\\\'es et d\\\'efis (S14)':S14},
    {'The Local Group in the Gaia era: from the Galactic halo to the Andromeda galaxy (S15)': S15},
    {'Atmosph\\`eres d\'exoplan\\`etes dans le contexte du JWST (S16)': S16},
    {'Disques de d\\\'ebris, exocom\\`etes et formation plan\\\'etaire (S18)': S18},
    {'Cosmic turbulence (S20)': S20},
    {'Le renouveau de la radio-astronomie et SKA, c\'est maintenant ! (S21)': S21}
    ]

