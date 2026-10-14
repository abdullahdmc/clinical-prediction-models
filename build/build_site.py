"""Build the Infection Model Tracker website.

Inputs : build/src/content.py (curated models), Prediction_Model_Gap_Analysis.xlsx (catalogue),
         data/h2h_extract.tsv + data/serial_ids.json (head-to-head results), data/classified.json (search)
Outputs: docs/index.html (GitHub Pages site), docs/data.json, build/artifact.html (for publishing)
Run    : python -I build/build_site.py
"""
import sys, os, json, csv, re, collections, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'build', 'src'))
from content import SECTIONS, MODELS, ML_TOOLS, MD
from content2 import MODELS2
from pm import abstracts
import openpyxl

P = lambda *a: os.path.join(ROOT, *a)
UPDATED = '2026-10-14'

# ---------------------------------------------------------------- catalogue-level models
DOMAIN2SEC = {'Sepsis / organ dysfunction (adult)': 'adult-sepsis', 'ICU mortality / severity': 'icu', 'Early warning & ED triage': 'ed-ward',
 'Paediatric sepsis & severity': 'paeds', 'Neonatal & febrile infant': 'neonatal', 'Pneumonia & respiratory infection': 'pneumonia',
 'Bacteraemia & specific infections': 'bacteraemia', 'Tropical infections & febrile illness': 'tropical', 'Organ-specific complications (AKI, liver)': 'organ',
 'Maternal / obstetric sepsis': 'obstetric', 'Sepsis endotypes / phenotypes (research)': 'endotypes', 'Composite laboratory indices (research)': 'endotypes'}
# catalogue names already covered by a curated model (prefix match)
COVERED = {'SOFA': 'sofa', 'SOFA-2': 'sofa2', 'qSOFA': 'qsofa', 'Lactate-': 'lqsofa-adult', 'SIRS': 'sirs', 'MODS': 'mods', 'LODS (Logistic': 'lods', 'PIRO': 'pirom',
 'MEDS': 'meds', 'APACHE II': 'apache2', 'APACHE IV': 'apache4', 'SAPS II': 'saps2', 'SAPS 3': 'saps3', 'MPM': 'mpm', 'TropICS': 'tropics', 'R-MPM': 'rmpm',
 'SMS-ICU': 'smsicu', 'NEWS': 'news2', 'MEWS': 'mews', 'REMS': 'rems', 'UVA': 'uva', 'Phoenix': 'phoenix', 'pSOFA': 'psofa', 'PELOD': 'pelod2', 'PRISM': 'prism',
 'PIM3': 'pim3', 'Liverpool': 'lqsofa', 'PERSEVERE': 'persevere', 'SICK': 'sick', 'Lambarene': 'lambarene', 'Smart Triage': 'smarttriage', 'Smart Discharge': 'smartdischarge',
 'sTREM-1': 'strem1', 'Paediatric pneumonia: RISC': 'risc', 'Kaiser Early': 'kaisereos', 'nSOFA': 'nsofa', 'PECARN': 'pecarn', 'Step-by-Step': 'stepbystep',
 'AAP 2021': 'aap2021', 'Lab-score': 'labscore', 'mSOFA': 'msofa', 'SNAPPE': 'snappe', 'MPM II': 'mpm'}
