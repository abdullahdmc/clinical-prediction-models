import sys,json; sys.path.insert(0,'build/src'); from pm import *
sys.stdout.reconfigure(encoding='utf-8')
Q={'JAAM DIC':'Gando S[au] AND "disseminated intravascular coagulation" AND 2006[dp] AND "Crit Care Med"[ta]',
'SATS':'"South African Triage Scale"[tiab] AND (validation OR development) AND 2006:2010[dp]',
'TEWS':'"Triage Early Warning Score"[tiab]',
'Shapiro':'Shapiro NI[au] AND bacteremia AND "decision rule" AND 2008[dp]',
'A-DROP':'"A-DROP"[tiab] AND Miyashita',
'Pitt':'"Pitt bacteremia score"[tiab] AND Paterson DL[au]',
'INCREMENT':'Gutierrez-Gutierrez B[au] AND carbapenemase AND "mortality score"',
'SPIRIT':'Rajapakse S[au] AND leptospirosis AND "diagnostic"',
'MELD':'Kamath PS[au] AND "model to predict survival in patients with end-stage liver disease"',
'CLIF-C ACLF':'Jalan R[au] AND "CLIF Consortium" AND "ACLF score" AND 2014[dp]',
'RAPID':'Rahman NM[au] AND "pleural infection" AND "clinical score"',
'ROX':'Roca O[au] AND "ROX" AND 2016[dp]',
'ROX 2019':'Roca O[au] AND "ROX index" AND 2019[dp]',
'HACOR':'Duan J[au] AND HACOR AND 2017[dp]',
'SCAP':'Espana PP[au] AND "severe community-acquired pneumonia" AND 2006[dp]',
'MuLBSTA':'Guo L[au] AND MuLBSTA',
'COVID-GRAM':'Liang W[au] AND "COVID-19" AND "critical illness" AND 2020[dp] AND "JAMA Intern Med"[ta]',
'CALL':'Ji D[au] AND "CALL score"',
'PRIEST':'Goodacre S[au] AND PRIEST AND 2021[dp]',
'eSOFA':'Rhee C[au] AND "eSOFA"',
'REDS':'Sivayoham N[au] AND "REDS" AND 2019[dp]',
'ICNARC':'Harrison DA[au] AND "ICNARC" AND 2007[dp]',
'PCIS':'"Pediatric Critical Illness Score"[tiab]',
'NEOMOD':'Janota J[au] AND NEOMOD',
'RIFLE':'Bellomo R[au] AND "Acute Dialysis Quality Initiative" AND 2004[dp]',
'AKIN':'Mehta RL[au] AND "Acute Kidney Injury Network" AND 2007[dp]',
'FGSI':'Laor E[au] AND Fournier',
'MSIS':'Parvizi J[au] AND "periprosthetic joint infection" AND definition AND 2011[dp]',
'ABSI':'Tobiasen J[au] AND "abbreviated burn severity index"',
'revised Baux':'Osler T[au] AND Baux',
'NUTRIC':'Heyland DK[au] AND "NUTRIC" AND 2011[dp]',
'mNUTRIC':'Rahman A[au] AND "modified NUTRIC"',
'MeMed Oved':'Oved K[au] AND "host-protein signature" AND 2015[dp]',
'SeptiCyte McHugh':'McHugh L[au] AND SeptiCyte AND 2015[dp]',
'BCS Molyneux':'2690177[uid]',
'IDSA ATS 2007':'Mandell LA[au] AND "Infectious Diseases Society of America/American Thoracic Society consensus guidelines" AND 2007[dp]',
'CPIS Pugin':'2024824[uid]','LIPS':'20802164[uid]','CURB65':'12728155[uid]','PSI':'8995086[uid]','SMARTCOP':'18558884[uid]','4C':'32907855[uid]','qCSI':'33012378[uid]',
'Duke2023':'37138445[uid]','VIRSTA':'26916042[uid]','LRINEC':'15241098[uid]','MASCC':'10944139[uid]','CISNE':'25559804[uid]','BMS':'17200475[uid]','Candida':'16505659[uid]',
'ATLAS':'23530807[uid]','MDW':'31107278[uid]','WHO malaria':'25214480[uid]','CAM':'20105074[uid]','dengue8':'35346346[uid]','melioid':'39058188[uid]','scrub':'40650401[uid]',
'SFTS':'28061758[uid]','febtriage':'30305137[uid]','febtriage2':'41094705[uid]','NephroCheck':'23388612[uid]','RAI':'24048379[uid]','SIC':'28963294[uid]','ISTH':'11816725[uid]',
'SOS':'24613756[uid]','SOS val':'28885400[uid]','SOMANZ':'28670748[uid]','SOMANZ23':'38922822[uid]','MEOWS':'22066604[uid]','SRS':'26917434[uid]','MARS':'28864056[uid]','SENECA':'31104070[uid]',
'consensus':'41028542[uid]','dengue WS':'26832147[uid]','qPitt':'30737765[uid]','lepto review':'40457496[uid]','etat':'32439313[uid]','sats val':'36941710[uid]','shapiro val':'25222426[uid]'}
found={}
for k,q in Q.items():
    found[k]=search(q,1)
ids=sorted({i for v in found.values() for i in v}); A={}
for i in range(0,len(ids),100): A.update(abstracts(ids[i:i+100]))
json.dump({'found':found,'abs':A},open('build/src/abstracts2.json','w',encoding='utf-8'),ensure_ascii=False)
for k,v in found.items():
    for i in v: a=A.get(i,{}); print(f"{k:14s}| {i} {a.get('fa')} {a.get('year')} {a.get('journal')} | {a.get('pmc') or '-'} | {a.get('title','')[:80]}")
    if not v: print(k,'| NOT FOUND')
