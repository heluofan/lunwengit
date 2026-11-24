import urllib.request,json,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23')
for u in ['https://api.osf.io/v2/nodes/mh9sj/files/','https://api.osf.io/v2/nodes/mh9sj/files/osfstorage/','https://api.osf.io/v2/files/']:
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'Accept':'application/vnd.api+json','User-Agent':'Mozilla/5.0'}),timeout=25).read(); print(u,len(b),b[:3000])
 except Exception as e:print(u,type(e).__name__,e)
