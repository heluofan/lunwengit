import pathlib,urllib.request,json,concurrent.futures,urllib.parse,re
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
urls={'wave_html':'https://arxiv.org/html/2607.02394','wave_pdf':'https://arxiv.org/pdf/2607.02394','ieee_crossref':'https://api.crossref.org/works/10.1109/BIBM66473.2025.11356777','ieee_openalex':'https://api.openalex.org/works/https://doi.org/10.1109/BIBM66473.2025.11356777'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(p/(k+('.pdf' if k.endswith('pdf') else '.txt'))).write_bytes(b)
  if k=='ieee_crossref':
   d=json.loads(b)['message'];print(k,d.get('title'),d.get('abstract'),d.get('link'))
  elif k=='ieee_openalex':
   d=json.loads(b);ai=d.get('abstract_inverted_index') or {};w={i:k for k,l in ai.items() for i in l};print(k,' '.join(w[i] for i in sorted(w)),[(l.get('landing_page_url'),l.get('pdf_url')) for l in d.get('locations',[])])
  else:print(k,len(b),b[:70])
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:list(e.map(get,urls.items()))
