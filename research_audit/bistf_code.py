import urllib.request,pathlib,concurrent.futures,re,json,zipfile
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
urls={'bistf_readme':'https://raw.githubusercontent.com/zc701/BiSTF-Net/main/README.md','bistf_zip':'https://codeload.github.com/zc701/BiSTF-Net/zip/refs/heads/main','efnet_cites':'https://api.openalex.org/works?filter=cites:W4392847183&per-page=100'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=30).read();(p/(k+('.zip' if k.endswith('zip') else '.txt'))).write_bytes(b)
  if k.endswith('zip'):
   z=zipfile.ZipFile(p/(k+'.zip'));print(k,len(b),z.namelist()[:45]);z.extractall(p/'bistf_source')
  elif k=='efnet_cites':
   d=json.loads(b);print(k,d['meta']['count']);print('\n'.join(x['title']+' '+str(x['doi']) for x in d['results'] if any(w in x['title'].lower() for w in ['fnirs','f-nirs','cross','multimodal'])))
  else:print(k,b.decode('utf-8','replace')[:5000])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,urls.items()))
