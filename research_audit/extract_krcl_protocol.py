from pathlib import Path
import re
p=Path(r'C:\lunwen\research_audit\corpus_2025_2026\045.txt');t=p.read_text('utf-8',errors='replace')
for term in ['Hyper-Kvasir数据集','数据集的划分','训练集','70%','video-labels.csv','R@1','KRCL-IT','核心集','帧采样']:
 ids=[m.start() for m in re.finditer(term,t,re.I)]; print('\n',term,len(ids))
 for i in ids[:2]:print(t[max(0,i-120):i+1650].replace('\n',' '))
