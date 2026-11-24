import urllib.request,json, pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23');h={'Accept':'application/vnd.api+json','User-Agent':'Mozilla/5.0'}
for rootname,rootid in [('upper','5ea7fe97e4f0810197075eba'),('lower','5ea7feabe4f08101980763aa')]:
 u=f'https://api.osf.io/v2/nodes/mh9sj/files/osfstorage/{rootid}/';d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=h),timeout=30).read());
 for cat in d['data']:
  uid=cat['id'];u=f'https://api.osf.io/v2/nodes/mh9sj/files/osfstorage/{uid}/';dd=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=h),timeout=30).read());print(rootname,cat['attributes']['name'],[(x['id'],x['attributes']['name'],x['attributes']['kind'],x['attributes'].get('size'),x.get('links',{}).get('download')) for x in dd['data'][:6]])
