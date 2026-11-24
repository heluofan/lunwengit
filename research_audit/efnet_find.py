import urllib.request,pathlib,re,concurrent.futures
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
urls={'efnet_pmc':'https://pmc.ncbi.nlm.nih.gov/articles/PMC10974548/','efnet_mdpi':'https://www.mdpi.com/1424-8220/24/6/1889','efnet_xml_ncbi':'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10974548/?report=xml'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read();(p/(k+'.txt')).write_bytes(b);s=b.decode('utf-8','replace');print(k,len(b),re.findall(r'href=["\']([^"\']*(?:github|bbci|figshare|zenodo)[^"\']*)',s))
 except Exception as e:print(k,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(get,urls.items()))
t=(p/'efnet_clean.txt').read_text('utf-8')
for start,end in [('3.1.','3.2.'),('4.1.','4.2.'),('6. Limitations','7. Conclusions')]:
 i=t.find(start);j=t.find(end,i+len(start));print('EFNET',start,t[i:j][:6200])
