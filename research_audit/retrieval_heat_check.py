import urllib.request,urllib.parse,json,pathlib,concurrent.futures
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23')
qs=['HyperKvasir video text retrieval','gastrointestinal endoscopy video retrieval language','medical video text retrieval endoscopy','HyperKvasir keyframe retrieval']
def get(q):
 try:
  u='https://api.openalex.org/works?'+urllib.parse.urlencode({'search':q,'filter':'from_publication_date:2023-01-01,to_publication_date:2026-11-23','per-page':20});b=urllib.request.urlopen(u,timeout=30).read();(p/(re.sub(r'[^a-z]+','_',q.lower())[:35]+'.json')).write_bytes(b);print('\n',q, 'hits',json.loads(b)['meta']['count'])
  for x in json.loads(b)['results'][:12]:print(x['publication_year'],x['title'],x['doi'])
 except Exception as e:print(q,e)
import re
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,qs))
