import json,os,sys,collections
from openpyxl import load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
T=os.environ['TEMP']+'/pm/'
P=json.load(open(T+'classified.json'))
f=sys.argv[1]; wb=load_workbook(f)
H=Font(bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='1F4E78')
def sheet(name,head,data,widths,freeze='A2'):
    if name in wb.sheetnames: del wb[name]
    ws=wb.create_sheet(name); ws.append(head)
    for c in ws[1]: c.font=H; c.fill=HF; c.alignment=Alignment(wrap_text=True,vertical='top')
    for r in data: ws.append(r)
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
    ws.freeze_panes=freeze; ws.auto_filter.ref=ws.dimensions; return ws
yint=lambda p: int(p['year']) if str(p['year']).isdigit() else 0
# 1 Search log
log=json.load(open(T+'searchlog.json'))
sheet('Search log',['Item','Value'],log,[34,120])
# 2 Evidence map: disease x outcome counts (development / validation / ML)
dis=sorted({p['disease'] for p in P}); outs=['Mortality','Sepsis / septic shock onset or diagnosis','Bacteraemia / SBI / bacterial vs viral','ICU admission / deterioration','Organ dysfunction (AKI/ARDS/DIC/liver/encephalopathy)','Severe disease progression']
data=[]
for d in dis:
    sub=[p for p in P if p['disease']==d]
    for o in outs:
        s=[p for p in sub if o in p['outcome']]
        if not s: continue
        data.append([d,o,len(s),sum(p['dev'] for p in s),sum(p['ext'] for p in s),sum(p['comp'] for p in s),sum(p['ml'] for p in s),sum(p['ml'] and p['dev'] for p in s),sum(p['lmic'] for p in s),sum(yint(p)>=2024 for p in s)])
data.sort(key=lambda r:(r[0],-r[2]))
sheet('Evidence map',['Disease / condition','Outcome predicted','Papers','Model development','External validation','Comparison of tools','Uses ML','ML model development','LMIC setting','Published 2024-2026'],data,[30,40,9,12,12,12,9,12,10,12])
# 3 Under development: recent (2023+) development papers WITH external validation, by disease
data=[]
for p in P:
    if yint(p)>=2023 and p['dev'] and p['ext'] and not p['sr'] and p['hasabs']:
        data.append([p['disease'],'; '.join(p['outcome']) or 'Unclassified',p['pop'],'ML' if p['ml'] else 'Regression/score','Yes' if p['lmic'] else '',p['fa'],yint(p),p['journal'],p['title'],p['pmid'],f"https://pubmed.ncbi.nlm.nih.gov/{p['pmid']}/"])
data.sort(key=lambda r:(r[0],r[3],-r[6]))
sheet('Under development (2023+)',['Disease / condition','Outcome(s)','Population','Method','LMIC','First author','Year','Journal','Title','PMID','PubMed'],data,[24,30,12,14,6,14,6,18,70,10,32])
# 4 Systematic reviews of prediction models (source lists)
data=[[p['disease'],'; '.join(p['outcome']),'ML' if p['ml'] else '',p['fa'],yint(p),p['journal'],p['title'],p['pmid'],f"https://pubmed.ncbi.nlm.nih.gov/{p['pmid']}/"] for p in P if p['sr']]
data.sort(key=lambda r:(r[0],-r[4]))
sheet('Model reviews (SR-MA)',['Disease / condition','Outcome(s)','ML','First author','Year','Journal','Title','PMID','PubMed'],data,[24,30,5,14,6,18,70,10,32])
wb.save(f); print('written: evidence map',len(data))
