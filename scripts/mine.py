import json,re,os,sys,glob,collections
sys.stdout.reconfigure(encoding='utf-8')
T=os.environ['TEMP']+'/pm/'
C=[]; seen=set()
for f in ['corpus_pre2000.jsonl','cA.jsonl','cB.jsonl','cC.jsonl']:
    for l in open(T+f,encoding='utf-8'):
        try: r=json.loads(l)
        except: continue
        if r['pmid'] in seen: continue
        seen.add(r['pmid']); C.append(r)
print('corpus',len(C))
# ---------- classification ----------
R=lambda p: re.compile(p,re.I)
ML=R(r'machine learning|deep learning|artificial intelligence|random forest|xgboost|gradient boost|lightgbm|catboost|neural network|support vector|\bLSTM\b|transformer model|large language model|\bSHAP\b')
DEV=R(r'\b(develop|derive|deriv|construct|establish|build|built|creat|propos)\w*\b.{0,80}\b(model|score|nomogram|rule|tool|index|algorithm|system|signature|calculator)')
EXT=R(r'external(ly)? validat|validation cohort|independent cohort|temporal validation|geographic(al)? validation|prospective validation')
COMP=R(r'\bcompar\w*\b.{0,120}\b(score|scores|model|criteria|tool)s?\b|head-to-head|outperform')
SR=lambda r: any(p in ('Systematic Review','Meta-Analysis') for p in r['pt']) or re.search(r'systematic review|meta-analys',r['title'],re.I)
OUT=[('Mortality',r'mortality|death|surviv|fatal'),('Sepsis / septic shock onset or diagnosis',r'(predict|identif|detect|diagnos|recogni|screen)\w*.{0,40}(sepsis|septic shock)|sepsis.{0,20}(onset|diagnosis|screening|detection)'),
 ('Bacteraemia / SBI / bacterial vs viral',r'bacter[a]?emia|bloodstream infection|serious bacterial|invasive bacterial|bacterial (and|vs\.?|versus|or) viral|blood culture'),
 ('ICU admission / deterioration',r'ICU admission|intensive care (unit )?admission|deteriorat|escalation|critical care admission|rapid response'),
 ('Organ dysfunction (AKI/ARDS/DIC/liver/encephalopathy)',r'acute kidney injury|\bAKI\b|ARDS|respiratory distress|coagulopathy|\bDIC\b|liver (injury|failure)|encephalopathy|delirium|organ dysfunction|organ failure'),
 ('Severe disease progression',r'severe (disease|dengue|malaria|pneumonia|covid|case|outcome)|progression|severity')]
POPS=[('Neonatal',r'neonat|newborn|preterm|very low birth'),('Paediatric',r'child|paediatric|pediatric|infant|adolescen'),('Obstetric',r'pregnan|obstetric|maternal|postpartum|puerper'),('Adult',r'adult|elderly|older patients')]
DIS=[('COVID-19',r'covid|sars-cov-2'),('Pneumonia / respiratory',r'pneumonia|respiratory (tract )?infection|influenza|\bRSV\b'),('Malaria',r'malaria'),('Dengue',r'dengue'),('Other tropical',r'melioidosis|scrub typhus|leptospir|typhoid|enteric fever|severe fever with thrombocytopenia|\bSFTS\b|rickettsi|chikungunya|ebola|lassa'),
 ('Febrile neutropenia / immunocompromised',r'neutropeni|haematolog|hematolog|chemotherapy'),('Meningitis / CNS',r'meningitis|encephalitis'),('UTI / urosepsis',r'urinary tract|urosepsis|pyelonephritis'),('Skin & soft tissue',r'necrotizing fasciitis|soft tissue|cellulitis|fournier'),
 ('Endocarditis / S. aureus',r'endocarditis|staphylococcus aureus'),('Fungal',r'(?<![a-z])candid(a|iasis|emia|aemia)(?![a-z])|fungal|aspergill'),('C. difficile',r'difficile'),('Sepsis (general)',r'sepsis|septic')]
