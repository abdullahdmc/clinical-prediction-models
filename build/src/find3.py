import sys,json; sys.path.insert(0,'build/src'); from pm import *
sys.stdout.reconfigure(encoding='utf-8')
Q={'Pitt Paterson':'Paterson DL[au] AND "Klebsiella pneumoniae bacteremia" AND 2004[dp] AND "Ann Intern Med"[ta]',
'INCREMENT':'"INCREMENT-CPE"[tiab] AND "mortality score"',
'INCREMENT2':'Gutierrez-Gutierrez B[au] AND "Mayo Clin Proc"[ta]',
'ICNARC':'Harrison DA[au] AND "risk prediction model" AND "critical care" AND 2007[dp]',
'PRIEST':'Goodacre S[au] AND "suspected COVID-19" AND "clinical severity score"',
'NUTRIC':'Heyland DK[au] AND "novel risk assessment tool" AND nutrition',
'MeMed':'Oved K[au] AND "bacterial and viral" AND 2015[dp]',
'IDSA2007':'Mandell LA[au] AND community-acquired pneumonia AND "consensus guidelines" AND 2007[dp]',
'SPIRIT':'"SPIRIT"[tiab] AND leptospirosis',
'MELD orig':'Kamath PS[au] AND "end-stage liver disease" AND 2001[dp] AND Hepatology[ta]',
'CLIF-SOFA':'Moreau R[au] AND "acute-on-chronic liver failure" AND 2013[dp] AND Gastroenterology[ta]',
'SATS':'Gottschalk SB[au] AND triage',
'ETAT':'"Emergency Triage Assessment and Treatment"[tiab] AND (mortality OR evaluation)',
'Blantyre val':'"Blantyre coma scale"[ti]',
'WHO dengue':'"dengue" AND "2009 WHO" AND classification AND (multicentre OR multicenter) AND Alexander N[au]',
'ABSI val':'"abbreviated burn severity index"[tiab] AND validation',
'KDIGO':'"KDIGO" AND "acute kidney injury" AND guideline AND 2012[dp] AND Kellum JA[au]',
'MEWS-obs SOS':'"Sepsis in Obstetrics Score"[tiab] AND low-income',
'A-DROP orig':'"A-DROP"[ti]',
'Duke val':'"2023 Duke-ISCVID"[tiab] AND validation',
}
found={k:search(q,2) for k,q in Q.items()}
ids=sorted({i for v in found.values() for i in v}); A={}
for i in range(0,len(ids),100): A.update(abstracts(ids[i:i+100]))
old=json.load(open('build/src/abstracts2.json',encoding='utf-8')); old['abs'].update(A); old['found'].update({'_'+k:v for k,v in found.items()})
json.dump(old,open('build/src/abstracts2.json','w',encoding='utf-8'),ensure_ascii=False)
for k,v in found.items():
    for i in v: a=A.get(i,{}); print(f"{k:12s}| {i} {a.get('fa')} {a.get('year')} {a.get('journal')} | {a.get('pmc') or '-'} | {a.get('title','')[:85]}")
    if not v: print(k,'| NOT FOUND')
