import urllib.request,urllib.parse,json,pathlib,concurrent.futures,re
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23')
qs={'dken_exact':'DKEN Data Knowledge Enhanced medical visual question answering','mcam_exact':'CAMF medical visual question answering contextual multi-level feature fusion','vqa_slake_methods':'medical VQA dataset SLAKE public baseline code','slake_data':'SLAKE Medical VQA GitHub dataset'}
def get(kv):
 k,q=kv
 try:
  u='https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':q,'per_page':10});b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read();(p/(k+'.json')).write_bytes(b);print(k,[(x['full_name'],x.get('description')) for x in json.loads(b).get('items',[])])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,qs.items()))
