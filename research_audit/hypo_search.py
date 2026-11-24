import urllib.request,urllib.parse,json,concurrent.futures,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'hypo2':'VitalDB hypotension prediction','hypo3':'noninvasive hypotension deep learning','ecgppg':'multimodal electrocardiogram photoplethysmogram hypotension'}
def get(kv):
 k,q=kv
 try:
  b=urllib.request.urlopen('https://api.openalex.org/works?'+urllib.parse.urlencode({'search':q,'filter':'from_publication_date:2023-01-01,to_publication_date:2026-11-22','per-page':20}),timeout=30).read();(p/(k+'.json')).write_bytes(b)
  print(k)
  for x in json.loads(b)['results'][:15]:print(x['title'],x['doi'])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,qs.items()))
