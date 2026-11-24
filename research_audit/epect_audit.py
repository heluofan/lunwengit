import pathlib,urllib.request,concurrent.futures,json,urllib.parse,re,zipfile
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'epect_meta':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':'DOI:10.3390/math14132416','format':'json','resultType':'core'}),'epect_readme':'https://raw.githubusercontent.com/yiamcb/EPECT/main/README.md','sta_readme':'https://raw.githubusercontent.com/MutianLiu-SHU/STA-Net/main/README.md','efrm_readme':'https://raw.githubusercontent.com/EuijinMisp/EFRM-A-Multimodal-EEG-fNIRS-Representation-learning-Model/main/README.md','epect_zip':'https://codeload.github.com/yiamcb/EPECT/zip/refs/heads/main'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=30).read();(p/(k+('.zip' if k.endswith('zip') else '.txt'))).write_bytes(b)
  if k.endswith('zip'):
   z=zipfile.ZipFile(p/(k+'.zip'));print(k,len(b),z.namelist()[:50]);z.extractall(p/'epect_source')
  elif k=='epect_meta':
   for x in json.loads(b)['resultList']['result']:print(k,x.get('pmcid'),x.get('abstractText'))
  else:print(k,b.decode('utf-8','replace')[:5500])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(get,qs.items()))
