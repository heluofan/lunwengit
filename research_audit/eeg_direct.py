import urllib.request,urllib.parse,json,concurrent.futures,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'dbstf':'DOI:10.3390/brainsci16020241','mbc':'DOI:10.3389/fnhum.2025.1660532','mgf':'DOI:10.3390/s26113402','steca':'DOI:10.1088/1741-2552/ae2954','nvc':'DOI:10.1007/s40747-026-02580-1'}
def get(kv):
 k,q=kv
 try:
  u='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':q,'format':'json','resultType':'core'});b=urllib.request.urlopen(u,timeout=30).read();(p/(k+'_meta.json')).write_bytes(b)
  for x in json.loads(b)['resultList']['result']:print(k,x.get('pmcid'),x.get('title'),x.get('abstractText'),x.get('fullTextUrlList'))
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(get,qs.items()))
