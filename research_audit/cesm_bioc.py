import urllib.request,concurrent.futures,pathlib,xml.etree.ElementTree as ET,re
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
urls={'benign2025_bioc':'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC12383514/ascii','benign2026_bioc':'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC12938819/ascii'}
def get(kv):
 k,u=kv
 try:
  b=urllib.request.urlopen(u,timeout=40).read(); (p/(k+'.xml')).write_bytes(b);root=ET.fromstring(b);t='\n'.join(''.join(x.itertext()) for x in root.findall('.//passage/text'));(p/(k+'_clean.txt')).write_text(t,'utf-8')
  print(k,'length',len(t))
  for w in ['github','data availability','patient','random','CESM dataset','CESM Dataset','CM images','source code']:
   starts=[m.start() for m in re.finditer(re.escape(w),t,re.I)];print(w,[t[max(0,i-150):i+850] for i in starts[:2]])
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(get,urls.items()))
