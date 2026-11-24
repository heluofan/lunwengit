import urllib.request,urllib.parse,json,concurrent.futures,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
urls={'hf_cesm':'https://huggingface.co/api/datasets?search=CDD-CESM','cesm_zenodo':'https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':'"CDD-CESM"','size':8}),'kaggle_cesm_v2':'https://www.kaggle.com/api/v1/datasets/list?search=cesm&page=1','prostate_recent':'https://api.openalex.org/works?'+urllib.parse.urlencode({'search':'Prostate158','filter':'from_publication_date:2024-01-01,to_publication_date:2026-11-22','per-page':50})}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(p/(k+'.json')).write_bytes(b);d=json.loads(b)
  if k=='prostate_recent':
   print(k,d['meta']['count']);print('\n'.join(x['title']+' '+str(x['doi']) for x in d['results'][:25]))
  elif k=='cesm_zenodo':print(k,[(x['id'],x['metadata']['title'],[(f['key'],f['size']) for f in x.get('files',[])]) for x in d['hits']['hits']])
  elif k.startswith('kaggle'):print(k,[(x.get('ref'),x.get('totalBytes')) for x in d])
  else: print(k,[(x['id'],x.get('gated')) for x in d])
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,urls.items()))
