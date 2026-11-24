import urllib.request,urllib.parse,pathlib,re,concurrent.futures,json
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23')
urls={'hyper_paper':'https://www.nature.com/articles/s41597-020-00622-y','hyper_http':'http://datasets.simula.no/hyper-kvasir/','hyper_osf':'https://osf.io/mh9sj/','hyper_data_zenodo':'https://api.openalex.org/works/https://doi.org/10.1038/s41597-020-00622-y'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=50).read();(p/(k+'.txt')).write_bytes(b);s=b.decode('utf-8','replace')
  if k=='hyper_paper':
   s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',s,flags=re.S);t=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s));(p/(k+'_clean.txt')).write_text(t,'utf-8');
   for term in ['Data Records','Data Availability','download','374 videos','license','Baidu','Google']:
    ids=[m.start() for m in re.finditer(re.escape(term),t,re.I)];print(k,term,[t[max(0,i-120):i+1100] for i in ids[:2]])
   print('links',re.findall(r'href=["\']([^"\']*(?:simula|github|zenodo|osf|drive)[^"\']*)',s)[:25])
  else: print(k,len(b),b[:100],re.sub('<[^>]+>',' ',s)[:1500])
 except Exception as e:print(k,type(e).__name__,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(get,urls.items()))
