import urllib.request,urllib.parse,json,concurrent.futures,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122');p.mkdir(exist_ok=True)
qs={'eegfnirs':'EEG fNIRS multimodal dataset 60 subjects classification','oral':'oral cancer multimodal images clinical dataset public','olives':'OLIVES multimodal OCT clinical classification github','pcg':'heart murmur multimodal phonocardiogram demographic fusion CirCor github'}
def run(kv):
 k,q=kv
 try:
  u='https://api.openalex.org/works?'+urllib.parse.urlencode({'search':q,'filter':'from_publication_date:2023-01-01,to_publication_date:2026-11-22','per-page':12});b=urllib.request.urlopen(u,timeout=35).read();(p/(k+'.json')).write_bytes(b);d=json.loads(b);print('\n',k)
  for a in d['results'][:10]:print(a['title'],a['doi'],a['open_access']['oa_url'])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(run,qs.items()))
