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

year ='2023'

bstfile = 'aa.bst'
clsfile = 'sf2a-conf2023'

# the place where the proceedings will be installed
#urlbase_proc="http://lesia.obspm.fr/semaine-sf2a/2012/proceedings/"
#urlbase_proc="http://proc.sf2a.asso.fr/"
#urlbase_proc="http://sf2a.cesr.fr/"
urlbase_proc="http://proceedings.sf2a.eu/" + year + "/"

editeurs='M. N\'Diaye, A. Siebert, N. Lagarde, O. Venot, K. Bailli\'e, M. B\'ethermin, E. Lagadec, J. Malzac, J. Richard'

start_page =1

NOCONTRIB=0 # 1 -> the contributions are not inserted, only the chapters are processed

# definition of the 2023 sessions and contribution
# sort out contributions according to Review, Talk, Posters
# (alphabetical order within each subclass)
# comment out sessions with no contribution
S00 = ['S00', 'Allen_s00','De_simone_s00','Deheuvels_s00','Leboulleux_s00', 'Manchon_s00', 'Metris_s00','Ng_s00', 'Noble_s00']
S01 = ['S01', 'Mahler_s01', 'Cerardi_s01', 'Chu_S01', 'Kou_s01', 'Nagesh_s01', 'Pommiera_s01', 'Pommierb_s01']
S02 = ['S02', 'Palicio_s02', 'Contursi_s02', 'Fortin_s02', 'Khalil_s02', 'Li_s02', 'Martocchia_S02', 'Soubiran_s02', 'Tenachi_S02']
S03 = ['S03', 'Ng_s03', 'Petri_s03', 'Barrere_s03', 'Berteaud_s03', 'Boughelilba_s03', 'Bretaudeau_s03', 'Decoene_s03', 'Diez_s03', 'Duque_s03', 'Laviron_s03', 'Mottez_s03',  'Quintin_s03', 'Bugli_s03']
S04 = ['S04', 'Buchlin_s04', 'Genova_s04']
S05 = ['S05', 'Webb_s05']
S06 = ['S06', 'Halbwachs_s06', 'Leroy_s06', 'Midavaine_s06', 'Schuessler_s06', 'Barroy_s06', 'Lekic_s06', 'Lilensten_s06', 'Robineau_s06']
S07 = ['S07', 'Adam_s07', 'Farcy_s07']
S08 = ['S08', 'Puech_s08', 'PalmaBifani_s08', 'Delsanti_s08']
S09 = ['S09', 'Vauglin_s09', 'Pommier_s09']
S10 = ['S10', 'Chastenet_s10', 'Correia_s10', 'Michoulier_S10', 'Milli_s10', 'Segretain_s10']
S12 = ['S12', 'Chauvin_s12', 'Acuna_s12', 'Mouillet_s12']
S13 = ['S13', 'Gavino_s13', 'Kessler_s13', 'Valeille-Manet_s13', 'Coutens_s13', 'Oers_s13']
S14 = ['S14', 'Chastenet_s14', 'Gomez-Guijarro_s14', 'Paquereau_s14', 'Seille_s14']
S15 = ['S15', 'Baguet_s15', 'Robert_s15', 'Rosat_s15', 'RoubeauTissot_s15', 'Staelen_s15']
S16 = ['S16', 'Venot_s16', 'Bergezcasalou_s16', 'Debatzdetrenquelleon_s16', 'Dhouib_s16', 'Fleury_s16', 'Huet_s16', 'Naar_s16', 'Priolet_s16', 'Robert_s16']
S17 = ['S17', 'Aykroyd_s17', 'Beguin_s17', 'Blondin_s17', 'Cristofari_s17', 'Degott_s17', 'Ligi_s17', 'Marinho_s17', 'Mignon-risse_s17', 'Monpribat_s17', 'Perraut_s17', 'Astoul_s17', 'Bessila_s17', 'Breton_s17', 'Dumont_s17', 'Faurobert_s17', 'Gonzalez_s17', 'Halbwachs_s17', 'LeGouellec_s17', 'Martel_s17', 'Martinod_s17', 'Mauxion_s17', 'Radureau_s17', 'Ravinet_s17']
S18 = ['S18', 'Atteia_s18', 'Bugli_s18', 'Debony_s18', 'Fortin_s18', 'Foustoul_s18', 'Mignon-risse_s18', 'Francois_s18']
S19 = ['S19', 'Schneider_s19', 'ThomsonParessant_s19', 'Adami_s19', 'Dennefeld_s19', 'Parra-Ramos_s19', 'Russeil_s19', 'Soucail_S19']
S20 = ['S20', 'Neiner_s20']
S21 = ['S21', 'Leboulleux_s21']
#WARNING : encoding of the ' -> \' and \'e -> \\\'e to keep latex text in the keys
# comment out sessions with no contribution
sessions = [
    {'SF2A --- Plenary session': S00},
    {'Amas et groupes de galaxies dans l\'\`ere des grands relev\\\'es': S01},
    {'Arch\\\'eologie Galactique avec Gaia/DR3: un an apr\`es': S02},
    {'AS SKA-LOFAR and PNHE Workshop - Compact Objects: Observations and theory from radio to gamma': S03},
    {'Open Science in Astronomy': S04},
    {'Bien-\^etre en astrophysique': S05},
    {'Partenariat Gemini SAF SF2A sur les collaborations amateurs professionnels': S06},
    {'Cosmic Rays and Cosmology': S07},
    {'Demain l\'ELT! Strat\\\'egies d\'observation, pr\\\'eparation des programmes scientifiques et synergies trans-instruments': S08},    
    {'L\'\\\'egalit\\\'e des genres en A\&A: st\\\'er\\\'eotypes de genre dans l\'enseignement': S09},
    {'Latest insights on dust evolution': S10},
    {'Origine de l\'eau et de la vie: Quels d\\\'efis astrophysiques et instrumentaux pour demain ?': S12},
    {'Atelier g\\\'en\\\'eral du PCMI': S13},
    {'Galaxy evolution in the era of JWST (atelier du PNCG)': S14},
    {'PNGRAM G\\\'eod\\\'esie Spatiale': S15},
    {'Atelier g\\\'en\\\'eral du Programme National de Plan\\\'etologie (PNP)': S16},
    {'Atelier g\\\'en\\\'eral du Programme National de Physique Stellaire (PNPS)': S17},
    {'Pr\\\'ediction et suivi des signaux multi-messagers': S18},
    {'Sixi\`eme r\\\'eunion des utilisateurs des t\\\'elescopes fran\c cais (TBL/OHP193)': S19},
    {'The future of micro- and nanosatellites for astronomy': S20},
    {'Transition environnementale : quels leviers d\'actions pour r\\\'eduire l\'empreinte environnementale de l\'astronomie ?': S21},
    ]

