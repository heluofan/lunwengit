from pathlib import Path
import json,subprocess,concurrent.futures
root=Path(r'C:\lunwen\research_audit\corpus_2025_2026')
out=root/'visual_checks';out.mkdir(exist_ok=True)
rows={int(x['id']):x for x in json.loads((root/'manifest.json').read_text('utf-8'))}
pop=r'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
tasks=[(25,5),(81,5),(53,8),(78,4),(39,6),(93,1),(93,10),(100,12)]
def render(task):
 i,p=task;prefix=out/f'{i:03d}_p{p}'
 r=subprocess.run([pop,'-f',str(p),'-l',str(p),'-scale-to','1600','-png','-singlefile',rows[i]['file'],str(prefix)],capture_output=True)
 return str(prefix)+'.png',r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(render,tasks):print(result)
