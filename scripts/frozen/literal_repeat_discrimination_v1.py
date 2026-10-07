"""Literal EVA ee/eee section assay; document blocks, explicit power gates."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from run_structural_tests_v2 import load,input_path
import context_assays_v0 as context
import numpy as np

def literal_features(rows,representation=None):
    groups=[''.join(r['units']) for r in rows];n=max(1,len(groups))
    return dict(ee_group_fraction=sum('ee' in g for g in groups)/n,eee_group_fraction=sum('eee' in g for g in groups)/n,e_per_unit=sum(g.count('e') for g in groups)/max(1,sum(len(g) for g in groups)),mean_length=sum(len(g) for g in groups)/n)

def main():
    context.features=literal_features
    root=OUT/'tests/literal_e_repetition_v1';root.mkdir(parents=True,exist_ok=True);results=[];counts=[]
    for name in ('ZL_EVA','RF'):
        rows=load(name)
        for r in context.same_hand(rows):results.append(dict(dataset=name,scope='same_hand_same_currier',**r))
        for lang in ('A','B'):
            rr=[r for r in rows if r.get('currier')==lang]
            for r in context.context_prediction(rr):results.append(dict(dataset=name,scope='same_currier_all_hands',currier=lang,**r))
        for doc,rr in context.docs(rows).items():
            labels={(r.get('section'),r.get('currier'),r.get('hand')) for r in rr}
            section,currier,hand=next(iter(labels)) if len(labels)==1 else (None,None,None)
            counts.append(dict(dataset=name,document=doc,split=rr[0]['split'],section=section,currier=currier,hand=hand,groups=len(rr),**literal_features(rr)))
    write_json(root/'results.json',results);write_csv(root/'document_fractions.csv',counts);write_csv(root/'results.csv',[dict(dataset=r['dataset'],scope=r['scope'],currier=r.get('currier'),hand=r.get('hand'),section_a=r['label_a'],section_b=r['label_b'],status=r['status'],heldout_auc=r.get('heldout_document_auc'),ci=r.get('bootstrap_interval'),p=r.get('test_document_label_null_p')) for r in results])
    write_json(root/'config.json',dict(seed=SEED,feature='Four averaged document features: literal ee/eee group fractions, e/unit fraction, mean encoded group length. C=1 logistic model; training vocabulary irrelevant.',minimum_train_docs_per_class=6,minimum_test_docs_per_class=3,heldout='frozen caption split; train+validation fit, calibration excluded',bootstrap=1000,heldout_label_null=199,limits=['Same-currier all-hand contrasts are confounded sensitivities.', 'Literal e repetitions are transcription observations, not established physical minim repetitions.', 'Document blocks may share physical bifolios; exact earlier AUC settings unavailable.']))
    write_json(root/'input_manifest.json',dict(sources=[dict(path=input_path(n).relative_to(OUT).as_posix(),sha256=sha256(input_path(n))) for n in ('ZL_EVA','RF')],source_sha256=sha256(OUT/'src/literal_repeat_discrimination_v1.py')))
    (root/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nfrom literal_repeat_discrimination_v1 import main\nmain()\n',encoding='utf-8')
    (root/'README.md').write_text('# Literal EVA repetitions\n\nRun `run.py`. Source minim measurements are a different test. Literal ee and eee counts and held-out document discrimination are explicit; inadequate independent document counts withhold AUC.\n',encoding='utf-8')
    (root/'summary.md').write_text('# Literal repetition sensitivity\n\nLedger test 9 receives a defined document-level analogue. Same-hand same-Currier comparisons are primary; all-hand variants remain labeled confounded. Neither repeated encoded symbols nor section discrimination proves a phonetic vowel or recurring pen stroke.\n',encoding='utf-8')
    print('Literal repeat comparisons',len(results),'estimable',sum(r['status']=='estimated' for r in results),flush=True)

if __name__=='__main__':main()
