import sys,os,time,urllib.request,urllib.parse,xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')
os.makedirs('build/src/pmc',exist_ok=True)
def txt(e): return ' '.join(''.join(e.itertext()).split())
for pmc in sys.argv[1:]:
    time.sleep(0.5)
    x=urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'+urllib.parse.urlencode({'db':'pmc','id':pmc.replace('PMC',''),'retmode':'xml'}),timeout=120).read()
    r=ET.fromstring(x); out=[]
    t=r.find('.//article-title'); out.append('TITLE: '+(txt(t) if t is not None else ''))
    body=r.find('.//body')
    if body is None: out.append('NO BODY (not in OA subset)')
    for tw in r.iter('table-wrap'):
        cap=tw.find('caption'); lab=tw.findtext('label') or ''
        out.append(f'\n=== {lab} {txt(cap) if cap is not None else ""}')
        for tr in tw.iter('tr'):
            out.append(' | '.join(txt(c) for c in tr if c.tag in('td','th')))
        fn=tw.find('table-wrap-foot')
        if fn is not None: out.append('FOOT: '+txt(fn)[:1500])
    # boxes (often hold criteria)
    for bx in r.iter('boxed-text'): out.append('\n=== BOX: '+txt(bx)[:3000])
    open(f'build/src/pmc/{pmc}.txt','w',encoding='utf-8').write('\n'.join(out))
    print(pmc,len('\n'.join(out)),'chars', 'NO BODY' if body is None else '')
