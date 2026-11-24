import urllib.request,urllib.parse,json,pathlib,concurrent.futures
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23')
urls={'osf_api':'https://api.osf.io/v2/nodes/mh9sj/','hyper_kaggle':'https://www.kaggle.com/api/v1/datasets/list?search=Hyper-Kvasir','hyper_zenodo':'https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':'HyperKvasir','size':5}),'retrieval_comp':'https://api.openalex.org/works?'+urllib.parse.urlencode({'search':'medical endoscopy video text retrieval Hyper-Kvasir keyframe','filter':'from_publication_date:2023-01-01,to_publication_date:2026-11-23','per-page':25})}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(p/(k+'.json')).write_bytes(b);d=json.loads(b)
  if k=='osf_api':print(k,d.get('data',{}).get('attributes'),[(x.get('id'),x.get('type')) for x in d.get('data',{}).get('relationships',{}).values()])
  elif k=='hyper_kaggle':print(k,[(x.get('ref'),x.get('totalBytes')) for x in d])
  elif k=='hyper_zenodo':print(k,[(x['id'],x['metadata'].get('title')) for x in d['hits']['hits']])
  else:
   for x in d['results'][:20]:print(k,x['title'],x['doi'],x['publication_year'])
 except Exception as e:print(k,type(e).__name__,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,urls.items()))
