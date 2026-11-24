from pathlib import Path
import sys,json
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');sys.path.insert(0,str(p/'python_deps'));import numpy as np;from scipy.io import loadmat
out={}
for mod in ['EEG','NIRS']:
 a=loadmat(p/'sample_subject001'/mod/'cnt_wg.mat',simplify_cells=True)['cnt_wg'];m=loadmat(p/'sample_subject001'/mod/'mrk_wg.mat',simplify_cells=True)['mrk_wg'];aa=a if mod=='EEG' else a['oxy'];x=aa['x'];fs=aa['fs'];out[mod]={'fs':float(fs),'shape':list(x.shape),'label_shape':list(m['y'].shape),'counts':m['y'].sum(axis=1).tolist(),'classes':list(m.get('className',[])),'first_events_ms':m['time'][:5].tolist(),'finite':bool(np.isfinite(x).all()),'duration_s':float(x.shape[0]/fs),'event_times':m['time'].tolist()};print(mod,{k:v for k,v in out[mod].items() if k!='event_times'})
print('event delta max milliseconds',np.max(np.abs(np.array(out['EEG']['event_times'])-np.array(out['NIRS']['event_times']))));(p/'sample_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf-8')
