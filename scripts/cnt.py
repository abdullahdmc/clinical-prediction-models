import sys,urllib.request,urllib.parse,json,time
sys.stdout.reconfigure(encoding='utf-8')
def c(q):
    u='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'+urllib.parse.urlencode({'db':'pubmed','term':q,'retmax':0,'retmode':'json'})
    time.sleep(0.4); return json.load(urllib.request.urlopen(u))['esearchresult']['count']
POP='(sepsis[tiab] OR septic[tiab] OR "severe infection"[tiab] OR bacteremia[tiab] OR bacteraemia[tiab] OR "bloodstream infection"[tiab] OR "febrile"[tiab] OR "fever"[ti] OR pneumonia[ti] OR malaria[ti] OR dengue[ti] OR melioidosis[ti] OR "scrub typhus"[ti] OR leptospirosis[ti] OR meningitis[ti] OR "febrile neutropenia"[ti] OR "serious bacterial infection"[tiab] OR "invasive bacterial infection"[tiab])'
MOD_TI='(score[ti] OR scores[ti] OR scoring[ti] OR "prediction model"[ti] OR "prognostic model"[ti] OR "predictive model"[ti] OR "risk model"[ti] OR nomogram[ti] OR "prediction rule"[ti] OR "decision rule"[ti] OR "clinical rule"[ti] OR "risk stratification"[ti] OR "machine learning"[ti] OR "deep learning"[ti] OR "artificial intelligence"[ti] OR algorithm[ti] OR "early warning"[ti] OR calculator[ti] OR criteria[ti] OR tool[ti])'
DEV='(develop*[tiab] OR deriv*[tiab] OR validat*[tiab] OR "external validation"[tiab] OR comparison[tiab] OR compar*[ti] OR performance[tiab] OR accuracy[tiab])'
PERF='(AUC[tiab] OR AUROC[tiab] OR "area under"[tiab] OR "c-statistic"[tiab] OR "c statistic"[tiab] OR "c-index"[tiab] OR discrimination[tiab] OR calibration[tiab] OR sensitivity[tiab])'
HUM='(humans[mh] OR NOT animals[mh]) NOT (review[pt] OR comment[pt] OR editorial[pt] OR letter[pt] OR "case reports"[pt])'
base=f'{POP} AND {MOD_TI} AND {DEV} AND {PERF} AND {HUM}'
print('core (all years):',c(base))
print('core 2000+:',c(base+' AND 2000:2026[dp]'))
print('core ML only:',c(base.replace(MOD_TI,'("machine learning"[tiab] OR "deep learning"[tiab] OR "artificial intelligence"[tiab] OR "random forest"[tiab] OR XGBoost[tiab] OR "neural network"[tiab])')))
print('SRs/MAs of models:',c(f'{POP} AND {MOD_TI} AND (systematic review[pt] OR meta-analysis[pt])'))
open(sys.argv[1],'w').write(base)
