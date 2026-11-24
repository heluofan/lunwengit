import urllib.request,urllib.parse,json,concurrent.futures,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23')
qs={'direct_kvasir':'DOI:10.7507/1001-5515.202304021','image_retrieval2026':'DOI:10.54364/aaiml.2026.62301','kvasirvqa':'DOI:10.1145/3689096.3689458'}
def get(kv):
 k,q=kv
 try:
  u='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':q,'rows':3});b=urllib.request.urlopen(u,timeout=30).read();(p/(k+'.json')).write_bytes(b);d=json.loads(b)['message']['items'];
  for x in d[:3]:print(k,x.get('title'),x.get('DOI'),x.get('container-title'),x.get('published'),str(x.get('abstract',''))[:1400])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,qs.items()))
