"""Read archived primary-paper attribution without executing archive code."""
from common import ROOT,OUT,write_json,sha256
from zipfile import ZipFile

def main():
    reports=[]
    for path in ROOT.glob('*.zip'):
        with ZipFile(path) as archive:
            selected=[n for n in archive.namelist() if n.endswith('voynich-multiscale-structural-model.md')]
            for name in selected:
                source=archive.read(name).decode('utf-8');lines=source.splitlines()
                reports.append(dict(archive=path.name,archive_sha256=sha256(path),entry=name,attribution_lines=lines[:45],status='archive text inspected only; no repository code executed'))
    write_json(OUT/'reports/local_primary_attribution_v1.json',reports)
    for r in reports:print(r['archive'], '\n'.join(r['attribution_lines'][:22]),flush=True)

if __name__=='__main__':main()
