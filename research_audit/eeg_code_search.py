import urllib.request,urllib.parse,json,concurrent.futures,pathlib
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
qs={'stecanet_repo':'STeCANet','efrm_repo':'EFRM EEG','epect_repo':'EPECT EEG','sta_repo':'STA-Net EEG fNIRS','mgf_repo':'MGFNet fNIRS'}
def get(kv):
 k,q=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request('https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':q,'per_page':6}),headers={'User-Agent':'ResearchAudit'}),timeout=30).read();(p/(k+'.json')).write_bytes(b);print(k,[(x['full_name'],x.get('description')) for x in json.loads(b).get('items',[])])
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,qs.items()))
