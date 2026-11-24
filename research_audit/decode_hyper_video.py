from pathlib import Path
import sys,json
p=Path(r'C:\lunwen\research_audit\topic_selection_nov23');sys.path.insert(0,str(p/'deps'));import cv2
f=p/'sample_polyp.avi';cap=cv2.VideoCapture(str(f));o={'opened':bool(cap.isOpened()),'frames_reported':int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),'fps':float(cap.get(cv2.CAP_PROP_FPS)),'width':int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),'height':int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))};
for n in [0,10,30]:
 cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,frame=cap.read();o.setdefault('decoded',[]).append({'index':n,'ok':bool(ok),'shape':list(frame.shape) if ok else None});
 if ok and n==10:cv2.imwrite(str(p/'sample_polyp_frame.jpg'),frame)
cap.release();print(json.dumps(o));(p/'sample_decode.json').write_text(json.dumps(o,indent=2),'utf-8')
