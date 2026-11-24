import urllib.request,urllib.parse,json,concurrent.futures,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'fd_hypo':'DOI:10.1109/jbhi.2024.3403109','framework':'DOI:10.1109/jbhi.2025.3583044','hypobrid':'DOI:10.1186/s12871-026-03888-8','vitalpaper':'DOI:10.1038/s41597-022-01411-5'}
def get(kv):
 k,q=kv
 try:
  b=urllib.request.urlopen('https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':q,'format':'json','resultType':'core'}),timeout=30).read();(p/(k+'_meta.json')).write_bytes(b)
  for x in json.loads(b)['resultList']['result']:print(k,x.get('pmcid'),x.get('title'),x.get('abstractText'),x.get('fullTextUrlList'))
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,qs.items()))
