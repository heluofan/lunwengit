import urllib.request,urllib.parse,json,concurrent.futures,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'hypotension':'intraoperative hypotension non invasive ECG PPG multimodal github VitalDB','breathing':'multimodal respiratory sound demographic classification github SPRSound','retinal':'OLIVES clinical biomarkers OCT multimodal github'}
def get(kv):
 k,q=kv
 try:
  b=urllib.request.urlopen('https://api.openalex.org/works?'+urllib.parse.urlencode({'search':q,'filter':'from_publication_date:2023-01-01,to_publication_date:2026-11-22','per-page':12}),timeout=30).read();(p/(k+'_search.json')).write_bytes(b)
  for x in json.loads(b)['results'][:10]:print(k,x['title'],x['doi'],x['open_access']['oa_url'])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,qs.items()))
