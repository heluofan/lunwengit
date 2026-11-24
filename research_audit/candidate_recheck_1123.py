import urllib.request,urllib.parse,json,concurrent.futures,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23');p.mkdir(exist_ok=True)
urls={'paper':'https://api.crossref.org/works?'+urllib.parse.urlencode({'query.title':'基于多模态对比学习的小肠视频关键帧检索','rows':3}),'hyper':'https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':'Hyper-Kvasir','size':5}),'hf':'https://huggingface.co/api/datasets?search=Hyper-Kvasir'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(p/(k+'.json')).write_bytes(b);d=json.loads(b)
  if k=='paper':
   for x in d['message']['items']:print(k,x.get('title'),x.get('DOI'),x.get('author'),x.get('link'))
  elif k=='hyper':print(k,[(x['id'],x['metadata']['title'],x['metadata'].get('license'),[(f['key'],f['size']) for f in x.get('files',[])]) for x in d['hits']['hits']])
  else:print(k,[(x['id'],x.get('gated')) for x in d])
 except Exception as e:print(k,type(e).__name__,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,urls.items()))
