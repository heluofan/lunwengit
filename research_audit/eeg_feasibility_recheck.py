from pathlib import Path
import urllib.request,urllib.parse,json,concurrent.futures,re,ssl
p=Path(r'C:\lunwen\research_audit\new_direction_20261122\feasibility_recheck');p.mkdir(exist_ok=True)
ctx=ssl.create_default_context()
for store in ['ROOT','CA']:
 for cert,enc,trust in ssl.enum_certificates(store):
  if enc=='x509_asn':
   try:ctx.load_verify_locations(cadata=ssl.DER_cert_to_PEM_cert(cert))
   except ssl.SSLError:pass
urls={'data_description':'https://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/Dataset%20description_MATLAB.pdf','original_paper':'https://www.nature.com/articles/sdata2018003','dataset_record':'https://api.datacite.org/dois/10.14279/depositonce-5830','bistf_github':'https://api.github.com/repos/zc701/BiSTF-Net','steca_search':'https://api.openalex.org/works?'+urllib.parse.urlencode({'search':'"STeCANet"','per-page':10})}
def get(kv):
 k,u=kv
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),context=ctx,timeout=35);b=r.read();(p/(k+('.pdf' if b.startswith(b'%PDF') else '.txt'))).write_bytes(b)
  if k=='original_paper':
   s=b.decode('utf-8','replace');s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',s,flags=re.S);t=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s));(p/'original_paper_clean.txt').write_text(t,'utf-8');
   for w in ['filter','200 Hz','Data Records','Usage Notes']:
    ids=[m.start() for m in re.finditer(re.escape(w),t,re.I)];print(k,w,[t[max(0,i-120):i+1200] for i in ids[:3]])
  elif k=='dataset_record':
   a=json.loads(b)['data']['attributes'];print(k,'rights',a.get('rightsList'),'URL',a.get('url'))
  elif k=='bistf_github':
   a=json.loads(b);print(k,'stars',a.get('stargazers_count'),'issues',a.get('open_issues_count'),'pushed',a.get('pushed_at'),'license',a.get('license'))
  elif k=='steca_search':
   for a in json.loads(b)['results']:print(k,a['title'],a['open_access'],[(x.get('landing_page_url'),x.get('pdf_url')) for x in a['locations']])
  else:print(k,len(b))
 except Exception as e:print(k,type(e).__name__,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(get,urls.items()))
