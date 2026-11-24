from pathlib import Path
import hashlib,json,re,concurrent.futures
from pypdf import PdfReader
ROOT=Path(r'C:\Users\Administrator\Downloads\lunwen')
OUT=Path(r'C:\lunwen\research_audit\corpus_2025_2026')
OUT.mkdir(exist_ok=True)
def read(arg):
 i,p=arg
 raw=p.read_bytes()
 h=hashlib.sha256(raw).hexdigest()
 try:
  r=PdfReader(p)
  pages=[x.extract_text(extraction_mode='plain') or '' for x in r.pages]
  txt='\n\n'.join(f'=== PDF_PAGE {n+1} ===\n{t}' for n,t in enumerate(pages))
  fp=OUT/f'{i:03d}.txt';fp.write_text(txt,encoding='utf-8')
  return {'id':f'{i:03d}','file':str(p),'sha256':h,'pages':len(pages),'chars':len(txt),'text':str(fp),'head':pages[0][:550],'page_chars':[len(x) for x in pages]}
 except Exception as e:return {'id':f'{i:03d}','file':str(p),'sha256':h,'error':str(e)}
files=sorted(ROOT.rglob('*.pdf'),key=lambda p:p.name)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(read,enumerate(files,1)))
seen={}
for x in rows:
 if x['sha256'] in seen:x['duplicate_of']=seen[x['sha256']]
 else:seen[x['sha256']]=x['id']
(OUT/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for x in rows: print(x['id'],x.get('pages'),x.get('chars'),('DUP '+x['duplicate_of']) if x.get('duplicate_of') else '',Path(x['file']).name)
print('TOTAL',len(rows),'UNIQUE_HASH',len(seen),'PAGES',sum(x.get('pages',0) for x in rows))
