# SPDX-License-Identifier: CC0-1.0
# FungalRoot fetch, step 3 of 3, as run 2026-11-23T18:31:35Z to about 19:10Z:
# offsets 10200-36514 in pages of 100 on 16 connections (the proxy held each
# connection near 4 KB/s). The body below is the scratch file pdl.py, byte
# for byte, under these comment lines.
# Before it, in the same shell:   head -10200 fungalroot_occurrences.jsonl > first.jsonl
# After it, the extract:          cat first.jsonl $(ls pages/*.jsonl | sort) > fungalroot_occurrences_full.jsonl
# Extract as fetched: 36515 lines, 14523948 bytes, sha256
# 430ab42cadb7412deeb7fa9f81ae8e0cb8f9c8c60bba23bc5c125b8834410980
import json,subprocess,time,os
from concurrent.futures import ThreadPoolExecutor
key='744edc21-8dd2-474e-8a0b-b8c3d56a3c2d'
MOF='http://rs.tdwg.org/dwc/terms/MeasurementOrFact'; T='http://rs.tdwg.org/dwc/terms/'
def get(off):
    fn='pages/%06d.jsonl'%off
    if os.path.exists(fn): return off,'have'
    url='https://api.gbif.org/v1/occurrence/search?datasetKey=%s&limit=100&offset=%d'%(key,off)
    for a in range(6):
        r=subprocess.run(['curl','-sS','--compressed','-m','600',url],capture_output=True)
        try:
            d=json.loads(r.stdout); assert d['offset']==off; break
        except Exception: time.sleep(15)
    else: return off,'FAIL'
    L=[]
    for x in d['results']:
        rec={k:x.get(k) for k in('key','occurrenceID','scientificName','species','genus','family','taxonRank','taxonomicStatus','acceptedScientificName')}
        rec['mof']=[[m.get(T+'measurementType'),m.get(T+'measurementValue')] for m in x.get('extensions',{}).get(MOF,[]) if m.get(T+'measurementType')!='Source']
        L.append(json.dumps(rec,sort_keys=True,ensure_ascii=True)+'\n')
    open(fn+'.tmp','w').write(''.join(L)); os.rename(fn+'.tmp',fn)
    return off,'%d count=%d'%(len(L),d['count'])
with ThreadPoolExecutor(16) as ex:
    for off,st in ex.map(get,range(10200,36600,100)):
        print(time.strftime('%T',time.gmtime()),off,st,flush=True)
print('DONE')
