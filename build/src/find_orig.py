import sys; sys.path.insert(0,'build/src'); from pm import *
Q={'mSOFA Grissom':'Grissom CK[au] AND "modified sequential organ failure assessment"','REDS Sivayoham':'Sivayoham N[au] AND REDS','ICNARC Harrison 2007':'Harrison DA[au] AND "ICNARC model"[tiab]',
'SNAPPE-II':'Richardson DK[au] AND "SNAP-II and SNAPPE-II"','PRISM III':'Pollack MM[au] AND "PRISM III"[ti]','MPM0-III':'Higgins TL[au] AND "Mortality Probability Model"[ti] AND "III"',
'Phoenix consensus':'38245889[uid]','nSOFA Fleiss 2021':'Fleiss N[au] AND neonatal sequential organ failure','MEWS Subbe':'11588210[uid]','eSOFA Rhee':'Rhee C[au] AND "Adult Sepsis Event"',
'NEWS2 validation':'"NEWS2"[ti] AND sepsis AND validation','RISC-Malawi':'28030608[uid]','PECARN 2019':'30776077[uid]','Smart triage 2022':'36483471[uid]',
'PIM3':'23863821[uid]','SMS-ICU':'29368381[uid]','Liverpool qSOFA':'32978294[uid]','PERSEVERE':'23025259[uid]','Lambarene':'19911989[uid]','SICK':'16679672[uid]',
'TropICS':'29041985[uid]','RMPM':'27196252[uid]','UVA':'29082001[uid]','LqSOFA lactate':'32953813[uid]','Kaiser 2011':'22025590[uid]','Kaiser 2014':'24366992[uid]',
'StepbyStep':'27382134[uid]','AAP':'34281996[uid]','Labscore':'20515973[uid]','pSOFA':'28783810[uid]','PELOD2':'23685639[uid]','PRISMIV':'26492059[uid]',
'SOFA2':'41159833[uid]','Phoenix dev':'38245897[uid]','qSOFA':'26903335[uid]','SOFA':'8844239[uid]','MEDS':'12626967[uid]','MODS':'7587228[uid]','LODS':'8769590[uid]',
'APACHE II':'3928249[uid]','APACHE IV':'16540951[uid]','SAPS II':'8254858[uid]','SAPS3':'16132892[uid]','REMS':'15078500[uid]','PIRO':'21099424[uid]','NEWS':'23295778[uid]',
'SIRS':'1303622[uid]','Phoenix ext':'40116825[uid]','SOFA2 ext':'41968305[uid]','UVA ext':'34913982[uid]','qSOFA exc mort':'29800114[uid]','sTREM1':'34824252[uid]','Smart discharge':'38683787[uid]',
'nSOFA LOS':'33538825[uid]','PECARN 61-90':'40854562[uid]','PECARN 28d':'41359314[uid]','Kaiser RCT':'40831464[uid]','Kaiser update':'39314183[uid]','LqSOFA MA':'39853387[uid]'}
found={}
for k,q in Q.items():
    ids=search(q,2); found[k]=ids[:1] if '[uid]' in q else ids
allids=sorted({i for v in found.values() for i in v})
A={}
for i in range(0,len(allids),100): A.update(abstracts(allids[i:i+100]))
json.dump({'found':found,'abs':A},open('build/src/abstracts.json','w',encoding='utf-8'),ensure_ascii=False)
for k,v in found.items():
    for i in v: print(k,'|',i,A.get(i,{}).get('year'),A.get(i,{}).get('journal'),'| PMC:',A.get(i,{}).get('pmc'),'|',A.get(i,{}).get('title','')[:90])
