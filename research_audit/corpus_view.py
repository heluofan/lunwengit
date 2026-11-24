from pathlib import Path
import sys,re,unicodedata
root=Path(r'C:\lunwen\research_audit\corpus_2025_2026')
files=sorted(Path(r'C:\Users\Administrator\Downloads\lunwen').rglob('*.pdf'),key=lambda p:p.name)
mode=sys.argv[1]
for n in sys.argv[2:]:
 p=root/f'{int(n):03d}.txt'
 if not p.exists():continue
 t=unicodedata.normalize('NFKC',p.read_text(encoding='utf-8'))
 print('\n###',n,files[int(n)-1].name)
 if mode=='full': print(t);continue
 if mode=='head':print(t[:1800]);continue
 if mode in ('compact','overview'):
  print('FRONT:',re.sub(r'\s+',' ',t[:220]))
  a=re.search(r'摘\s*要\s*[：:]?',t)
  if a: print('ABS:',re.sub(r'\s+',' ',t[a.end():a.end()+(580 if mode=='compact' else 420)]))
  if mode=='overview':
   print('FOOT:',re.sub(r'\s+',' ',t[:5000][-350:]));continue
  ms=list(re.finditer(r'\n[^\n]{0,20}(?:数据集|研究对象|一般资料|实验数据|试验数据|临床资料|患者资料)[^\n]{0,20}\n',t[2500:]))
  if ms:
   start=ms[0].start()+2500
   print('DATA:',re.sub(r'\s+',' ',t[start:start+750]))
  cs=list(re.finditer(r'\n[^\n]{0,12}(?:结\s*论|结束语|局限性)[^\n]{0,10}\n',t))
  if cs: print('END:',re.sub(r'\s+',' ',t[cs[-1].start():cs[-1].start()+350]))
  continue
 # Read front matter, abstract, first data/protocol section and ending discussion.
 print('FRONT:',re.sub(r'\s+',' ',t[:500]))
 a=re.search(r'摘\s*要\s*[：:]?',t)
 if a:print('ABSTRACT:',re.sub(r'\s+',' ',t[a.end():a.end()+700]))
 body=t[3500:]
 if mode=='brief':
  pat=r'(?:数据集|数据来源|研究对象|一般资料|实验数据|试验数据|临床资料|患者资料)'
  matches=list(re.finditer(pat,body))
  for m in matches[:2]:print('DATA:',re.sub(r'\s+',' ',body[max(0,m.start()-80):m.start()+550]))
  cs=list(re.finditer(r'(?:\n\s*[4567]?\s*[.．、]?\s*(?:结\s*论|结束语)|本研究的局限|局限性|不足之处)',t))
  if cs:print('ENDING:',re.sub(r'\s+',' ',t[cs[-1].start():cs[-1].start()+650]))
 if mode=='data':
  pat=r'(?:数据集|数据来源|研究对象|一般资料|实验数据|试验数据|临床资料|患者资料|消融实验|单模态|单一模态|局限性|不足之处)'
  for m in list(re.finditer(pat,body))[:16]:print('p'+str(t[:3500+m.start()].count('=== PDF_PAGE'))+':',re.sub(r'\s+',' ',body[max(0,m.start()-100):m.start()+650]))
