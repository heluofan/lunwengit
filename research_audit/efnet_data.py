import urllib.request,pathlib,concurrent.futures,re,json
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
urls={'efnet_readme':'https://raw.githubusercontent.com/DL4mHealth/EF-Net/main/README.md','efnet_code':'https://codeload.github.com/DL4mHealth/EF-Net/zip/refs/heads/main','berlin':'https://www.bbci.de/supplementary/EEG-fNIRS/','berlin2018':'https://doc.ml.tu-berlin.de/hBCI/'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(p/(k+('.zip' if k=='efnet_code' else '.txt'))).write_bytes(b)
  if k=='efnet_code':print(k,len(b))
  else:
   s=b.decode('utf-8','replace');print(k,re.sub('<[^>]+>',' ',s)[:5500]);print('LINKS',re.findall(r'href=["\']([^"\']+)',s)[:40])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,urls.items()))
