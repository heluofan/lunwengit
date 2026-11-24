from pathlib import Path
import re,urllib.request,concurrent.futures,json
from pypdf import PdfReader
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');s=(p/'oral_full.txt').read_text('utf-8');s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',s,flags=re.S);t=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s));(p/'oral_clean.txt').write_text(t,'utf-8')
for w in ['dataset','Zenodo','patients','patient','clinical variables','metadata','36.']:
 inds=[m.start() for m in re.finditer(re.escape(w),t,re.I)];print('ORAL',w,[t[max(0,i-100):i+950] for i in inds[:3]])
print('ORAL LINKS',re.findall(r'href=["\']([^"\']*(?:zenodo|github)[^"\']*)',s))
t='\n'.join(pg.extract_text() for pg in PdfReader(p/'dmsl.pdf').pages);(p/'dmsl_clean.txt').write_text(t,'utf-8')
for w in ['github','dataset','subject-independent','29','code','delay']:
 inds=[m.start() for m in re.finditer(re.escape(w),t,re.I)];print('DMSL',w,[t[max(0,i-100):i+700] for i in inds[:2]])
urls={'oral_repo':'https://raw.githubusercontent.com/pormen/OCA_Embedding_Fusion/main/README.md','efnet_full':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10974548/fullTextXML'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=30).read();(p/(k+'.txt')).write_bytes(b);print(k,len(b),b[:400] if k=='oral_repo' else '')
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(get,urls.items()))
