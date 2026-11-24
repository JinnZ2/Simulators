# SPDX-License-Identifier: CC0-1.0
# FungalRoot fetch, step 2 of 3, as run from 2026-11-23T18:27Z and stopped by
# hand after one page (offsets 10200-10299, 140 s). Its output was NOT used:
# the final extract takes lines 1-10200 from step 1 and the rest from step 3.
# Kept because it ran. The body below is the scratch file dl.py, byte for
# byte, under these comment lines.
import json,subprocess,time,sys,os
key='744edc21-8dd2-474e-8a0b-b8c3d56a3c2d'
MOF='http://rs.tdwg.org/dwc/terms/MeasurementOrFact'
T='http://rs.tdwg.org/dwc/terms/'
off=sum(1 for _ in open('fungalroot_occurrences.jsonl'))
out=open('fungalroot_occurrences.jsonl','a')
log=open('dl.log','a')
while True:
    url='https://api.gbif.org/v1/occurrence/search?datasetKey=%s&limit=100&offset=%d'%(key,off)
    t=time.time()
    r=subprocess.run(['curl','-sS','--compressed','-m','900',url],capture_output=True)
    try: d=json.loads(r.stdout)
    except Exception:
        log.write('%s fail at %d\n'%(time.strftime('%FT%TZ',time.gmtime()),off)); log.flush(); time.sleep(20); continue
    for x in d['results']:
        rec={k:x.get(k) for k in('key','occurrenceID','scientificName','species','genus','family','taxonRank','taxonomicStatus','acceptedScientificName')}
        rec['mof']=[[m.get(T+'measurementType'),m.get(T+'measurementValue')] for m in x.get('extensions',{}).get(MOF,[]) if m.get(T+'measurementType')!='Source']
        out.write(json.dumps(rec,sort_keys=True,ensure_ascii=True)+'\n')
    out.flush(); off+=len(d['results'])
    log.write('%s %d %.0fs\n'%(time.strftime('%FT%TZ',time.gmtime()),off,time.time()-t)); log.flush()
    if d['endOfRecords'] or not d['results']: log.write('DONE\n'); break
