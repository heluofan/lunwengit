import urllib.request,urllib.parse,json,pathlib,concurrent.futures
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'delay_meta':'DOI:10.1109/tnsre.2023.3330911','scdm_meta':'DOI:10.1109/tmi.2025.3532480','steca_full_meta':'DOI:10.1088/1741-2552/ae2954'}
def get(kv):
 k,q=kv
 try:
  b=urllib.request.urlopen('https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':q,'format':'json','resultType':'core'}),timeout=25).read();(p/(k+'.json')).write_bytes(b)
  for x in json.loads(b)['resultList']['result']:print(k,x.get('abstractText'),x.get('pmcid'))
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,qs.items()))
