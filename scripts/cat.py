import json,re,os,sys
rows=json.load(open(os.environ['TEMP']+'/pm/rows.json'))
txt=[(str(r['Title'])+' '+str(r['Abstract'])) for r in rows]
# domain: name -> regex
C={
# Sepsis / organ dysfunction (adult)
'SOFA':r'\bSOFA\b','SOFA-2 (2025)':r'SOFA[- ]?2\b','qSOFA':r'q-?\s?SOFA|quick SOFA','Lactate-qSOFA (LqSOFA)':r'LqSOFA|lactate.{0,10}qSOFA|qSOFA.{0,15}lactate','SIRS':r'\bSIRS\b','MODS (Marshall)':r'Multiple Organ Dysfunction Score|\bMODS\b','LODS':r'\bLODS\b|Logistic Organ Dysfunction','PIRO':r'\bPIRO\b','MEDS':r'\bMEDS\b|Mortality in Emergency Department Sepsis','CLIF-SOFA':r'CLIF','SIC (sepsis-induced coagulopathy)':r'\bSIC\b|sepsis-induced coagulopathy','ISTH DIC':r'ISTH','JAAM DIC':r'JAAM',
# ICU mortality
'APACHE II':r'APACHE[ -]?(II|2)\b','APACHE III':r'APACHE[ -]?(III|3)\b','APACHE IV':r'APACHE[ -]?(IV|4)\b','SAPS II':r'SAPS[ -]?(II|2)\b','SAPS 3':r'SAPS[ -]?(3|III)\b','MPM':r'\bMPM','ICNARC model':r'ICNARC','ANZROD':r'ANZROD','TropICS':r'TropICS|Tropical Intensive Care','R-MPM (Rwanda)':r'R-MPM','SMS-ICU':r'SMS-ICU',
# EWS / ED triage
'NEWS':r'\bNEWS\b','NEWS2':r'NEWS ?2','MEWS':r'\bMEWS\b','REMS':r'\bREMS\b','UVA score':r'Universal Vital Assessment|\bUVA\b','TEWS/SATS':r'\bTEWS\b|South African Triage','Shock index':r'shock index','eCART/CART':r'\beCART\b|\bCART score','Shapiro bacteremia rule':r'Shapiro','Epic Sepsis Model':r'Epic Sepsis','TREWS':r'TREWS','Sepsis ImmunoScore':r'ImmunoScore','TriVerity':r'TriVerity','IntelliSep':r'IntelliSep|Cytovale','Monocyte distribution width':r'monocyte distribution width|\bMDW\b','SeptiCyte':r'SeptiCyte','MeMed BV':r'MeMed|TRAIL.{0,20}IP-10',
# Paediatric sepsis/ICU
'Phoenix Sepsis Score':r'Phoenix','pSOFA':r'pSOFA|pediatric SOFA|paediatric SOFA','PELOD/PELOD-2':r'PELOD','PRISM':r'\bPRISM','PIM2/3':r'\bPIM ?[23]?\b|Paediatric Index of Mortality|Pediatric Index of Mortality','PEWS':r'\bPEWS\b','PERSEVERE':r'PERSEVERE','Liverpool qSOFA':r'Liverpool','SICK score':r'\bSICK\b','Lambarene LODS':r'Lambar','Smart Discharge/Smart Triage':r'Smart (Discharge|Triage)','ETAT/IMCI':r'\bETAT\b|\bIMCI\b',
# Neonatal / febrile infant
'Kaiser EOS calculator':r'Kaiser|early-onset sepsis calculator|EOS calculator','nSOFA':r'nSOFA|neonatal SOFA','SNAPPE/CRIB':r'SNAP|\bCRIB','Febrile infant rules (Rochester/Step-by-Step/PECARN)':r'Rochester|Step-by-Step|PECARN|Philadelphia criteria|Boston criteria','Lab-score':r'Lab-?score',
# Pneumonia/COVID
'CURB-65/CRB-65':r'C?U?RB-?65','PSI/PORT':r'\bPSI\b|Pneumonia Severity Index|\bPORT\b','SMART-COP':r'SMART-COP','IDSA/ATS criteria':r'IDSA/ATS|ATS/IDSA','A-DROP':r'A-DROP','RISC (child pneumonia)':r'\bRISC\b','4C Mortality':r'\b4C\b|ISARIC','CPIS':r'\bCPIS\b','COVID-GRAM/CALL':r'COVID-GRAM|CALL score',
# Infection-specific
'Pitt Bacteremia':r'Pitt','INCREMENT-CPE':r'INCREMENT','Duke criteria':r'\bDuke','VIRSTA/PREDICT/HANDOC':r'VIRSTA|HANDOC|DENOVA','LRINEC':r'LRINEC','MASCC/CISNE':r'MASCC|CISNE','Candida score':r'Candida score|Ostrosky|colonization index','Bacterial Meningitis Score':r'Bacterial Meningitis Score','C. difficile ATLAS/Zar':r'ATLAS|Zar score',
# Tropical
'WHO severe malaria criteria':r'severe malaria','CAM / RCAM (malaria)':r'\bR?CAM\b|Coma Acidosis Malaria','Blantyre Coma Scale':r'Blantyre','WHO dengue warning signs':r'warning sign','Leptospirosis SPIRIT/Faine':r'SPIRIT|Faine',
# Organ-specific
'KDIGO/AKI biomarkers':r'KDIGO|NephroCheck|TIMP-?2|IGFBP-?7','Renal Angina Index':r'Renal Angina','LIPS / Murray LIS':r'Lung Injury Prediction|\bLIPS\b|Murray|Lung Injury Score','MELD':r'\bMELD','Child-Pugh':r'Child-?(Turcotte-)?Pugh','ALBI':r'\bALBI\b','Charlson':r'Charlson','Clinical Frailty Scale':r'Frailty Scale',
# Obstetric/burn/trauma
'Sepsis in Obstetrics Score / omqSOFA':r'Obstetric(s)? Score|omqSOFA|\bSOS\b','MEOWS':r'MEOWS','ABSI / Baux':r'\bABSI\b|Baux','ISS/TRISS/RTS':r'\bISS\b|TRISS|\bRTS\b',
# Endotypes / omics
'Sepsis endotypes (SRS/SENECA/MARS)':r'\bSRS\b|SENECA|\bMARS\b|endotype|phenotype',
'Gene-expression signatures':r'gene expression signature|transcriptomic',
# Composite biomarker indices
'NLR/PLR/SII-type indices':r'NLR|neutrophil[- ]to[- ]lymphocyte|\bSII\b|systemic immune','PNI/CALLY/HALP':r'\bPNI\b|CALLY|HALP','TyG':r'\bTyG\b',
}
for k,v in C.items():
    n=sum(1 for t in txt if re.search(v,t))
    print(f'{n:4d}  {k}')
