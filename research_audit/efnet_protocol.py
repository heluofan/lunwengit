import pathlib,json,re,urllib.request,urllib.parse,concurrent.futures
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122');nb=json.loads((p/'efnet_source/EF-Net-main/EEG-fNIRS/Deep_Learning_with_EEG+fNIRS_Subjects_Independent.ipynb').read_text())
for c in nb['cells']:
 s=''.join(c.get('source',[]))
 if s.strip():print('CELL',s[:4000])
qs={'efnet_meta':'https://api.openalex.org/works/https://doi.org/10.3390/s24061889','wg_recent':'https://api.openalex.org/works?'+urllib.parse.urlencode({'search':'EEG fNIRS word generation subject independent','filter':'from_publication_date:2024-01-01,to_publication_date:2026-11-22','per-page':20})}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=35).read();(p/(k+'.json')).write_bytes(b);d=json.loads(b)
  if k=='efnet_meta':print(k,d['id'],d.get('cited_by_count'))
  else:
   for a in d['results'][:15]:print(k,a['title'],a['doi'])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(get,qs.items()))
