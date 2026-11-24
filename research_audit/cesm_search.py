import pathlib,urllib.request,urllib.parse,json,concurrent.futures,xml.etree.ElementTree as ET
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
queries={'cesm_recent':'CDD-CESM','cesm_benign':'contrast enhanced mammography benign malignant multimodal fusion','cesm_fusion':'cross-energy feature fusion contrast mammography'}
def get(kv):
 k,q=kv;u='https://api.openalex.org/works?'+urllib.parse.urlencode({'search':q,'filter':'from_publication_date:2024-01-01,to_publication_date:2026-11-22','per-page':50})
 try:
  b=urllib.request.urlopen(u,timeout=40).read();(p/(k+'.json')).write_bytes(b);d=json.loads(b)
  print('\nQUERY',q,'raw_count',d['meta']['count'])
  for a in d['results']:
   title=a['title']
   if any(w in title.lower() for w in ['mammogra','breast','cesm','cross-energy']):print(a['publication_year'],title,a['doi'],a['open_access']['oa_url'])
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,queries.items()))
root=ET.fromstring((p/'fusion_full.txt').read_bytes())
for node in root.findall('.//ref'):
 if node.attrib.get('id','').endswith('26'): print('REF26',' '.join(node.itertext()))
for node in root.findall('.//sec'):
 title=node.find('title')
 if title is not None and any(w in ''.join(title.itertext()).lower() for w in ['availability','preprocessing','network']):print('SECTION',' '.join(node.itertext())[:5000])
