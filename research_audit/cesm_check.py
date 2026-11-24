import pathlib,urllib.request,re,concurrent.futures,json,zipfile,xml.etree.ElementTree as ET
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22')
z=zipfile.ZipFile(p/'annotations.xlsx'); ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
ss=ET.fromstring(z.read('xl/sharedStrings.xml')); strings=[''.join(x.itertext()) for x in ss]
print('WORKBOOK',z.read('xl/workbook.xml').decode()[:1800])
for f in z.namelist():
 if re.match(r'xl/worksheets/sheet\d+.xml$',f):
  root=ET.fromstring(z.read(f)); rows=[]
  for row in root.findall('.//m:sheetData/m:row',ns):
   vals=[]
   for c in row:
    v=c.find('m:v',ns); vals.append((c.attrib.get('r'),strings[int(v.text)] if v is not None and c.attrib.get('t')=='s' else v.text if v is not None else ''))
   rows.append(vals)
  (p/(pathlib.Path(f).stem+'.json')).write_text(json.dumps(rows,ensure_ascii=False),'utf-8')
  print(f,len(rows),'FIRST',rows[:7])
links=re.findall(r'href=["\']([^"\']+)',(p/'tcia.txt').read_text('utf-8'))
a=next(x for x in links if 'faspex/public/package' in x)
urls={'aspera':a,'crad_openalex':'https://api.openalex.org/works/https://doi.org/10.1016/j.crad.2026.107276','jimaging_openalex':'https://api.openalex.org/works/https://doi.org/10.3390/jimaging12010041','cesm_repo':'https://codeload.github.com/omar-mohamed/CDD-CESM-Dataset/zip/refs/heads/main','europepmc':'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.3390/jimaging12010041&format=json'}
def get(kv):
 k,u=kv
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45); b=r.read(); (p/(k+('.zip' if k=='cesm_repo' else '.txt'))).write_bytes(b)
  print(k,len(b),b.decode('utf-8','replace')[:7000] if k.endswith('openalex') or k=='europepmc' else b[:100])
 except Exception as e:print(k,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(get,urls.items()))
