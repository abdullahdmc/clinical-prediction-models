import sys; sys.stdout.reconfigure(encoding="utf-8",errors="replace")
import urllib.request,urllib.parse,json,sys,time
B='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def s(q,n=8,sort='relevance'):
    u=B+'esearch.fcgi?'+urllib.parse.urlencode({'db':'pubmed','term':q,'retmax':n,'retmode':'json','sort':sort})
    r=json.load(urllib.request.urlopen(u)); ids=r['esearchresult']['idlist']; cnt=r['esearchresult']['count']
    out=[]
    if ids:
        time.sleep(0.35)
        d=json.load(urllib.request.urlopen(B+'esummary.fcgi?db=pubmed&retmode=json&id='+','.join(ids)))['result']
        out=[(i,d[i].get('pubdate','')[:4],d[i].get('source',''),d[i].get('title','')[:150]) for i in ids]
    time.sleep(0.35); return cnt,out
for line in open(sys.argv[1],encoding='utf-8'):
    line=line.strip()
    if not line: continue
    lab,q=line.split('|',1)
    try: c,o=s(q)
    except Exception as e: print('ERR',lab,e); continue
    print(f'\n### {lab}  (n={c})')
    for x in o: print('  ',x[0],x[1],x[2],'|',x[3])
