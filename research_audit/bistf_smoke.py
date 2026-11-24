from pathlib import Path
import sys,ast,json,time
p=Path(r'C:\lunwen\research_audit\new_direction_20261122');sys.path.insert(0,str(p/'python_deps'))
import torch
# Keep model definitions and the imports actually needed to instantiate them. Architecture is unchanged.
src=p/'bistf_source/BiSTF-Net-main/model.py';tree=ast.parse(src.read_text('utf-8'));body=[]
for n in tree.body:
 if isinstance(n,(ast.Import,ast.ImportFrom)):
  modules=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module or '']
  if not all(m.split('.')[0] in {'torch','numpy','einops','os','time'} for m in modules):continue
 body.append(n)
namespace={};exec(compile(ast.Module(body=body,type_ignores=[]),str(src),'exec'),namespace)
torch.set_num_threads(2);torch.manual_seed(42);net=namespace['BiSTFNet']();net.train();e=torch.randn(2,16,16,600,1);f=torch.randn(2,11,16,16,30,2);start=time.time();r=net(e,f);loss=torch.nn.functional.cross_entropy(r['class_output'],torch.tensor([0,1]));loss.backward();o={'torch':torch.__version__,'device':'CPU','params':sum(x.numel() for x in net.parameters()),'logits_shape':list(r['class_output'].shape),'loss':float(loss.detach()),'finite':bool(torch.isfinite(r['class_output']).all()),'grad_params':sum(x.grad is not None for x in net.parameters()),'elapsed_s':time.time()-start,'boundary':'Random-input model forward/backward only; not a trained result, original training entrypoint not validated; unused training-library imports omitted.'};(p/'bistf_model_smoke.json').write_text(json.dumps(o,indent=2),'utf-8');print(json.dumps(o))
