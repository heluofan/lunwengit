import urllib.request,json,csv,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23');h={'Accept':'application/vnd.api+json','User-Agent':'Mozilla/5.0'}
labels=list(csv.DictReader((p/'video-labels.csv').open(encoding='utf-8-sig'))); target={r['Video file']:r for r in labels}
for nm,id in [('lower_path','5ea8004476188b01cd912015'),('lower_interv','5ea7fff976188b01c89102cc')]:
 u=f'https://api.osf.io/v2/nodes/mh9sj/files/osfstorage/{id}/?page%5Bsize%5D=100'
 try:
  d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=h),timeout=30).read());matches=[]
  for x in d['data']:
   a=x['attributes']; stem=a['name'].removesuffix('.avi')
   if stem in target and any(w in target[stem]['Finding 1'].lower() for w in ['polyp']):matches.append({'uuid':stem,'filename':a['name'],'size':a.get('size'),'download':x['links'].get('download'),'label':target[stem]})
  print(nm,'files',len(d['data']),'polyps matches',len(matches),'smallest',sorted(matches,key=lambda x:x['size'] or 0)[:3])
  (p/f'{nm}_manifest.json').write_text(json.dumps(matches,indent=2),'utf-8')
 except Exception as e:print(e)
