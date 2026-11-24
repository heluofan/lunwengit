import urllib.request,pathlib,json,concurrent.futures,urllib.parse
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
urls={'prostate_readme':'https://raw.githubusercontent.com/kbressem/prostate158/main/README.md','prostate_train':'https://raw.githubusercontent.com/kbressem/prostate158/main/prostate158/train.py','prostate_train_data':'https://zenodo.org/api/records/6481141','prostate_test_data':'https://zenodo.org/api/records/6592345','lesmi_meta':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':'DOI:10.1002/mp.70019','format':'json','resultType':'core'})}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=40).read();(p/(k+'.txt')).write_bytes(b)
  if k.endswith('data'):
   d=json.loads(b);print(k,'access',d['metadata'].get('access_right'),'license',d['metadata'].get('license'),'files',[(x['key'],x['size'],x['links']) for x in d['files']])
  elif k=='lesmi_meta':
   for r in json.loads(b)['resultList']['result']:print(k,r.get('pmcid'),r.get('title'),r.get('abstractText'),r.get('fullTextUrlList'))
  else:print(k,b.decode('utf-8','replace')[:6500])
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(get,urls.items()))
