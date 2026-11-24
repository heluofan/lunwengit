import urllib.request,pathlib,json
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_nov23');x=sorted(json.loads((p/'lower_path_manifest.json').read_text()),key=lambda z:z['size'])[0]
r=urllib.request.urlopen(urllib.request.Request(x['download'],headers={'User-Agent':'Mozilla/5.0'}),timeout=60);b=r.read();f=p/'sample_polyp.avi';f.write_bytes(b);print('status',r.status,'bytes',len(b),'expected',x['size'],'content_type',r.headers.get('Content-Type'),'signature',b[:16].hex(),'label',x['label'])
