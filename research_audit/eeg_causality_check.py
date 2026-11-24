from pathlib import Path
import urllib.request,re,concurrent.futures,sys,json
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');q=p/'feasibility_recheck'
urls={'original_full':'https://www.nature.com/articles/sdata20183','mne_filter_doc':'https://mne.tools/stable/generated/mne.filter.filter_data.html','steca_pubmed':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:41360009&format=json&resultType=core'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(q/(k+'.html')).write_bytes(b)
  if k=='steca_pubmed':
   for x in json.loads(b)['resultList']['result']:print(k,x.get('firstPublicationDate'),x.get('abstractText'))
  else:
   s=b.decode('utf-8','replace');s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',s,flags=re.S);t=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s));(q/(k+'_clean.txt')).write_text(t,'utf-8')
   terms=['filter','200 Hz','WG task','zero-phase','filtfilt','data is licensed'] if k=='original_full' else ['phase','filtfilt','forward']
   for w in terms:
    ids=[m.start() for m in re.finditer(re.escape(w),t,re.I)];print(k,w,[t[max(0,i-150):i+1100] for i in ids[:3]])
 except Exception as e:print(k,type(e).__name__,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,urls.items()))
