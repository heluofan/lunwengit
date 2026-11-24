from pathlib import Path
import urllib.request,concurrent.futures
p=Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22'); t=(p/'wave_full_clean.txt').read_text('utf-8')
for start,end in [('5.1.1 Discrimination','5.2 Modality'),('5.2 Modality','5.3 Stable'),('5.6 Comparison','6 Discussion')]:
 i=t.find(start,t.find('Abstract',2000)+8);i=t.find(start,i+1) if i<4000 and i>=0 else i;j=t.find(end,i+len(start));print('\nSECTION',start,t[i:j][:5800])
urls={'ieee_full_attempt':'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11356777','ieee_publisher':'https://ieeexplore.ieee.org/document/11356777/'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read();(p/(k+'.txt')).write_bytes(b);print(k,len(b),b[:70])
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(get,urls.items()))
