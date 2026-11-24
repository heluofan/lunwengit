import urllib.request,urllib.parse,json,pathlib,concurrent.futures
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23')
qs=['KRCL Hyper-Kvasir','keyframe retrieval medical video CLIP','Small bowel video keyframe retrieval','Xing Wu KRCL']
def get(q):
 try:
  u='https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':q,'per_page':10});b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read();d=json.loads(b);print('\n',q,[(x['full_name'],x.get('description')) for x in d.get('items',[])])
 except Exception as e:print(q,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,qs))
