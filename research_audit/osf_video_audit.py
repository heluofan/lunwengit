import urllib.request,json,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23');h={'Accept':'application/vnd.api+json','User-Agent':'Mozilla/5.0'}
for name,id in [('root','mh9sj:osfstorage'),('videos','5dfb57eaa95d73000939fc5b')]:
 u='https://api.osf.io/v2/nodes/mh9sj/files/osfstorage/'+(id.split(':')[1]+'/' if ':' in id else id+'/')
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers=h),timeout=30).read();d=json.loads(b);(p/f'osf_{name}.json').write_bytes(b);print(name,[(x['id'],x['attributes']['name'],x['attributes']['kind'],x['attributes'].get('size'),x['links'].get('download'),x['links'].get('info')) for x in d['data'][:50]])
 except Exception as e:print(name,e)
for u in ['https://api.github.com/repos/simula/hyper-kvasir','https://raw.githubusercontent.com/simula/hyper-kvasir/master/README.md','https://raw.githubusercontent.com/simula/hyper-kvasir/main/README.md']:
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read();print(u,b[:1600])
 except Exception as e:print(u,e)
