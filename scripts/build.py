import sys,os,re,json,time,urllib.request
sys.stdout.reconfigure(encoding='utf-8')
T=os.environ['TEMP']+'/pm/'
rows=json.load(open(T+'rows.json'))
txt=[(str(r['Title'])+' '+str(r['Abstract'])) for r in rows]
def cnt(rx): return sum(1 for t in txt if re.search(rx,t)) if rx else 0
# Domain | Model | Type | Population/setting | Status | regex-in-file | originator PMID | key update/validation PMID(s) | calculator | note
D=[
('Sepsis / organ dysfunction (adult)','SOFA','Organ-dysfunction score','ICU adults','In routine use (Sepsis-3 definition)',r'\bSOFA\b','8844239','26903335','MDCalc',''),
('Sepsis / organ dysfunction (adult)','SOFA-2 (2025 update)','Organ-dysfunction score','ICU adults','New (2025); replacing SOFA',r'SOFA[- ]?2\b','41159833','41159829; 41968305; 42192473','Not yet (check MDCalc)','Major gap: 1 record in file. Will change SOFA cut-offs on the site.'),
('Sepsis / organ dysfunction (adult)','qSOFA','Bedside screening score','ED/ward adults','In use (screening only; SSC 2021 advises against as single tool)',r'q-?\s?SOFA|quick SOFA','26903335','29800114','MDCalc',''),
('Sepsis / organ dysfunction (adult)','Lactate-qSOFA (LqSOFA)','Score + biomarker','ED adults','Validated, limited use',r'lactate.{0,15}qSOFA|qSOFA.{0,15}lactate|LqSOFA','32953813','39853387','None','Name clash with Liverpool qSOFA (paediatric). Site must disambiguate.'),
('Sepsis / organ dysfunction (adult)','SIRS criteria','Criteria','All adults','Legacy (Sepsis-1/2); still used for screening',r'\bSIRS\b','1303622','','MDCalc',''),
('Sepsis / organ dysfunction (adult)','MODS (Marshall)','Organ-dysfunction score','ICU adults','Research use',r'Multiple Organ Dysfunction Score|\bMODS\b','7587228','','MDCalc',''),
('Sepsis / organ dysfunction (adult)','LODS (Logistic Organ Dysfunction System)','Organ-dysfunction score','ICU adults','Research use',r'Logistic Organ Dysfunction','8769590','','None',''),
('Sepsis / organ dysfunction (adult)','PIRO','Staging score','ED sepsis adults','Research use',r'\bPIRO\b','21099424','','None',''),
('Sepsis / organ dysfunction (adult)','MEDS (Mortality in ED Sepsis)','Prognostic score','ED adults','Validated, moderate use',r'\bMEDS\b|Mortality in Emergency Department Sepsis','12626967','17110874','MDCalc',''),
('Sepsis / organ dysfunction (adult)','SIC (sepsis-induced coagulopathy)','Coagulopathy score','ICU sepsis','Guideline-endorsed (ISTH)',r'\bSIC\b|sepsis-induced coagulopathy','28963294','','None',''),
('Sepsis / organ dysfunction (adult)','ISTH overt DIC','Coagulopathy score','All','In routine use',r'ISTH','11816725','','MDCalc',''),
('Sepsis / organ dysfunction (adult)','JAAM DIC','Coagulopathy score','Acute care (Japan)','Regional use',r'JAAM','','','None','Originator PMID to add'),
('ICU mortality / severity','APACHE II','Prognostic score','ICU adults','In routine use',r'APACHE[ -]?(II|2)\b','3928249','','MDCalc',''),
('ICU mortality / severity','APACHE IV','Prognostic model','ICU adults (US)','In use (proprietary)',r'APACHE[ -]?(IV|4)\b','16540951','','Cerner (proprietary)',''),
('ICU mortality / severity','SAPS II','Prognostic score','ICU adults','In routine use',r'SAPS[ -]?(II|2)\b','8254858','','MDCalc',''),
('ICU mortality / severity','SAPS 3','Prognostic model','ICU adults','In use',r'SAPS[ -]?(3|III)\b','16132892','','saps3.org',''),
('ICU mortality / severity','MPM0-III','Prognostic model','ICU adults','In use (US)',r'\bMPM','','','None','Gap; originator PMID to verify (Higgins 2007)'),
('ICU mortality / severity','TropICS (simplified LMIC ICU model)','Prognostic model','ICU adults, South Asia LMIC','Validated, regional',r'TropICS|Tropical Intensive Care','29041985','29373996','None','Gap; NICST/MORU work'),
('ICU mortality / severity','R-MPM (Rwanda MPM)','Prognostic model','ICU adults, low-income','Validated, regional',r'R-MPM','27196252','','None','Gap'),
('ICU mortality / severity','SMS-ICU','Prognostic score','ICU adults','Validated',r'SMS-ICU','29368381','','None','Gap'),
('Early warning & ED triage','NEWS / NEWS2','Early-warning score','Ward/ED adults','In routine use (UK NHS standard)',r'\bNEWS ?2?\b','23295778','','MDCalc','NEWS2 = RCP 2017 report (not PubMed)'),
('Early warning & ED triage','MEWS','Early-warning score','Ward adults','In use',r'\bMEWS\b','11588210','','MDCalc',''),
('Early warning & ED triage','REMS','Prognostic score','ED adults','Validated',r'\bREMS\b','15078500','','MDCalc',''),
('Early warning & ED triage','UVA (Universal Vital Assessment)','Prognostic score','Hospitalised adults, sub-Saharan Africa','Validated, LMIC use',r'Universal Vital Assessment|\bUVA\b','29082001','34913982; 35320314','None','Major LMIC gap'),
('Early warning & ED triage','SATS / TEWS','Triage score','ED, South Africa/LMIC','In routine use (LMIC)',r'\bTEWS\b|South African Triage','','36941710','None','Originator PMID to add'),
('Early warning & ED triage','Shapiro bacteraemia rule','Diagnostic rule','ED adults','Validated',r'Shapiro','','25222426','MDCalc','Originator Shapiro 2008 PMID to add'),
('Early warning & ED triage','eCART','EHR ML deterioration model','Ward adults','Regulatory-cleared (FDA 2024)',r'\beCART\b','','39405061','Proprietary','Gap'),
('Early warning & ED triage','Kaiser Advance Alert Monitor','EHR ML deterioration model','Ward adults','In use (Kaiser)',r'Advance Alert Monitor','33176085','','Proprietary','Gap'),
('Paediatric sepsis & severity','Phoenix Sepsis Score / criteria','Organ-dysfunction score / definition','Children','New international definition (2024)',r'Phoenix','38245897','38245889; 40116825','None official','Major gap: 2 records'),
('Paediatric sepsis & severity','pSOFA','Organ-dysfunction score','PICU','Validated',r'pSOFA|pediatric SOFA|paediatric SOFA','28783810','','None',''),
('Paediatric sepsis & severity','PELOD-2','Organ-dysfunction score','PICU','In use',r'PELOD','23685639','26369662','MDCalc',''),
('Paediatric sepsis & severity','PRISM III / IV','Prognostic score','PICU','In use (proprietary)',r'\bPRISM','26492059','','None',''),
('Paediatric sepsis & severity','PIM3','Prognostic model','PICU','In routine use (ANZ/UK)',r'Paediatric Index of Mortality|Pediatric Index of Mortality|\bPIM ?3\b','23863821','','Online (various)','Gap'),
('Paediatric sepsis & severity','Liverpool qSOFA (LqSOFA, paediatric)','Bedside screening score','Febrile children, ED','Validated',r'Liverpool','32978294','40287144','None','Which "LqSOFA" did you mean? Both will be listed.'),
('Paediatric sepsis & severity','PERSEVERE / PERSEVERE-II / -XP','Biomarker risk model','Paediatric septic shock','Research / trial enrichment',r'PERSEVERE','23025259','28324661; 35818064','None',''),
('Paediatric sepsis & severity','SICK score','Bedside score','Children, LMIC','Validated, limited',r'\bSICK\b','16679672','20420670','None','Gap'),
('Paediatric sepsis & severity','Lambarene Organ Dysfunction Score (LODS)','Bedside score','Children with malaria/febrile illness, Africa','Validated',r'Lambar','19911989','37414210','None','Gap; name clash with adult LODS'),
('Paediatric sepsis & severity','Smart Triage (Pediatric Rapid Sepsis Trigger)','Triage model (digital)','Children, East Africa','Implementation',r'Smart Triage','36483471','38949998; 37653477','App','Gap'),
('Paediatric sepsis & severity','Smart Discharge post-discharge mortality models','Prognostic model','Children after infection admission, Uganda/Rwanda','Implementation',r'post-discharge mortality','38683787','40591583','App','Gap; new outcome category'),
('Paediatric sepsis & severity','sTREM-1 based triage (febrile children)','Biomarker triage model','Febrile children, Africa/Asia','Under development',r'sTREM-1.{0,80}triage|triage.{0,80}sTREM-1','34824252','37092821; 36243198','None','Directly relevant to your biomarker work'),
('Paediatric sepsis & severity','Paediatric pneumonia: RISC / RISC-Malawi / PERCH','Prognostic score','Children with pneumonia, LMIC','Validated',r'\bRISC\b|PERCH','22238570','28030608; 34737862','None','Gap'),
('Paediatric sepsis & severity','WHO ETAT / IMCI danger signs','Triage algorithm','Children, LMIC','Guideline (WHO)',r'\bETAT\b|\bIMCI\b','','32439313','None','Gap; WHO guideline, not PubMed'),
('Neonatal & febrile infant','Kaiser Early-Onset Sepsis Calculator','Prognostic model','Newborns >=34 wk','In routine use',r'Kaiser|early-onset sepsis calculator|EOS calculator','22025590','24366992; 28241253; 39314183; 40831464','Kaiser EOS calculator (official)','Major gap'),
('Neonatal & febrile infant','nSOFA','Organ-dysfunction score','Preterm neonates','Validated',r'nSOFA|neonatal sequential organ','33538825','37757759','None','Gap'),
('Neonatal & febrile infant','PECARN febrile infant rules (<=60 d, 61-90 d, <=28 d)','Diagnostic rule','Febrile infants','Guideline-endorsed',r'PECARN','30776077','40854562; 41359314','MDCalc','Gap'),
('Neonatal & febrile infant','Step-by-Step','Diagnostic algorithm','Febrile infants <=90 d','In use (Europe)',r'Step-by-Step','27382134','','MDCalc','Gap'),
('Neonatal & febrile infant','AAP 2021 febrile infant guideline','Diagnostic algorithm','Febrile infants 8-60 d','Guideline (US)',r'American Academy of Pediatrics','34281996','','None','Gap'),
('Neonatal & febrile infant','Lab-score','Diagnostic score','Febrile children <3 y','Validated',r'Lab-?score','20515973','29373477','None','Gap'),
('Pneumonia & respiratory infection','CURB-65 / CRB-65','Prognostic score','Adults with CAP','In routine use',r'C?U?RB-?65','12728155','','MDCalc',''),
('Pneumonia & respiratory infection','PSI / PORT','Prognostic score','Adults with CAP','In routine use (IDSA/ATS)',r'Pneumonia Severity Index|\bPSI\b','8995086','31573350','MDCalc',''),
('Pneumonia & respiratory infection','SMART-COP','Prognostic score','Adults with CAP','In use (Australia)',r'SMART-COP','18558884','20121679','MDCalc','Gap'),
('Pneumonia & respiratory infection','IDSA/ATS severe CAP criteria','Criteria','Adults with CAP','Guideline',r'IDSA/ATS|ATS/IDSA','31573350','','MDCalc','Gap'),
('Pneumonia & respiratory infection','A-DROP','Prognostic score','Adults with CAP (Japan)','Regional use',r'A-DROP','','18713094','None','Gap'),
('Pneumonia & respiratory infection','ISARIC 4C Mortality / Deterioration','Prognostic model','Adults with COVID-19','Validated, widely used',r'\b4C\b|ISARIC','32907855','35450898','isaric4c.net','Gap'),
('Pneumonia & respiratory infection','qCSI (Quick COVID-19 Severity Index)','Prognostic score','ED COVID-19','Validated',r'qCSI','33012378','','MDCalc','Gap'),
('Pneumonia & respiratory infection','CPIS','Diagnostic score','Ventilated (VAP)','In use',r'\bCPIS\b','2024824','','MDCalc',''),
('Pneumonia & respiratory infection','LIPS (Lung Injury Prediction Score)','Prognostic score','At-risk adults (ARDS)','Validated',r'Lung Injury Prediction|\bLIPS\b','20802164','20562130','MDCalc',''),
('Bacteraemia & specific infections','Pitt Bacteremia Score / quick Pitt','Prognostic score','Bloodstream infection','In use',r'Pitt','','30737765; 31219148','MDCalc','Originator (Paterson/Chow) PMID to add'),
('Bacteraemia & specific infections','INCREMENT-CPE score','Prognostic score','CPE bloodstream infection','Validated',r'INCREMENT','','','None','Gap; PMID to verify'),
('Bacteraemia & specific infections','2023 Duke-ISCVID criteria','Diagnostic criteria','Suspected endocarditis','Guideline',r'\bDuke','37138445','','MDCalc',''),
('Bacteraemia & specific infections','VIRSTA / PREDICT / POSITIVE','Diagnostic score','S. aureus bacteraemia (IE risk)','Validated',r'VIRSTA|HANDOC|DENOVA','26916042','','None','Gap'),
('Bacteraemia & specific infections','LRINEC','Diagnostic score','Soft-tissue infection','In use (poor sensitivity)',r'LRINEC','15241098','38720193','MDCalc',''),
('Bacteraemia & specific infections','MASCC risk index','Prognostic score','Febrile neutropenia','Guideline-endorsed',r'MASCC','10944139','32244162','MDCalc',''),
('Bacteraemia & specific infections','CISNE','Prognostic score','Stable febrile neutropenia','Guideline-endorsed',r'CISNE','25559804','','MDCalc','Gap'),
('Bacteraemia & specific infections','Bacterial Meningitis Score','Diagnostic rule','Children with CSF pleocytosis','In use',r'Bacterial Meningitis Score','17200475','22764093','MDCalc','Gap'),
('Bacteraemia & specific infections','Candida score','Diagnostic score','ICU non-neutropenic','In use',r'Candida score','16505659','19325481','MDCalc','Gap'),
('Bacteraemia & specific infections','ATLAS (C. difficile)','Prognostic score','C. difficile infection','Validated',r'ATLAS','23530807','','MDCalc','Gap'),
('Bacteraemia & specific infections','Host-response diagnostic: MeMed BV','Diagnostic (protein signature)','Bacterial vs viral','Regulatory-cleared (FDA 2021)',r'MeMed|TRAIL.{0,20}IP-10','29700762','','Device','Gap'),
('Bacteraemia & specific infections','Host-response diagnostic: SeptiCyte RAPID','Diagnostic (gene signature)','ICU sepsis vs SIRS','Regulatory-cleared (FDA)',r'SeptiCyte','29624409','27655322','Device','Gap'),
('Bacteraemia & specific infections','Monocyte Distribution Width (MDW)','Diagnostic (haematology parameter)','ED adults','Regulatory-cleared (FDA)',r'monocyte distribution width|\bMDW\b','31107278','','Analyser','Partly in file'),
('Tropical infections & febrile illness','WHO severe malaria criteria','Diagnostic/prognostic criteria','Malaria, all ages','Guideline (WHO)',r'severe malaria','25214480','','None',''),
('Tropical infections & febrile illness','CAM / RCAM (Coma-Acidosis-Malaria) score','Prognostic score','Adults with severe malaria','Validated',r'Coma Acidosis Malaria|\bR?CAM\b','20105074','28416929','None','Gap; MORU-derived'),
('Tropical infections & febrile illness','Blantyre Coma Scale','Severity scale','Children with cerebral malaria','In routine use',r'Blantyre','2690177','','MDCalc','Gap'),
('Tropical infections & febrile illness','Malaria prognostic models (systematic review)','Review','Malaria','Reference',r'malaria.{0,60}prognostic model','31772089','','-','Source list for malaria section'),
('Tropical infections & febrile illness','WHO 2009 dengue warning signs','Prognostic criteria','Dengue','Guideline (WHO)',r'warning sign','','26832147','None','WHO document (not PubMed)'),
('Tropical infections & febrile illness','Dengue 8-gene ML model','ML gene-expression model','Dengue','Under development',r'8-gene','35346346','','None','Gap'),
('Tropical infections & febrile illness','Melioidosis mortality prediction rules','Prognostic score','Melioidosis','Under development',r'melioidosis','39058188','37457570','None','Gap'),
('Tropical infections & febrile illness','Scrub typhus progression models','ML prognostic model','Scrub typhus','Under development',r'scrub typhus','40650401','','None','Gap'),
('Tropical infections & febrile illness','SFTS mortality scores / nomograms','Prognostic score','SFTS (East Asia)','Under development',r'severe fever with thrombocytopenia','28061758','38724615','None','Gap'),
('Tropical infections & febrile illness','Leptospirosis severity predictors / SPIRIT','Diagnostic/prognostic score','Leptospirosis','Under development',r'leptospirosis','','40457496','None','Gap'),
('Tropical infections & febrile illness','Febrile-illness biomarker triage (Ang-2, sTREM-1, CRP)','Triage','Acute febrile illness, LMIC','Under development',r'febrile illness','30305137','41094705','None','Your core domain'),
('Organ-specific complications (AKI, liver)','KDIGO staging + NephroCheck (TIMP-2*IGFBP7)','Staging + biomarker','ICU adults','In use (FDA-cleared test)',r'NephroCheck|TIMP-?2|IGFBP-?7','23388612','','Device',''),
('Organ-specific complications (AKI, liver)','Renal Angina Index','Prognostic score','PICU children','Validated',r'Renal Angina','24048379','24677554','MDCalc','Gap'),
('Organ-specific complications (AKI, liver)','MELD / MELD-Na','Prognostic score','Liver disease','In routine use',r'\bMELD','','','MDCalc','Out of core scope?'),
('Organ-specific complications (AKI, liver)','CLIF-SOFA / CLIF-C ACLF','Prognostic score','Cirrhosis / ACLF','In use',r'CLIF','','','efclif.com','Out of core scope?'),
('Maternal / obstetric sepsis','Sepsis in Obstetrics Score (SOS)','Prognostic score','Pregnant/postpartum women','Validated',r'Obstetric(s)? Score','24613756','28885400; 31217814','MDCalc','Gap'),
('Maternal / obstetric sepsis','omqSOFA / omSOFA (SOMANZ)','Screening score','Pregnant women','Guideline (ANZ)',r'omqSOFA|obstetrically modified','28670748','38922822','None','Gap'),
('Maternal / obstetric sepsis','MEOWS','Early-warning score','Obstetric inpatients','In routine use (UK)',r'MEOWS','22066604','','None','Gap'),
('ML / AI models (landing box)','Epic Sepsis Model','Proprietary EHR ML','Hospitalised adults','In use (widely); poor external validity',r'Epic Sepsis','34152373','37405252','Proprietary','Gap'),
('ML / AI models (landing box)','TREWS (Bayesian Health)','EHR ML early warning','Hospitalised adults','In use; prospective outcome data',r'TREWS','35864252','35864251','Proprietary','Gap'),
('ML / AI models (landing box)','COMPOSER (UCSD)','Deep-learning EHR model','ED adults','In use (single system)',r'COMPOSER','38263386','34504260; 40379845','Proprietary','Gap'),
('ML / AI models (landing box)','Sepsis ImmunoScore (Prenosis)','ML + biomarkers','ED/hospital adults','Regulatory-cleared (FDA De Novo 2024)',r'ImmunoScore','42449744','','Proprietary','Originator: Bhargava, NEJM AI 2024 (not indexed in PubMed)'),
('ML / AI models (landing box)','TriVerity (Inflammatix)','ML + 29-mRNA host response','ED adults','Regulatory-cleared (FDA 2025)',r'TriVerity','41028541','39982589','Device','In file (record 2)'),
('ML / AI models (landing box)','IntelliSep (Cytovale)','Cellular host response','ED adults','Regulatory-cleared (FDA)',r'IntelliSep|Cytovale','38333076','','Device','Gap; confirm 38333076 is IntelliSep'),
('ML / AI models (landing box)','Sepsis ML systematic reviews (onset & mortality)','Review','Mixed','Reference',r'machine learning|deep learning|random forest|XGBoost','38082381','41348160; 41372900; 37759175; 39478824','-','Source lists to populate the ML box'),
('Sepsis endotypes / phenotypes (research)','SRS1/SRS2 (Sepsis Response Signatures)','Transcriptomic endotype','ICU sepsis','Research / trial enrichment',r'\bSRS\b|sepsis response signature','26917434','30365341','None','Gap'),
('Sepsis endotypes / phenotypes (research)','MARS endotypes','Transcriptomic endotype','ICU sepsis','Research',r'\bMARS\b','28864056','','None','Gap'),
('Sepsis endotypes / phenotypes (research)','SENECA alpha/beta/gamma/delta phenotypes','Clinical phenotypes','Sepsis','Research',r'SENECA','31104070','','None','Gap'),
('Sepsis endotypes / phenotypes (research)','Consensus blood transcriptomic framework','Transcriptomic framework','Sepsis','Research (2025)',r'transcriptomic framework','41028542','','None','Gap'),
]
pm=sorted({p.strip() for d in D for f in (d[6],d[7]) for p in f.split(';') if p.strip().isdigit()})
oa={}
for i in range(0,len(pm),150):
    u='https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?format=json&tool=cpmtracker&ids='+','.join(pm[i:i+150])
    for rec in json.load(urllib.request.urlopen(u))['records']:
        oa[rec.get('pmid') or rec.get('requested-id')]=rec.get('pmcid','')
    time.sleep(0.4)
summ={}
for i in range(0,len(pm),150):
    d=json.load(urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id='+','.join(pm[i:i+150])))['result']
    for p in pm[i:i+150]:
        x=d.get(p,{}); summ[p]=(x.get('sortfirstauthor',''),x.get('pubdate','')[:4],x.get('source',''),x.get('title',''),next((a['value'] for a in x.get('articleids',[]) if a['idtype']=='doi'),''))
    time.sleep(0.4)
json.dump({'D':D,'oa':oa,'summ':summ,'cnt':[cnt(d[5]) for d in D]},open(T+'cat.json','w'))
print(len(D),'models;',len(pm),'PMIDs;',sum(1 for p in pm if oa.get(p)),'free in PMC')
