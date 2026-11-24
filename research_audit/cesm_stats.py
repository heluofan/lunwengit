import json,pathlib,collections,re,zipfile
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22');rows=json.loads((p/'sheet1.json').read_text('utf-8'))[1:];d=[{re.sub(r'\d+','',k):str(v).strip() for k,v in r} for r in rows]
print('rows',len(d),'patients',len(set(x['B'] for x in d)),'labels',collections.Counter(x['L'] for x in d))
g=collections.defaultdict(list)
for x in d:g[(x['B'],x['C'],x['I'])].append(x)
print('same-view groups',len(g),'complete modalities',sum(set(x['D'] for x in v)=={'DM','CESM'} for v in g.values()),'label_conflicts',[(k,[(x['A'],x['L']) for x in v]) for k,v in g.items() if len(set(x['L'] for x in v))>1][:10])
s=collections.defaultdict(list)
for x in d:s[(x['B'],x['C'])].append(x)
full=[v for v in s.values() if {(x['D'],x['I']) for x in v}=={('DM','CC'),('DM','MLO'),('CESM','CC'),('CESM','MLO')}]
print('sides',len(s),'4image sides',len(full),'4image side label set',collections.Counter('/'.join(sorted(set(x['L'] for x in v))) for v in full))
for name in ['crad_openalex','jimaging_openalex']:
 a=json.loads((p/(name+'.txt')).read_text()); ai=a.get('abstract_inverted_index'); txt=''
 if ai:
  seq={n:w for w,ns in ai.items() for n in ns};txt=' '.join(seq[i] for i in sorted(seq))
 print(name,'ABSTRACT',txt,'LOCATIONS',[(x.get('landing_page_url'),x.get('pdf_url')) for x in a['locations']])
if (p/'europepmc.txt').exists():print('PMC',json.loads((p/'europepmc.txt').read_text()).get('resultList'))
if (p/'cesm_repo.zip').exists():
 z=zipfile.ZipFile(p/'cesm_repo.zip');print('CODE',z.namelist()[:30]);z.extractall(p/'author_code')
if (p/'aspera.txt').exists():
 a=(p/'aspera.txt').read_text('utf-8'); print('ASPERA',len(a));print(re.sub('<[^>]+>',' ',a)[:2500]); print('scripts',re.findall(r'<script[^>]+src=["\']([^"\']+)',a))
