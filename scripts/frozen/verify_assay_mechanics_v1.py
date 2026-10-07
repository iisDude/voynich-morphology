"""Small falsification fixtures for parser, graph leakage and mask bookkeeping."""
from common import OUT,write_json,SEED
from parse_comparison_transcriptions_v2 import clean,signs,logical_lines
from structural_assays import edge_graph,alternate_prediction,graph_assay,regression
from analyse_native_structure import unpack
import numpy as np

checks=[]
def check(name,condition):
    checks.append(dict(name=name,passed=bool(condition)))
    if not condition:raise AssertionError(name)

meta={};text,events,ligatures=clean(' {ch} <note> o <@H=2> <- > ',meta)
check('Ligature signs retained, annotations removed, scoped hand recorded',text=='cho' and meta=={'H':'2'} and ligatures==['ch'])
check('v101 punctuation retained as valid literal signs',signs('3#+!(&','v101')==list('3#+!(&'))
check('EVA punctuation abstains',signs('ch!','ZL_EVA') is None)
check('Numeric escape atomic and bounded',signs('a@128;b','v101')==['a','@128;','b'] and signs('@256;','v101') is None)
check('Reading alternatives abstain',signs('a[b:c]','v101') is None)
check('Logical continuation preserves one record',list(logical_lines('# ignored\n<f1r.1,@P0> ab/\n/cd\n'))==[[2,'<f1r.1,@P0> abcd']])
x=np.c_[np.ones(20),np.ones(20),np.arange(20),np.arange(20)**2]
check('Rank deficient model withheld',regression(x,np.arange(20))['beta'] is None)

rows=[]
for split in ('train','test'):
    for core in ('xy','zz'):
        for unit,p in [('a',.1),('b',.4),('c',.7)]:
            for i in range(6):rows.append(dict(units=[unit]+list(core),normalized_group_rank=p,folio_component=f'{split}_{core}',line_id=f'{split}_{core}_{i}',split=split))
edges=edge_graph(rows,'normalized_group_rank','left',5,2)
check('Signed graph orientation is target minus source',abs(edges[('a','c')]['delta']-.6)<1e-12)
check('Direct edge omitted alternate potential recovers algebraic triangle',abs(alternate_prediction(edges,'a','c')-.6)<1e-12)
result,edges,predictions,triangles=graph_assay(rows,'normalized_group_rank','left',5,2,0)
check('Removing direct edge AND all its training matched cores prevents shared-mean leakage',len(predictions)==0)
check('Common-mean triangle not counted as context-independent evidence',len(triangles)==0)

rng=np.random.default_rng(SEED);masks=[rng.integers(0,2,(h,w),dtype=np.uint8) for h,w in [(3,5),(17,23),(1,1)]];packed=[np.packbits(m.ravel(),bitorder='little') for m in masks];offsets=np.r_[0,np.cumsum([len(p) for p in packed])]
data={'data':np.concatenate(packed),'offsets':offsets,'sizes':np.array([m.shape for m in masks])}
check('Little-endian native masks restore exact odd-size pixels',all(np.array_equal(unpack(data,i),m) for i,m in enumerate(masks)))
write_json(OUT/'tests/mechanics_v1/results.json',dict(seed=SEED,checks=checks,status='passed',limits='Fixtures verify mechanics and a shared-core counterexample, not scientific source validity or every parser ambiguity.'))
print('Passed',len(checks),'mechanics checks')
