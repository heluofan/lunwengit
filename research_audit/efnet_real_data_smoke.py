from pathlib import Path
import sys,importlib.util,json,contextlib,io
from unittest.mock import patch
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');sys.path.insert(0,str(p/'python_deps'));import numpy as np;from scipy.io import loadmat
src=p/'efnet_source/EF-Net-main/EEG-fNIRS/data_preprocess.py';spec=importlib.util.spec_from_file_location('ef_data',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def loader(name,*args,**kwargs):
 mod='NIRS' if 'FNIRS' in name else 'EEG';return loadmat(p/'sample_subject001'/mod/Path(name).name,*args,**kwargs)
with patch.object(m.scipy.io,'loadmat',side_effect=loader),contextlib.redirect_stdout(io.StringIO()):e,f,y=m.extract_subj_dep('01',False)
o={'EEG':list(e.shape),'fNIRS':list(f.shape),'labels':list(y.shape),'finite':bool(np.isfinite(e).all() and np.isfinite(f).all()),'classes':y.sum(axis=0).tolist(),'boundary':'Original EF-Net preprocessing with only input-file resolution redirected to downloaded subject001; 360 overlapping windows represent 60 trials from one person, not 360 independent people.'};(p/'efnet_real_sample_pipeline.json').write_text(json.dumps(o,indent=2),'utf-8');print(json.dumps(o))
