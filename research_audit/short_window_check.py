from pathlib import Path
import urllib.request,urllib.parse,json,concurrent.futures
p=Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'early_wg_extra':'word generation EEG fNIRS low latency classification','fnirs_delay':'Rethinking Delayed Hemodynamic Responses for fNIRS Classification'}
def get(kv):
 k,q=kv
 try:
  b=urllib.request.urlopen('https://api.openalex.org/works?'+urllib.parse.urlencode({'search':q,'per-page':8}),timeout=25).read();(p/(k+'.json')).write_bytes(b)
  for x in json.loads(b)['results'][:6]:print(k,x['title'],x['doi'])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(get,qs.items()))
