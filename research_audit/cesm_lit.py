import urllib.request,concurrent.futures,pathlib,xml.etree.ElementTree as ET,re,json
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
urls={'fusion_full':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12842785/fullTextXML','crad_abstract':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:41740222&format=json&resultType=core'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=40).read();(p/(k+'.txt')).write_bytes(b)
  if k=='fusion_full':
   root=ET.fromstring(b); t=' '.join(root.itertext());(p/'fusion_full_clean.txt').write_text(t,'utf-8')
   for sec in root.findall('.//sec'):
    title=sec.find('title')
    if title is not None and any(w in ''.join(title.itertext()).lower() for w in ['data','limitation','implementation','availability']):print(k,' '.join(sec.itertext())[:5000])
   print('LINKS',re.findall(r'https?[^\s<>"\]]+',t)[-30:])
  else:
   r=json.loads(b)['resultList']['result'][0];print(k,r.get('abstractText',''),r.get('fullTextUrlList',''))
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(get,urls.items()))
