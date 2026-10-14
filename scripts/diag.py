import urllib.request,urllib.parse,json,time,sys,re
sys.stdout.reconfigure(encoding='utf-8')
src=open('cnt.py').read(); exec(src[src.index('POP='):src.index('base=')])
gold=sys.argv[1].split()
def hits(q):
    q='('+q+') AND ('+' OR '.join(p+'[uid]' for p in gold)+')'
    time.sleep(0.4)
    r=json.load(urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?',data=urllib.parse.urlencode({'db':'pubmed','term':q,'retmax':100,'retmode':'json'}).encode()))
    return set(r['esearchresult']['idlist'])
for n,q in [('POP',POP),('MOD_TI',MOD_TI),('DEV',DEV),('PERF',PERF),('HUM',HUM.replace('(humans[mh] OR NOT animals[mh]) NOT','all[sb] NOT'))]:
    h=hits(q); print(n,len(h),'missing:',[g for g in gold if g not in h])
