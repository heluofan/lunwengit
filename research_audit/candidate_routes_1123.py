from pathlib import Path
import urllib.request,urllib.parse,json,concurrent.futures,re
p=Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'hyper_paper':'https://api.crossref.org/works/10.1038/s41597-020-00622-y','slake_github':'https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':'SLAKE medical VQA','per_page':5}),'vqa_rad_github':'https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':'VQA-RAD medical visual question answering','per_page':5}),'hyper_hub':'https://hyper-kvasir.github.io/','hyper_github':'https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':'KRCL medical video keyframe retrieval Hyper-Kvasir','per_page':5})}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(p/(k+'.txt')).write_bytes(b)
  if k.endswith('github'):
   print(k,[(x['full_name'],x.get('description'),x.get('html_url')) for x in json.loads(b).get('items',[])])
  elif k=='hyper_paper':
   d=json.loads(b)['message'];print(k,d.get('title'),d.get('link'),d.get('license'))
  else: print(k,len(b),re.sub('<[^>]+>',' ',b.decode('utf-8','replace'))[:1300],re.findall(r'href=["\']([^"\']+)',b.decode('utf-8','replace'))[:18])
 except Exception as e:print(k,type(e).__name__,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(get,qs.items()))
