"""Read supplied UD corpora as sentence-rank controls, with no physical pixels."""
from common import ROOT,OUT,sha256,write_json,SEED
import zipfile
import unicodedata
import hashlib


def main():
    summary=[]
    for name,archive in [('Finnish','UD_Finnish-TDT-master.zip'),('Turkish','UD_Turkish-IMST-master.zip'),('Latin','UD_Latin-PROIEL-master.zip')]:
        path=ROOT/archive;records=[];documents=set();sentences=0
        with zipfile.ZipFile(path) as z:
            for member in sorted(n for n in z.namelist() if n.endswith('.conllu')):
                document=member;sentenceid=None;forms=[]
                def flush():
                    nonlocal forms,sentences
                    if not forms:return
                    sentences+=1;documents.add(document)
                    bucket=int(hashlib.sha256(f'{SEED}|{name}|{document}'.encode()).hexdigest()[:16],16)%5
                    split='train' if bucket<3 else 'validation' if bucket==3 else 'test'
                    for i,form in enumerate(forms):
                        records.append(dict(group_id=f'{name}_{sentences:06d}_{i:03d}',line_id=f'{name}_{sentences:06d}',folio_component=document,split=split,units=list(form),form=form,normalized_group_rank=i/(len(forms)-1) if len(forms)>1 else .5,normalized_pixel_center=None,group_rank=i,group_count=len(forms),section=name,hand=None,currier=None,coordinate_kind='UD sentence token rank; no manuscript physical line or pixel position'))
                    forms=[]
                for raw in z.read(member).decode('utf-8-sig').splitlines()+['']:
                    if not raw.strip():flush();continue
                    if raw.startswith('# newdoc'):
                        document=name+'|newdoc|'+raw.split('=',1)[-1].strip();continue
                    if raw.startswith('# source'):
                        document=name+'|source|'+raw.split('=',1)[-1].strip();continue
                    if raw.startswith('# sent_id'):
                        sentenceid=raw.split('=',1)[-1].strip()
                        if name=='Finnish' and '.' in sentenceid:
                            document=name+'|sent_id_prefix|'+sentenceid.rsplit('.',1)[0]
                        elif name=='Turkish' and '_' in sentenceid:
                            document=name+'|sent_id_prefix|'+sentenceid.rsplit('_',1)[0]
                        continue
                    if raw.startswith('#'):continue
                    fields=raw.split('\t')
                    if len(fields)<4 or not fields[0].isdigit() or fields[3] in ('PUNCT','SYM'):continue
                    form=unicodedata.normalize('NFC',fields[1]).casefold()
                    if form and any(c.isalpha() for c in form):forms.append(form)
        outfile=OUT/f'data/controls/{name.lower()}_sentence_groups.json';write_json(outfile,records)
        summary.append(dict(corpus=name,archive=archive,archive_sha256=sha256(path),sentences=sentences,groups=len(records),types=len(set(r['form'] for r in records)),document_blocks=len(documents),position_kind='ordinal sentence rank only; measured pixel controls unavailable',segmentation='NFC casefold Unicode codepoints; natural-language word boundaries from UD, not Voynich ground truth',output=outfile.relative_to(OUT).as_posix()))
        print(summary[-1],flush=True)
    write_json(OUT/'data/controls/control_manifest.json',summary)


if __name__=='__main__':main()