SKIP = ('Sepsis ML systematic reviews', 'Malaria prognostic models (systematic review)')
CALC = {'CURB-65': '324/curb-65-score-pneumonia-severity', 'PSI': '33/psi-port-score-pneumonia-severity-index-cap', 'SMART-COP': '3914/smart-cop-score-pneumonia-severity',
 'SCAP': '10280/severe-community-acquired-pneumonia-scap-score', 'ISARIC 4C': '10338/4c-mortality-score-covid-19', 'qCSI': '10304/quick-covid-19-severity-index-qcsi',
 'COVID-GRAM': '10303/covid-gram-critical-illness-risk-score', 'PRIEST': '10369/priest-covid-19-clinical-severity-score', 'ROX': '10302/rox-index-intubation-hfnc',
 'HACOR': '10460/hacor-score', 'CPIS': '3278/clinical-pulmonary-infection-score-cpis-ventilator-associated-pneumonia-vap', 'LIPS': '10281/lung-injury-prediction-score-lips',
 '2023 Duke': '10564/2023-duke-international-society-cardiovascular-infectious-diseases-iscvid-criteria', 'LRINEC': '1734/lrinec-score-necrotizing-soft-tissue-infection',
 'MASCC': '3913/mascc-risk-index-febrile-neutropenia', 'CISNE': '3997/clinical-index-stable-febrile-neutropenia-cisne', 'Bacterial Meningitis': '3911/bacterial-meningitis-score-children',
 'ATLAS': '10218/atlas-score-clostridium-difficile-infection', 'ISTH': '10203/isth-criteria-disseminated-intravascular-coagulation-dic', 'SIC': '10301/sepsis-induced-coagulopathy-sic-score',
 'Shapiro': '10513/shapiro-rule', 'RIFLE': '10019/rifle-criteria-acute-kidney-injury-aki', 'MELD': '10437/model-end-stage-liver-disease-meld',
 'CLIF': '10240/clif-c-aclf-acute-chronic-liver-failure', 'NUTRIC': '4011/nutrition-risk-critically-ill-nutric-score'}

def bucket(status):
    s = status.lower()
    if any(k in s for k in ('new', 'under development', 'research', 'implementation', 'reference')): return 'developing'
    if any(k in s for k in ('routine', 'guideline', 'international definition', 'in use', 'in wide use', 'cleared', 'authorised', 'legacy', 'superseded', 'regional use')): return 'inuse'
    return 'validated'

def load_catalogue(cats=()):
    if not os.path.exists(P('Prediction_Model_Gap_Analysis.xlsx')): return []  # workbook is kept locally, not in the repo
    wb = openpyxl.load_workbook(P('Prediction_Model_Gap_Analysis.xlsx'), read_only=True)
    rows = list(wb['Master catalogue'].iter_rows(values_only=True)); h = rows[0]
    ix = {k: h.index(k) for k in h if k}
    out = []
    for r in rows[1:]:
        dom, name = r[ix['Outcome domain']], r[ix['Model']]
        if not name or dom not in DOMAIN2SEC or name.startswith(SKIP): continue
        if any(name.startswith(k) for k in COVERED) or any(name.startswith(c) for c in cats): continue
        orig = str(r[ix['Originator PMID']] or '').strip()
        upd = [u.strip() for u in str(r[ix['Key update / validation PMID(s)']] or '').split(';') if u.strip().isdigit()]
        calc = next(([('MDCalc: ' + name.split(' (')[0], MD + v)] for k, v in CALC.items() if name.startswith(k)), [])
        note = str(r[ix['Notes']] or '')
        note = re.sub(r'\s*\|\s*In ML box.*', '', note)
        out.append(dict(id=re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:40], name=name, full='', section=DOMAIN2SEC[dom],
            type=r[ix['Model type']] or '', status=r[ix['Status (in use / developing)']] or '', population=r[ix['Population / setting']] or '',
            predicts='', components=None, scoring='', cutoffs=[], originator=(orig, '') if orig.isdigit() else ('', ''), updates=[(u, '') for u in upd],
            gold='', performance=[], calculators=calc, related=[], evidence='catalogue',
            evnote=note, papers=r[ix['Papers in new search']] if 'Papers in new search' in ix else None))
    return out

