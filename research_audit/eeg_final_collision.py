import urllib.request,urllib.parse,json,pathlib,concurrent.futures
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'latency_distillation':'EEG fNIRS early prediction distillation short window','stecanet_meta2':'STeCANet spatio temporal cross attention network','early_fnirs':'EEG fNIRS short time window classification'}
def get(kv):
 k,q=kv
 try:
  b=urllib.request.urlopen('https://api.openalex.org/works?'+urllib.parse.urlencode({'search':q,'filter':'from_publication_date:2023-01-01,to_publication_date:2026-11-22','per-page':10}),timeout=25).read();(p/(k+'.json')).write_bytes(b)
  for x in json.loads(b)['results'][:6]:print(k,x['title'],x['doi'])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,qs.items()))
