import ssl,urllib.request,pathlib,io,zipfile,json,re
p=pathlib.Path(r'C:\lunwen\research_audit\new_direction_20261122')
ctx=ssl.create_default_context()
for store in ['ROOT','CA']:
 for cert,enc,trust in ssl.enum_certificates(store):
  if enc=='x509_asn':
   try:ctx.load_verify_locations(cadata=ssl.DER_cert_to_PEM_cert(cert))
   except ssl.SSLError:pass
class RemoteFile(io.RawIOBase):
 def __init__(self,url):
  self.url=url;self.pos=0;r=urllib.request.urlopen(urllib.request.Request(url,method='HEAD'),context=ctx,timeout=40);self.size=int(r.headers['Content-Length']);self.n=0
 def seekable(self):return True
 def readable(self):return True
 def seek(self,o,w=0):self.pos=o if w==0 else self.pos+o if w==1 else self.size+o;return self.pos
 def tell(self):return self.pos
 def read(self,n=-1):
  if n<0:n=self.size-self.pos
  if n==0:return b''
  req=urllib.request.Request(self.url,headers={'Range':f'bytes={self.pos}-{min(self.pos+n-1,self.size-1)}'})
  r=urllib.request.urlopen(req,context=ctx,timeout=50)
  if r.status!=206:raise RuntimeError(f'Range not respected {r.status}')
  b=r.read();self.pos+=len(b);self.n+=len(b);return b
for mod in ['NIRS','EEG']:
 try:
  u=f'https://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/{mod}/{mod}_01-26_MATLAB.zip';f=RemoteFile(u);z=zipfile.ZipFile(f);ns=z.namelist();print(mod,'size',f.size,'entries',len(ns),'sample',ns[:10]);(p/(mod+'_zip_manifest.json')).write_text(json.dumps([{'name':i.filename,'size':i.file_size,'compressed':i.compress_size} for i in z.infolist()],indent=2),'utf-8')
  selected=[x for x in ns if 'VP001' in x and x.endswith(('cnt_wg.mat','mrk_wg.mat','mnt_wg.mat'))]
  print('SELECT',selected)
  for x in selected:
   b=z.read(x);out=p/'sample_subject001'/mod/pathlib.PurePosixPath(x).name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b);print('SAVED',str(out),len(b))
  print('transferred',f.n)
 except Exception as e:print(mod,type(e).__name__,str(e))