# ---------------------------------------------------------------- references
def refs_for(models, extra):
    ids = set(extra)
    for m in models:
        if m['originator'][0]: ids.add(m['originator'][0])
        ids.update(u[0] for u in m['updates'] if u[0]); ids.update(p[4] for p in m['performance'] if len(p) > 4 and p[4])
    ids.update(t['pmid'] for t in ML_TOOLS)
    cache_f = P('build', 'src', 'refs.json')
    cache = json.load(open(cache_f, encoding='utf-8')) if os.path.exists(cache_f) else {}
    need = sorted(i for i in ids if i and i not in cache)
    for i in range(0, len(need), 150): cache.update(abstracts(need[i:i + 150]))
    json.dump(cache, open(cache_f, 'w', encoding='utf-8'), ensure_ascii=False)
    out = {}
    for i in ids:
        a = cache.get(i)
        if not a: continue
        out[i] = dict(cite=f"{a['fa']} et al. {a['journal']} {a['year']}", title=a['title'], doi=a.get('doi', ''), pmc=a.get('pmc', ''))
    return out

# ---------------------------------------------------------------- head-to-head
NAME2ID = {'SOFA': 'sofa', 'qSOFA': 'qsofa', 'SIRS': 'sirs', 'APACHE II': 'apache2', 'SAPS II': 'saps2', 'MEDS': 'meds', 'NEWS': 'news2', 'NEWS2': 'news2', 'MEWS': 'mews'}
def load_h2h():
    ids = json.load(open(P('data', 'serial_ids.json')))
    rows = list(csv.DictReader(open(P('data', 'h2h_extract.tsv'), encoding='utf-8'), delimiter='\t'))
    studies = collections.OrderedDict()
    for r in rows:
        s = studies.setdefault(r['serial'], dict(pmid=ids[r['serial']][0], author=r['author'], year=int(r['year']), setting=r['setting'], population=r['age'],
                                                 n=int(r['n']), outcome=r['outcome'], results=[]))
        base = re.sub(r'\s*\(.*\)$', '', r['model']).strip()
        combo = '+' in r['model'] or base not in NAME2ID
        s['results'].append(dict(model=r['model'], id=None if combo else NAME2ID.get(base), auc=float(r['auc']), ci=r['ci'], derived=r['value_type'] == 'derived',
                                 combo=combo, note=r['note']))
    out = list(studies.values())
    for s in out:
        o = s['outcome'].lower()
        s['group'] = 'Mortality' if 'mortality' in o or 'death' in o else ('Sepsis diagnosis or onset' if 'sepsis' in o else 'Other outcomes')
    return out

# ---------------------------------------------------------------- pipeline from search
def section_of(p):
    pop, dis, outc = p['pop'], p['disease'], p['outcome']
    if pop == 'Neonatal': return 'neonatal'
    if pop == 'Obstetric': return 'obstetric'
    if pop == 'Paediatric': return 'paeds'
    if dis in ('COVID-19', 'Pneumonia / respiratory'): return 'pneumonia'
    if dis in ('Malaria', 'Dengue', 'Other tropical'): return 'tropical'
    if dis in ('Febrile neutropenia / immunocompromised', 'Meningitis / CNS', 'UTI / urosepsis', 'Skin & soft tissue', 'Endocarditis / S. aureus', 'Fungal', 'C. difficile'): return 'bacteraemia'
    if dis == 'Sepsis (general)':
        if 'Organ dysfunction (AKI/ARDS/DIC/liver/encephalopathy)' in outc and 'Mortality' not in outc: return 'organ'
        if 'ICU admission / deterioration' in outc: return 'ed-ward'
        return 'adult-sepsis'
    return None

