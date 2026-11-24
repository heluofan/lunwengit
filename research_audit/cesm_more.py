import json,pathlib,urllib.request,urllib.parse,concurrent.futures
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
a=json.loads((p/'cesm_recent.json').read_text())
print('CDD recent relevant title list:')
for x in a['results']:
 if any(w in x['title'].lower() for w in ['mammogra','breast','cesm']):print(x['publication_year'],x['title'],x['doi'])
urls={'kaggle_search':'https://www.kaggle.com/api/v1/datasets/list?search=cdd-cesm','cbm_meta':'https://api.crossref.org/works/10.1016/j.compbiomed.2024.109266','benign2026_meta':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.3390/bioengineering13020206&format=json&resultType=core','benign2025_meta':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.3390/bioengineering12080885&format=json&resultType=core'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(p/(k+'.json')).write_bytes(b);d=json.loads(b)
  if k=='kaggle_search':print(k,[(x.get('ref'),x.get('totalBytes'),x.get('licenseName')) for x in d])
  elif k=='cbm_meta':print(k,d['message'].get('abstract'),d['message'].get('link'),d['message'].get('author'))
  else:
   for r in d.get('resultList',{}).get('result',[]):print(k,r.get('pmcid'),r.get('title'),r.get('abstractText'))
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,urls.items()))
