from pathlib import Path
import sys
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');sys.path.insert(0,str(p/'python_deps'));from scipy.io import loadmat
for mod in ['EEG','NIRS']:
 a=loadmat(p/'sample_subject001'/mod/'mnt_wg.mat',simplify_cells=True)['mnt_wg'];print(mod,{k:(getattr(v,'shape',None),str(v)[:250]) for k,v in a.items()})
