from pathlib import Path
import urllib.request,json,re,concurrent.futures
p=Path(r'C:\lunwen\research_audit\new_direction_20261122')
urls={'steca_crossref':'https://api.crossref.org/works/10.1088/1741-2552/ae2954','steca_pdf':'https://iopscience.iop.org/article/10.1088/1741-2552/ae2954/pdf','steca_publisher':'https://iopscience.iop.org/article/10.1088/1741-2552/ae2954'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read();(p/(k+('.pdf' if b.startswith(b'%PDF') else '.txt'))).write_bytes(b)
  if k=='steca_crossref':
   d=json.loads(b)['message'];print(k,d.get('author'),d.get('link'))
  else:print(k,len(b),b[:100])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,urls.items()))
