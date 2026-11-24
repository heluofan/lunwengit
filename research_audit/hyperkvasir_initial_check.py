import urllib.request,urllib.parse,pathlib,re,json,concurrent.futures
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23');p.mkdir(exist_ok=True)
urls={'hyper_official':'https://datasets.simula.no/hyper-kvasir/','hyper_repo':'https://api.github.com/repos/Simula-Research-Laboratory/HyperKvasir','clip4clip_readme':'https://raw.githubusercontent.com/ArrowLuo/CLIP4Clip/master/README.md','clip4clip_repo':'https://api.github.com/repos/ArrowLuo/CLIP4Clip'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(p/(k+'.txt')).write_bytes(b);s=b.decode('utf-8','replace')
  if k.endswith('repo'):
   d=json.loads(s);print(k,d.get('full_name'),d.get('license'),d.get('size'),d.get('pushed_at'),d.get('stargazers_count'),d.get('open_issues_count'),d.get('html_url'))
  else:
   clean=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s));print(k,clean[:3500]);print('links',re.findall(r'href=["\']([^"\']+)',s)[:35])
 except Exception as e:print(k,type(e).__name__,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,urls.items()))
