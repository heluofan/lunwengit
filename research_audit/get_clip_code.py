import urllib.request,pathlib,zipfile,json
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23')
for name,url in [('clip4clip','https://codeload.github.com/ArrowLuo/CLIP4Clip/zip/refs/heads/master'),('hyper_official_code','https://codeload.github.com/simula/hyper-kvasir/zip/refs/heads/master')]:
 try:
  b=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read();(p/(name+'.zip')).write_bytes(b);z=zipfile.ZipFile(p/(name+'.zip'));print(name,len(b),len(z.namelist()),z.namelist()[:60]);z.extractall(p/(name+'_src'))
 except Exception as e:print(name,type(e).__name__,str(e))
