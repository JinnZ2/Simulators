# SPDX-License-Identifier: CC0-1.0
# FungalRoot fetch, step 1 of 3, as run 2026-11-23T18:13:56Z to 18:21:12Z.
# Ran inline (python3 - <<heredoc), not from a file: this text is copied from
# the session transcript, with these comment lines added. It stopped itself
# at offset 10200 ("failed at 10200") when the connection slowed; the 10200
# lines it had written are the first 10200 lines of the final extract.
# No data and no taxon table are in this directory.
import json,subprocess,time,sys
key='744edc21-8dd2-474e-8a0b-b8c3d56a3c2d'
out=open('fungalroot_occurrences.jsonl','w'); n=0; off=0
MOF='http://rs.tdwg.org/dwc/terms/MeasurementOrFact'
while True:
    url='https://api.gbif.org/v1/occurrence/search?datasetKey=%s&limit=300&offset=%d'%(key,off)
    for attempt in range(4):
        r=subprocess.run(['curl','-sS','-m','90',url],capture_output=True)
        try: d=json.loads(r.stdout); break
        except Exception: time.sleep(3)
    else: sys.exit('failed at %d'%off)
    for x in d['results']:
        rec={k:x.get(k) for k in('key','occurrenceID','scientificName','species','genus','family','taxonRank','taxonomicStatus','acceptedScientificName')}
        rec['mof']=[[m.get('http://rs.tdwg.org/dwc/terms/measurementType'),m.get('http://rs.tdwg.org/dwc/terms/measurementValue')] for m in x.get('extensions',{}).get(MOF,[]) if m.get('http://rs.tdwg.org/dwc/terms/measurementType')!='Source']
        out.write(json.dumps(rec,sort_keys=True,ensure_ascii=True)+'\n'); n+=1
    off+=300
    if d['endOfRecords'] or not d['results']: break
print(n,d['count'])
