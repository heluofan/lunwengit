import re,sys,unicodedata,json
from pathlib import Path
root=Path(r'C:\lunwen\research_audit\corpus_2025_2026')
ids=sys.argv[1].split(',');pattern=sys.argv[2];width=int(sys.argv[3]) if len(sys.argv)>3 else 500
for i in ids:
 t=unicodedata.normalize('NFKC',(root/f'{int(i):03d}.txt').read_text('utf-8'))
 print('\n###',i)
 pos=[]
 for m in re.finditer(pattern,t):
  if any(abs(m.start()-x)<width for x in pos):continue
  if re.search(r'参考文献|References',t[max(0,m.start()-1000):m.start()]):continue
  pos.append(m.start())
  print('PDFp',t[:m.start()].count('=== PDF_PAGE'),':',re.sub(r'\s+',' ',t[max(0,m.start()-100):m.start()+width]))
  if len(pos)>=5:break
