from pathlib import Path
import urllib.request,concurrent.futures,re,xml.etree.ElementTree as ET
p=Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'bistf':'PMC12938437','mgf_full':'PMC13259229','mbc_full':'PMC12504385'}
def get(kv):
 k,pmc=kv
 try:
  b=urllib.request.urlopen(f'https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/',timeout=35).read();(p/(k+'.html')).write_bytes(b);s=b.decode('utf-8','replace');print(k,'LINKS',re.findall(r'href=["\']([^"\']*(?:github|zenodo|figshare)[^"\']*)',s))
  s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',s,flags=re.S);t=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s));(p/(k+'_clean.txt')).write_text(t,'utf-8')
  for w in ['subject-independent','leave-one','Data Availability','cross-validation','Limitations','limitation']:
   ids=[m.start() for m in re.finditer(re.escape(w),t,re.I)];print(k,w,[t[max(0,i-100):i+950] for i in ids[:2]])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,qs.items()))
from scipy.io import loadmat
for mod in ['EEG','NIRS']:
 a=loadmat(p/'sample_subject001'/mod/'cnt_wg.mat',simplify_cells=True)['cnt_wg'];m=loadmat(p/'sample_subject001'/mod/'mrk_wg.mat',simplify_cells=True)['mrk_wg'];print('SAMPLE',mod,'keys',a.keys(),'fs',a.get('fs'),'labels',m['y'].shape,'times',m['time'][:4])
 if mod=='EEG':print('EEG shape',a['x'].shape)
 else:print('NIRS oxy',a['oxy']['x'].shape,'deoxy',a['deoxy']['x'].shape)
