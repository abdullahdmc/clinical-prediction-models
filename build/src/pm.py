import sys,json,time,urllib.request,urllib.parse,xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
E='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def get(u,data=None):
    for t in range(4):
        try:
            time.sleep(0.4); return urllib.request.urlopen(u,data=urllib.parse.urlencode(data).encode() if data else None,timeout=90).read()
        except Exception as e: time.sleep(3)
    raise SystemExit('fail '+u)
def search(q,n=5):
    return json.loads(get(E+'esearch.fcgi',{'db':'pubmed','term':q,'retmax':n,'retmode':'json','sort':'relevance'}))['esearchresult']['idlist']
def abstracts(ids):
    x=ET.fromstring(get(E+'efetch.fcgi',{'db':'pubmed','id':','.join(ids),'retmode':'xml'}))
    out={}
    for a in x.iter('PubmedArticle'):
        m=a.find('MedlineCitation'); art=m.find('Article')
        au=art.find('AuthorList/Author')
        out[m.findtext('PMID')]={'title':''.join(art.find('ArticleTitle').itertext()),
          'abstract':' '.join(((t.get('Label')+': ') if t.get('Label') else '')+''.join(t.itertext()) for t in art.iter('AbstractText')),
          'year':art.findtext('Journal/JournalIssue/PubDate/Year') or (art.findtext('Journal/JournalIssue/PubDate/MedlineDate') or '')[:4],
          'journal':art.findtext('Journal/ISOAbbreviation'),'fa':(au.findtext('LastName') or au.findtext('CollectiveName') or '') if au is not None else '',
          'doi':next((i.text for i in a.iter('ArticleId') if i.get('IdType')=='doi'),''),
          'pmc':next((i.text for i in a.iter('ArticleId') if i.get('IdType')=='pmc'),'')}
    return out
