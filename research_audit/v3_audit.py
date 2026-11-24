import urllib.request, urllib.parse, json, concurrent.futures, pathlib, re
OUT=pathlib.Path(r'C:\lunwen\research_audit\v3_new_topic')
OUT.mkdir(exist_ok=True)
URLS={
 'prostate_train':'https://zenodo.org/api/records/6481141',
 'prostate_test':'https://zenodo.org/api/records/6592345',
 'prostate_tree':'https://api.github.com/repos/kbressem/prostate158/git/trees/main?recursive=1',
 'prostate_issues':'https://api.github.com/repos/kbressem/prostate158/issues?state=all&per_page=100',
 'lesion_guided_crossref':'https://api.crossref.org/works?query.title='+urllib.parse.quote('Lesion-Guided Selective Multi-Modal Integration for Prostate Cancer Segmentation')+'&rows=3',
 'prostate_recent':'https://api.openalex.org/works?search=prostate158&filter=from_publication_date:2024-01-01&per-page=30',
 'isles_readme':'https://raw.githubusercontent.com/Tabrisrei/ISLES22/master/README.md',
}
def get(k,u):
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'ResearchAudit/1.0'})
  with urllib.request.urlopen(req,timeout=40) as r: raw=r.read()
  (OUT/(k+'.txt')).write_bytes(raw)
  d=json.loads(raw)
  if k.startswith('prostate_') and 'metadata' in d:
   return k,{'title':d['metadata']['title'],'description':d['metadata'].get('description'),'access':d['metadata'].get('access_right'),'license':d['metadata'].get('license'),'files':d.get('files')}
  if k=='prostate_recent': return k,[{'title':x['title'],'year':x['publication_year'],'doi':x['doi'],'cited':x['cited_by_count'],'url':x['primary_location']} for x in d['results']]
  if k=='lesion_guided_crossref': return k,[{'title':x.get('title'),'doi':x.get('DOI'),'published':x.get('published'),'abstract':x.get('abstract'),'link':x.get('link')} for x in d['message']['items']]
  if k=='prostate_tree':return k,[x['path'] for x in d['tree'] if x['type']=='blob']
  if k=='prostate_issues':return k,[{'number':x['number'],'title':x['title'],'body':x['body']} for x in d]
  return k,raw.decode()[:8000]
 except Exception as e:return k,{'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for k,result in ex.map(lambda p:get(*p),URLS.items()):
  print(k,json.dumps(result,ensure_ascii=False))
