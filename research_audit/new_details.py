import urllib.request,urllib.parse,json,concurrent.futures,pathlib,re
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'hybrid_dataset':'https://www.nature.com/articles/s41597-026-07807-x','efnet':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode({'query':'DOI:10.3390/s24061889','format':'json','resultType':'core'}),'dmsl':'https://repository.essex.ac.uk/42759/1/DMSL2026.pdf','oral_full':'https://www.nature.com/articles/s41598-026-52410-0','eeg_recent':'https://api.openalex.org/works?'+urllib.parse.urlencode({'search':'EEG fNIRS motor imagery fusion github','filter':'from_publication_date:2024-01-01,to_publication_date:2026-11-22','per-page':15})}
def run(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read();(p/(k+('.pdf' if k=='dmsl' else '.txt'))).write_bytes(b)
  if k=='efnet':
   for a in json.loads(b)['resultList']['result']:print(k,a.get('pmcid'),a.get('abstractText'))
  elif k=='eeg_recent':
   for a in json.loads(b)['results']:print(k,a['title'],a['doi'])
  elif k=='dmsl':print(k,len(b))
  else:
   t=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',b.decode('utf-8','replace')));(p/(k+'_clean.txt')).write_text(t,'utf-8')
   for w in ['Abstract','Data availability','Code availability','subjects','participants','figshare','github']:
    i=t.find(w);print(k,w,t[max(0,i-80):i+1800] if i>=0 else 'not found')
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(run,qs.items()))
