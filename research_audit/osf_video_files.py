import urllib.request,json,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23');h={'Accept':'application/vnd.api+json','User-Agent':'Mozilla/5.0'}
for name,id in [('upper','5ea7fe97e4f0810197075eba'),('lower','5ea7feabe4f08101980763aa')]:
 u=f'https://api.osf.io/v2/nodes/mh9sj/files/osfstorage/{id}/';
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers=h),timeout=30).read();d=json.loads(b);(p/f'osf_{name}.json').write_bytes(b);print(name,[(x['id'],x['attributes']['name'],x['attributes']['kind'],x['attributes'].get('size'),x['links'].get('download')) for x in d['data'][:80]])
 except Exception as e:print(name,e)
