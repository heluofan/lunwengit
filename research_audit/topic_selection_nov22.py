import urllib.request,urllib.parse,json,re,pathlib,html,concurrent.futures
OUT=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22');OUT.mkdir(exist_ok=True)
def fetch(name,url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 ResearchAudit'})
  with urllib.request.urlopen(req,timeout=40) as r:b=r.read()
  (OUT/(name+'.txt')).write_bytes(b)
  s=b.decode('utf-8','replace')
  if name in ['tcia','cesm_paper','fusion_paper']:
   clean=html.unescape(re.sub('<[^>]+>',' ',re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',s,flags=re.S)))
   clean=re.sub(r'\s+',' ',clean)
   (OUT/(name+'_clean.txt')).write_text(clean,'utf-8')
   links=re.findall(r'href=["\']([^"\']+)["\']',s)
   print(name,'LINKS',json.dumps([x for x in links if re.search(r'\.zip|\.csv|\.xlsx|figshare|doi.org|github|download',x,re.I)],ensure_ascii=False)[:12000])
   for word in ['Data Availability','Availability of Data','Code Availability','Download','326','1,003','1003','License','GitHub','github','patient-grouped']:
    i=clean.find(word)
    if i>=0:print(name,word,clean[max(0,i-200):i+1200])
  else:print(name,s[:7000])
 except Exception as e:print(name,'ERROR',str(e))
urls={
 'tcia':'https://www.cancerimagingarchive.net/collection/cdd-cesm/',
 'cesm_paper':'https://www.nature.com/articles/s41597-022-01238-0',
 'fusion_paper':'https://www.mdpi.com/2313-433X/12/1/41',
 'derm_readme':'https://raw.githubusercontent.com/jeremykawahara/derm7pt/master/README.md',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(lambda x:fetch(*x),urls.items()))
