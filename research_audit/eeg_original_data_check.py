from pathlib import Path
import urllib.request,urllib.parse,json,sys,re
from pypdf import PdfReader
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');q=p/'feasibility_recheck';t='\n'.join(x.extract_text() for x in PdfReader(q/'data_description.pdf').pages);(q/'data_description_clean.txt').write_text(t,'utf-8');print('DESCRIPTOR',t[:6500])
u='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.title':'Simultaneous acquisition of EEG and NIRS during cognitive tasks for an open access dataset','rows':2});b=urllib.request.urlopen(u,timeout=30).read();(q/'original_paper_crossref.json').write_bytes(b)
for x in json.loads(b)['message']['items']:print('ORIGINAL',x['title'],x['DOI'],x.get('link'))
sys.path.insert(0,str(p/'python_deps'));from scipy.io import loadmat
for mod in ['EEG','NIRS']:
 a=loadmat(p/'sample_subject001'/mod/'cnt_wg.mat',simplify_cells=True)['cnt_wg'];aa=a if mod=='EEG' else a['oxy'];print('MAT',mod,'metadata', {k:str(v)[:1300] for k,v in aa.items() if k not in ['x','time','clab']})
