import pathlib,json,re,collections
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22'); rows=json.loads((p/'sheet1.json').read_text('utf-8'))[1:];d=[{re.sub(r'\d+','',k):str(v).strip() for k,v in r} for r in rows];rank={'Normal':0,'Benign':1,'Malignant':2};g=collections.defaultdict(list)
for r in d:g[(r['B'],r['C'])].append(r)
a=[]
for (pat,side),rs in g.items():
 label=max((r['L'] for r in rs),key=lambda x:rank[x]); a.append({'patient_id':pat,'side':side,'label_aggregate':label,'label_set':sorted(set(r['L'] for r in rs)),'image_names':[r['A'] for r in rs]})
b=[r for r in a if r['label_aggregate']!='Normal'];print('sides',len(a),'counts',collections.Counter(r['label_aggregate'] for r in a),'BM patients',len(set(r['patient_id'] for r in b)),'BM sides',len(b),'conflicting sides',sum(len(r['label_set'])>1 for r in a));(p/'side_level_annotation_audit.json').write_text(json.dumps(a,ensure_ascii=False,indent=2),'utf-8')
for k in ['benign2025_bioc_clean','benign2026_bioc_clean']:
 t=(p/(k+'.txt')).read_text('utf-8')
 for section in ['2.1.','2.2.','patient-level','patient level','Table 14']:
  i=t.find(section)
  if i>=0:print(k,section,t[i:i+1500])
