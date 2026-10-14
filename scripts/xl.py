import json,os,collections,sys
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
T=os.environ['TEMP']+'/pm/'
c=json.load(open(T+'cat.json')); D,oa,summ,cnt=c['D'],c['oa'],c['summ'],c['cnt']
out=sys.argv[1]
wb=Workbook()
H=Font(bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='1F4E78')
GAP=PatternFill('solid',fgColor='FCE4D6'); PART=PatternFill('solid',fgColor='FFF2CC')
def sheet(ws,head,rows,widths):
    ws.append(head)
    for cl in ws[1]: cl.font=H; cl.fill=HF; cl.alignment=Alignment(wrap_text=True,vertical='top')
    for r in rows: ws.append(r)
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    for row in ws.iter_rows(min_row=2):
        for cl in row: cl.alignment=Alignment(wrap_text=True,vertical='top')
    ws.freeze_panes='C2'; ws.auto_filter.ref=ws.dimensions

def pl(s): return [p.strip() for p in s.split(';') if p.strip().isdigit()]
def ft(s):
    ps=pl(s)
    if not ps: return ''
    return '; '.join(f"{p}: {'PMC free' if oa.get(p) else 'NEED PDF'}" for p in ps)

# Sheet 1: summary
ws=wb.active; ws.title='Read me & findings'
cov=collections.defaultdict(lambda:[0,0,0])
for d,n in zip(D,cnt):
    k=cov[d[0]]; k[0]+=1; k[1]+= n>=3; k[2]+= n==0
lines=[
['Clinical Prediction Model Tracker: gap analysis of your PubMed file (prepared 14 Oct 2026)'],[''],
['Your file: 1,540 records. A biomarker-led search (PCT, CRP, IL-6, lactate, etc.) on sepsis/severe infection, mostly ICU (712) and mortality (1,099).'],
['The keyword extraction only tagged 19 clinical scores. Re-mining the abstracts found about 60 named scores/indices, but most are mentioned as comparators, not as the model under study.'],
['Most important structural gap: the search finds biomarker studies that MENTION scores. It was not designed to find prediction-model development/validation papers. ED, ward, LMIC, paediatric, neonatal and obstetric models are badly under-represented.'],[''],
['Assumed scope (please confirm): prediction/diagnostic models for acute infection, sepsis and febrile-illness severity, in adults and children, high- and low-resource settings.'],[''],
['Coverage by outcome domain','Models in catalogue','Well covered in your file (>=3 records)','Absent from your file (0 records)'],
]
for l in lines: ws.append(l)
for k,v in cov.items(): ws.append([k]+v)
ws.append([''])
ws.append(['Legend (Master catalogue): orange row = absent from your file; yellow = 1-2 records; white = >=3 records.'])
ws.append(['Record counts come from regex matches on title + abstract. They are approximate and include passing mentions.'])
ws.append(['"NEED PDF" = no free PubMed Central copy. See the "PDFs to download" sheet.'])
ws['A1'].font=Font(bold=True,size=14)
for cl in ws[9]: cl.font=Font(bold=True)
ws.column_dimensions['A'].width=60
for col in 'BCD': ws.column_dimensions[col].width=22

# Sheet 2: master catalogue
ws=wb.create_sheet('Master catalogue')
rows=[]
for d,n in zip(D,cnt):
    gap='ABSENT' if n==0 else ('Sparse' if n<3 else 'Covered')
    rows.append([d[0],d[1],d[2],d[3],d[4],n,gap,d[6],d[7],ft(d[6]),ft(d[7]),d[8],d[9]])
sheet(ws,['Outcome domain','Model','Model type','Population / setting','Status (in use / developing)','Records in your file','Gap status','Originator PMID','Key update / validation PMID(s)','Originator full text','Update full text','Online calculator','Notes'],rows,[28,34,22,26,28,10,10,12,22,22,26,18,40])
for row in ws.iter_rows(min_row=2):
    f=GAP if row[6].value=='ABSENT' else (PART if row[6].value=='Sparse' else None)
    if f:
        for cl in row: cl.fill=f

# Sheet 3: PDFs to download
ws=wb.create_sheet('PDFs to download')
need={}
for d in D:
    for role,s in (('Originator',d[6]),('Update/validation',d[7])):
        for p in pl(s):
            if not oa.get(p):
                e=need.setdefault(p,{'models':[],'role':role})
                e['models'].append(d[1])
                if role=='Originator': e['role']='Originator'
rows=[]
for p,e in need.items():
    a,y,j,t,doi=summ.get(p,['','','','',''])
    pr='1-High' if e['role']=='Originator' else '2-Medium'
    rows.append([pr,'; '.join(dict.fromkeys(e['models'])),e['role'],a,y,j,t,p,doi,f'https://pubmed.ncbi.nlm.nih.gov/{p}/',f'https://doi.org/{doi}' if doi else '',''])
rows.sort(key=lambda r:(r[0],r[1]))
sheet(ws,['Priority','Model(s)','Role','First author','Year','Journal','Title','PMID','DOI','PubMed link','DOI link','Downloaded? (tick)'],rows,[9,30,14,16,6,18,60,10,26,32,32,12])

# Sheet 4: still to resolve
ws=wb.create_sheet('Open items')
items=[[d[1],d[9]] for d in D if ('to add' in d[9] or 'verify' in d[9] or 'confirm' in d[9] or 'not PubMed' in d[9] or 'not indexed' in d[9] or 'scope' in d[9] or '?' in d[9])]
sheet(ws,['Model','Issue'],items,[40,80])

# Sheet 5: free in PMC
ws=wb.create_sheet('Free in PMC')
rows=[]
for p,v in oa.items():
    if v:
        a,y,j,t,doi=summ.get(p,['','','','',''])
        rows.append([a,y,j,t,p,v,f'https://pmc.ncbi.nlm.nih.gov/articles/{v}/'])
sheet(ws,['First author','Year','Journal','Title','PMID','PMCID','Link'],sorted(rows,key=lambda r:r[1]),[16,6,20,70,10,12,40])
wb.save(out); print('saved',len(D),'models,',len(need),'PDFs needed')
