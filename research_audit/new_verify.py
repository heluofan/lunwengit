from pathlib import Path
import re,urllib.request,json,concurrent.futures,xml.etree.ElementTree as ET
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');print((p/'oral_repo.txt').read_text('utf-8'))
s=(p/'hybrid_dataset.txt').read_text('utf-8');s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',s,flags=re.S);t=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s))
print('MIND data',[(m.start(),t[m.start()-200:m.start()+1000]) for m in re.finditer('figshare|Data records|Data Records|Data Availability',t,re.I)][:8]);print('links',re.findall(r'href=["\']([^"\']*(?:figshare|zenodo|github|10.6084)[^"\']*)',s))
urls={'efnet_bioc':'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC10974548/ascii','oral_data':'https://zenodo.org/api/records/10664056','mind_repo':'https://raw.githubusercontent.com/useflf/Multimodal-fNIRS-EEG-Dataset/main/README.md'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=30).read();(p/(k+'.txt')).write_bytes(b)
  if k=='efnet_bioc':
   root=ET.fromstring(b);t='\n'.join(''.join(x.itertext()) for x in root.findall('.//passage/text'));(p/'efnet_clean.txt').write_text(t,'utf-8')
   for w in ['github','Data Availability','29','26','Dataset','Limitations']:
    inds=[m.start() for m in re.finditer(re.escape(w),t,re.I)];print(k,w,[t[max(0,i-100):i+1100] for i in inds[:2]])
  elif k=='oral_data':
   d=json.loads(b);print(k,d['metadata'].get('title'),d['metadata'].get('description'),[(f['key'],f['size']) for f in d['files']])
  else:print(k,b.decode('utf-8','replace')[:6500])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,urls.items()))
