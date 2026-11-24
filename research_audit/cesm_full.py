import urllib.request,urllib.parse,pathlib,concurrent.futures,json,xml.etree.ElementTree as ET,re
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
urls={'cbm_pubmed':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':'DOI:10.1016/j.compbiomed.2024.109266','format':'json','resultType':'core'}),'benign2026_full':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12938819/fullTextXML','benign2025_full':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12383514/fullTextXML','wave_meta':'https://api.openalex.org/works/https://doi.org/10.48550/arxiv.2607.02394'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=40).read();(p/(k+'.txt')).write_bytes(b)
  if k.endswith('full'):
   root=ET.fromstring(b);t=' '.join(root.itertext());(p/(k+'_clean.txt')).write_text(t,'utf-8')
   for w in ['github','Data Availability','patient','CESM dataset','CESM Dataset']:
    starts=[m.start() for m in re.finditer(re.escape(w),t,re.I)]; print(k,w,[t[max(0,i-160):i+1100] for i in starts[:3]])
  elif k=='cbm_pubmed':
   for x in json.loads(b)['resultList']['result']:print(k,x.get('abstractText'),x.get('fullTextUrlList'))
  else:
   d=json.loads(b);ai=d.get('abstract_inverted_index');seq={i:w for w,l in (ai or {}).items() for i in l};print(k,' '.join(seq[i] for i in sorted(seq)),d.get('locations'))
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,urls.items()))