LMIC=R(r'\b(Africa|Uganda|Kenya|Tanzania|Malawi|Rwanda|Nigeria|Ghana|Ethiopia|Mozambique|Zambia|Zimbabwe|Gabon|Burkina|Mali|Senegal|Cameroon|Congo|Sudan|Bangladesh|India|Pakistan|Nepal|Sri Lanka|Myanmar|Cambodia|Lao|Laos|Vietnam|Viet Nam|Indonesia|Philippines|Thailand|Malaysia|Bhutan|Papua|Brazil|Peru|Bolivia|Colombia|Mexico|Haiti|Guatemala|Honduras|Egypt|Iran|Iraq|low-income|middle-income|low- and middle-income|LMIC|resource-limited|resource-poor|low-resource)\b')
def first(pairs,t):
    return [k for k,p in pairs if re.search(p,t,re.I)]
P=[]
for r in C:
    t=r['title']+' '+r['abstract']
    P.append({'pmid':r['pmid'],'year':r['year'],'title':r['title'],'journal':r['journal'],'fa':r['fa'],'doi':r['doi'],
      'ml':bool(ML.search(t)),'dev':bool(DEV.search(t)),'ext':bool(EXT.search(t)),'comp':bool(COMP.search(t)),'sr':bool(SR(r)),
      'outcome':first(OUT,t),'pop':(first(POPS,t) or ['Unspecified'])[0],'disease':(first(DIS,t) or ['Other / mixed'])[0],'lmic':bool(LMIC.search(t)),
      'hasabs':bool(r['abstract'].strip())})
json.dump(P,open(T+'classified.json','w'))
# ---------- named model discovery ----------
NAME=re.compile(r'\b((?:[a-z]{0,2}[A-Z][A-Za-z0-9]*[A-Z0-9][A-Za-z0-9]*|[A-Z]{2,})(?:[\-/ ][A-Z0-9][A-Za-z0-9\-]{0,10}){0,2})\s*(?:\(\w[^)]{0,40}\)\s*)?(?:score|scores|scoring system|criteria|index|rule|scale|model|nomogram|calculator|signature|tool|risk score)\b')
STOP=set('AUC ROC CI OR HR ICU ED IL CRP PCT WBC NLR PLR SII ROC-AUC LASSO SHAP MIMIC MIMIC-IV MIMIC-III eICU COVID-19 SARS-CoV-2 HIV AKI ARDS DIC MODS SIRS LR RR BMI GCS COX Cox ML AI DL RF SVM XGBoost LightGBM CatBoost DCA NRI IDI CT MRI PCR RT-PCR DNA RNA USA UK US WHO II III IV I The A An In We This These Our Of'.split())
cnt=collections.Counter(); tcnt=collections.Counter(); yrs=collections.defaultdict(list)
for r in C:
    t=r['title']+' '+r['abstract']
    found=set(m.strip() for m in NAME.findall(t))
    found={f for f in found if f not in STOP and not re.fullmatch(r'[IVX]+|\d+',f) and len(f)>=2}
    for f in found:
        cnt[f]+=1; yrs[f].append(r['year'])
        if f in r['title']: tcnt[f]+=1
cand=[(k,v,tcnt[k],min(yrs[k]),max(yrs[k])) for k,v in cnt.items() if v>=5]
cand.sort(key=lambda x:-x[1])
json.dump(cand,open(T+'named_candidates.json','w'))
print('named candidates (>=5 papers):',len(cand))
s=collections.Counter
print('dev',sum(p['dev'] for p in P),'ext',sum(p['ext'] for p in P),'comp',sum(p['comp'] for p in P),'sr',sum(p['sr'] for p in P),'ml',sum(p['ml'] for p in P),'lmic',sum(p['lmic'] for p in P))