def load_pipeline():
    if not os.path.exists(P('data', 'classified.json')):  # large search file is kept locally; reuse last build
        old = json.load(open(P('docs', 'data.json'), encoding='utf-8'))
        return old['pipeline'], old['ml'], old['stats']['searched']
    C = json.load(open(P('data', 'classified.json')))
    yr = lambda p: int(p['year']) if str(p['year']).isdigit() else 0
    per = collections.defaultdict(list)
    for p in C:
        if p['dev'] and p['ext'] and not p['sr'] and p['hasabs'] and yr(p) >= 2023:
            s = section_of(p)
            if s: per[s].append(p)
    pipe = {}
    for s, L in per.items():
        L.sort(key=lambda p: (-yr(p), not p['lmic']))
        pipe[s] = dict(n=len(L), ml=sum(p['ml'] for p in L), lmic=sum(p['lmic'] for p in L),
                       recent=[dict(pmid=p['pmid'], title=p['title'], year=yr(p), journal=p['journal'], fa=p['fa'], ml=p['ml'], lmic=p['lmic']) for p in L[:8]])
    mlyear = collections.Counter(yr(p) for p in C if p['ml'] and p['dev'] and not p['sr'])
    ml_recent = [p for p in C if p['ml'] and p['dev'] and p['ext'] and not p['sr'] and yr(p) >= 2024 and p['disease'] == 'Sepsis (general)']
    ml_recent.sort(key=lambda p: -yr(p))
    return pipe, dict(byyear={y: mlyear.get(y, 0) for y in range(2012, 2027)}, total=sum(1 for p in C if p['ml']),
                      dev_ext=sum(1 for p in C if p['ml'] and p['dev'] and p['ext'] and not p['sr']),
                      recent=[dict(pmid=p['pmid'], title=p['title'], year=yr(p), journal=p['journal'], fa=p['fa'], lmic=p['lmic']) for p in ml_recent[:12]]), len(C)

# ---------------------------------------------------------------- assemble
def main():
    curated = [dict(m) for m in MODELS + MODELS2]
    cat = load_catalogue([m['cat'] for m in MODELS2 if m.get('cat')])
    if cat: print('Catalogue rows without a sheet:', [m['name'] for m in cat])
    models = curated + cat
    seen = set()
    for m in models:
        while m['id'] in seen: m['id'] += '-2'
        seen.add(m['id']); m['bucket'] = bucket(m['status']); m.setdefault('lmic', False)
    h2h = load_h2h()
    pipe, ml, nsearch = load_pipeline()
    refs = refs_for(models, [s['pmid'] for s in h2h])
    for m in models:  # normalise tuples to dicts
        m['originator'] = dict(pmid=m['originator'][0], label=m['originator'][1])
        m['updates'] = [dict(pmid=u[0], label=u[1]) for u in m['updates']]
        m['performance'] = [dict(auc=p[0], ci=p[1], outcome=p[2], setting=p[3], pmid=p[4] if len(p) > 4 else '') for p in m['performance']]
        m['cutoffs'] = [dict(at=c[0], means=c[1]) for c in m['cutoffs']]
        m['calculators'] = [dict(label=c[0], url=c[1]) for c in m['calculators']]
        m['related'] = [dict(id=r[0], note=r[1]) for r in m['related']]
    data = dict(updated=UPDATED, nextUpdate='October 2027', sections=SECTIONS, models=models, ml_tools=ML_TOOLS, h2h=h2h, pipeline=pipe, ml=ml, refs=refs,
                stats=dict(searched=nsearch, models=len(models), curated=len(curated), h2h_results=sum(len(s['results']) for s in h2h), h2h_studies=len(h2h)))
    os.makedirs(P('docs'), exist_ok=True)
    open(P('docs', '.nojekyll'), 'w').close()
    js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    json.dump(data, open(P('docs', 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tpl = open(P('build', 'template.html'), encoding='utf-8').read()
    body = tpl.replace('/*__DATA__*/null', js)
    open(P('build', 'artifact.html'), 'w', encoding='utf-8').write(body)
    full = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + body.replace('</style>', '</style></head><body>', 1) + '\n</body></html>')
    open(P('docs', 'index.html'), 'w', encoding='utf-8').write(full)
    print(f"models {len(models)} (curated {len(curated)}), h2h studies {len(h2h)}, refs {len(refs)}, sections w/ pipeline {len(pipe)}, size {len(body)//1024} KB")

if __name__ == '__main__':
    main()
