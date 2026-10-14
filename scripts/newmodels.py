import json,re,os,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
T=os.environ['TEMP']+'/pm/'
C=[]; seen=set()
for f in ['corpus_pre2000.jsonl','cA.jsonl','cB.jsonl','cC.jsonl']:
    for l in open(T+f,encoding='utf-8'):
        r=json.loads(l)
        if r['pmid'] not in seen: seen.add(r['pmid']); C.append(r)
cat=json.load(open(T+'cat.json'))
# New in-scope models identified by manual review of named_candidates.json
NEW=[
('Pneumonia & respiratory infection','ROX index','Prognostic index','Patients on high-flow nasal oxygen (pneumonia/COVID)','Validated, widely used',r'\bROX\b'),
('Pneumonia & respiratory infection','HACOR score','Prognostic score','Patients on non-invasive ventilation','Validated',r'\bHACOR\b'),
('Pneumonia & respiratory infection','SCAP (severe CAP) score','Prognostic score','Adults with CAP','Validated',r'\bSCAP\b'),
('Pneumonia & respiratory infection','MuLBSTA score','Prognostic score','Viral pneumonia','Validated, limited',r'MuLBSTA'),
('Pneumonia & respiratory infection','COVID-GRAM','Prognostic model','COVID-19','Validated',r'COVID-GRAM'),
('Pneumonia & respiratory infection','CALL score','Prognostic score','COVID-19','Validated',r'\bCALL score'),
('Pneumonia & respiratory infection','PRIEST score','Triage model','Suspected COVID-19, ED','Validated (UK)',r'\bPRIEST\b'),
('Pneumonia & respiratory infection','RAPID score (pleural infection)','Prognostic score','Pleural infection','Validated',r'RAPID score|\bRAPID\b.{0,40}pleural|pleural.{0,60}\bRAPID\b'),
('Sepsis / organ dysfunction (adult)','mSOFA (modified SOFA, no labs)','Organ-dysfunction score','Adults, resource-limited settings','Validated, LMIC',r'\bmSOFA\b|modified SOFA'),
('Sepsis / organ dysfunction (adult)','eSOFA / CDC Adult Sepsis Event','EHR surveillance definition','Hospitalised adults','In use (US surveillance)',r'\beSOFA\b|Adult Sepsis Event'),
('Sepsis / organ dysfunction (adult)','REDS score','Prognostic score','ED sepsis','Validated (UK)',r'\bREDS\b'),
('ICU mortality / severity','ICNARC model','Prognostic model','ICU adults (UK)','In routine use (UK)',r'ICNARC'),
('ICU mortality / severity','MPM II / MPM0-III','Prognostic model','ICU adults','In use',r'\bMPM\b|Mortality Probability Model'),
('Paediatric sepsis & severity','PCIS (Pediatric Critical Illness Score)','Severity score','PICU (China)','Regional use',r'\bPCIS\b|Pediatric Critical Illness Score'),
('Neonatal & febrile infant','SNAPPE-II / CRIB-II','Severity score','NICU','In routine use',r'SNAPPE|\bCRIB\b'),
('Neonatal & febrile infant','NEOMOD','Organ-dysfunction score','NICU','Research use',r'NEOMOD'),
('Organ-specific complications (AKI, liver)','RIFLE / AKIN / pRIFLE','AKI staging','ICU adults and children','Superseded by KDIGO, still used',r'\bRIFLE\b|\bAKIN\b|pRIFLE'),
('Bacteraemia & specific infections','FGSI (Fournier Gangrene Severity Index)','Prognostic score','Fournier gangrene','In use',r'\bFGSI\b|Fournier.{0,20}Severity Index'),
('Bacteraemia & specific infections','MSIS / ICM / EBJIS PJI criteria','Diagnostic criteria','Periprosthetic joint infection','Guideline',r'\bMSIS\b|EBJIS|periprosthetic joint infection.{0,80}criteria'),
('Bacteraemia & specific infections','Burns: ABSI / revised Baux','Prognostic score','Burn patients (sepsis risk)','In use',r'\bABSI\b|Baux'),
('Composite laboratory indices (research)','HALP / CALLY / CONUT / PNI / GNRI / TyG','Composite biomarker index','Sepsis, mixed','Under research (mostly single-centre)',r'\bHALP\b|\bCALLY\b|\bCONUT\b|\bPNI\b|\bGNRI\b|\bTyG\b'),
('ICU mortality / severity','NUTRIC / mNUTRIC (nutrition risk)','Prognostic score','ICU adults','In use (nutrition)',r'NUTRIC'),
]
def stats(rx):
    rc=re.compile(rx)
    hits=[r for r in C if rc.search(r['title']+' '+r['abstract'])]
    ti=[r for r in hits if rc.search(r['title'])]
    yrs=[int(r['year']) for r in ti if str(r['year']).isdigit()]
    early=sorted(ti,key=lambda r:(int(r['year']) if str(r['year']).isdigit() else 9999))[:1]
    return len(hits),len(ti),sum(1 for r in hits if str(r['year']).isdigit() and int(r['year'])>=2024),(early[0]['pmid']+' ('+early[0]['year']+')') if early else ''
out={'catalogue':[],'new':[]}
for d,n in zip(cat['D'],cat['cnt']):
    a,t,rec,e=stats(d[5]) if d[5] else (0,0,0,'')
    out['catalogue'].append([d[1],n,a,t,rec])
for x in NEW:
    a,t,rec,e=stats(x[5]); out['new'].append(list(x)+[a,t,rec,e])
json.dump(out,open(T+'newmodels.json','w'))
for r in out['new']: print(r[1],'| papers',r[6],'| title',r[7],'| 2024+',r[8],'| earliest title paper',r[9])
print('---catalogue models: file vs new search')
for r in out['catalogue']: print(f'{r[0][:45]:45s} file={r[1]:4d} search={r[2]:5d} title={r[3]:4d} 2024+={r[4]}')
