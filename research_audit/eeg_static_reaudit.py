from pathlib import Path
import ast,json,sys,math
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');q=p/'feasibility_recheck';src=p/'bistf_source/BiSTF-Net-main/preprocessing.py';tree=ast.parse(src.read_text('utf-8'));found=[]
for node in ast.walk(tree):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr in ['filter','fit','plot_sources']:
  found.append({'line':node.lineno,'call':ast.unparse(node)[:450]})
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='input':found.append({'line':node.lineno,'call':ast.unparse(node)})
train=(p/'bistf_source/BiSTF-Net-main/train.py').read_text('utf-8');tr=ast.parse(train);assigned=set()
for n in ast.walk(tr):
 if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store):assigned.add(n.id)
o={'preprocessing_operations':found,'train_device_assignment_present':'device' in assigned,'training_entrypoint_has_test_selection':"trainer.evaluate(test_loader)" in train and "eval_result['class_acc'] > best_acc" in train,'epoch_pre_onset_s':5,'first_window_start_from_epoch_s':3,'first_eeg_window_event_relative_s':[-2,1],'first_fnirs_candidate_union_event_relative_s':[-2,11],'coordinate_boundary':'Derived only if supplied training input uses the preprocessing.py epoch origin. The released train/preprocessing NPZ interfaces differ, so actual published training coordinates are not established by these files alone.'}
(q/'static_code_recheck.json').write_text(json.dumps(o,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(o,ensure_ascii=False,indent=2))
sys.path.insert(0,str(p/'python_deps'));import numpy as np
# Planning sensitivity, not an estimate of this dataset's effect or variance.
rows=[]
for sd in [.05,.10,.15]:
 se=sd/math.sqrt(26);rows.append({'paired_subject_difference_sd_assumption':sd,'approx_95ci_half_width_pp':2.06*se*100,'approx_effect_pp_for_80percent_power':(1.96+.842)*se*100})
(q/'planning_sensitivity_assumptions.json').write_text(json.dumps(rows,indent=2),'utf-8');print('ASSUMPTION_ONLY',rows)
