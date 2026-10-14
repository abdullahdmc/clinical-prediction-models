import urllib.request,urllib.parse,json,time,sys,xml.etree.ElementTree as ET,os
sys.stdout.reconfigure(encoding='utf-8')
Q=open('query2.txt').read()
E='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def req(url,data=None,tries=5):
    for t in range(tries):
        try:
            time.sleep(1.1); return urllib.request.urlopen(url,data=urllib.parse.urlencode(data).encode() if data else None,timeout=120).read()
        except Exception as e: print('retry',e,flush=True); time.sleep(5*(t+1))
    raise SystemExit('failed')
def search(q):
    return json.loads(req(E+'esearch.fcgi',{'db':'pubmed','term':q,'usehistory':'y','retmax':0,'retmode':'json'}))['esearchresult']
ranges=[]
for y in range(1960,2027):
    r=f'{y}/01/01:{y}/12/31[dp]' if y>1985 else None
    if y<=1985:
        if y==1960: ranges.append('1800/01/01:1985/12/31[dp]')
        continue
    ranges.append(r)
out=open(sys.argv[1],'w',encoding='utf-8'); seen=set()
def dorange(rg):
    s=search(f'({Q}) AND {rg}'); n=int(s['count'])
    if n>9500:
        y=rg[:4]
        for a,b in [('01/01','03/31'),('04/01','06/30'),('07/01','09/30'),('10/01','12/31')]: dorange(f'{y}/{a}:{y}/{b}[dp]')
        return
    for st in range(0,n,2000):
        x=req(E+'efetch.fcgi',{'db':'pubmed','query_key':s['querykey'],'WebEnv':s['webenv'],'retstart':st,'retmax':2000,'retmode':'xml'})
        for a in ET.fromstring(x).iter('PubmedArticle'):
            m=a.find('MedlineCitation'); p=m.findtext('PMID')
            if p in seen: continue
            seen.add(p); art=m.find('Article')
            ab=' '.join(((t.get('Label')+': ') if t.get('Label') else '')+''.join(t.itertext()) for t in art.iter('AbstractText'))
            doi=next((i.text for i in a.iter('ArticleId') if i.get('IdType')=='doi'),'')
            yr=(art.findtext('Journal/JournalIssue/PubDate/Year') or (art.findtext('Journal/JournalIssue/PubDate/MedlineDate') or '')[:4])
            au=art.find('AuthorList/Author'); fa=(au.findtext('LastName') or au.findtext('CollectiveName') or '') if au is not None else ''
            out.write(json.dumps({'pmid':p,'title':''.join(art.find('ArticleTitle').itertext()) if art.find('ArticleTitle') is not None else '','abstract':ab,'year':yr,'journal':art.findtext('Journal/ISOAbbreviation'),'doi':doi,'fa':fa,'pt':[t.text for t in art.iter('PublicationType')],'mesh':[d.findtext('DescriptorName') for d in m.iter('MeshHeading')]},ensure_ascii=False)+'\n')
    print(rg,n,'total',len(seen),flush=True)
for y in sys.argv[2].split(','): dorange(f'{y}/01/01:{y}/12/31[dp]')
out.close(); print('DONE',len(seen))
