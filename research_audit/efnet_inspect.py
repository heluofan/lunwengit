import zipfile,pathlib,urllib.request,concurrent.futures,re
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122');z=zipfile.ZipFile(p/'efnet_code.zip');print('TREE',z.namelist());z.extractall(p/'efnet_source')
urls={'data_http':'http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/','data_https':'https://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/','efnet_citations':'https://api.openalex.org/works?filter=cites:W4392873463&per-page=50'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=30).read();(p/(k+'.txt')).write_bytes(b);s=b.decode('utf-8','replace');print(k,len(b),re.sub('<[^>]+>',' ',s)[:5000]);print('LINKS',re.findall(r'href=["\']([^"\']+)',s)[:55])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(get,list(urls.items())[:2]))
