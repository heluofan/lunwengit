import urllib.request,pathlib,csv,io
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23')
u='https://osf.io/download/5f3g2/'
try:
 b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read();(p/'video-labels.csv').write_bytes(b);print('bytes',len(b),b[:300]);rows=list(csv.DictReader(io.StringIO(b.decode('utf-8-sig'))));print('rows',len(rows),'fields',list(rows[0]) if rows else None,'sample',rows[:4])
except Exception as e:print(type(e).__name__,e)
