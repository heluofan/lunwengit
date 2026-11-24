import urllib.request,urllib.parse,json,concurrent.futures,pathlib,re
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
urls={'hypo_github':'https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':'hypotension frequency','per_page':20}),'fd_openalex':'https://api.openalex.org/works/https://doi.org/10.1109/jbhi.2024.3403109','hypobrid_full':'https://pmc.ncbi.nlm.nih.gov/articles/PMC13340010/','vital_api':'https://api.vitaldb.net/cases','vital_trks':'https://api.vitaldb.net/trks','vital_readme':'https://raw.githubusercontent.com/vitaldb/vitaldb-python/master/README.md'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read();(p/(k+'.txt')).write_bytes(b)
  if k=='hypo_github':print(k,[(x['full_name'],x.get('description')) for x in json.loads(b).get('items',[])])
  elif k=='fd_openalex':
   d=json.loads(b);print(k,[(x.get('landing_page_url'),x.get('pdf_url')) for x in d['locations']],[(x['author']['display_name']) for x in d['authorships']])
  elif k=='hypobrid_full':
   s=b.decode('utf-8');print(k,re.findall(r'href=["\']([^"\']*(?:github|figshare|zenodo)[^"\']*)',s));s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',s,flags=re.S);t=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s));(p/'hypobrid_clean.txt').write_text(t,'utf-8');i=t.find('Data availability');print(t[i:i+1500])
  else:print(k,len(b),b[:1300])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:list(ex.map(get,urls.items()))
