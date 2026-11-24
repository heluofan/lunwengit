import urllib.request,pathlib,concurrent.futures,re,urllib.parse,json
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
urls={'derm_site':'https://derm.cs.sfu.ca/','derm_recent':'https://api.openalex.org/works?'+urllib.parse.urlencode({'search':'clinical dermoscopic multimodal classification Derm7pt','filter':'from_publication_date:2024-01-01,to_publication_date:2026-11-22','per-page':15})}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();(p/(k+'.txt')).write_bytes(b)
  if k=='derm_site': print(k,re.sub('<[^>]+>',' ',b.decode('utf-8','replace'))[:8500]);print('LINKS',re.findall(r'href=["\']([^"\']+)',b.decode('utf-8','replace')))
  else:
   for x in json.loads(b)['results']:print(x['title'],x['doi'],x['open_access']['oa_url'])
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(get,urls.items()))
