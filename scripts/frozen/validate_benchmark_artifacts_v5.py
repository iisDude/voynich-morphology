"""Validate saved scripts, native atlas links and frozen source provenance."""
from common import OUT,write_json
from map_frozen_classes_v5 import verify_source_seal
from row_benchmark_guard_v5 import require_unfrozen
from html.parser import HTMLParser
import ast
class Links(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.rows=0
    def handle_starttag(self,tag,attrs):
        if tag=='article':self.rows+=1
        for k,v in attrs:
            if k in ['href','src']:self.refs.append(v)
def main():
    require_unfrozen();files=list((OUT/'src').glob('*v5*.py'))
    for p in files:ast.parse(p.read_text(encoding='utf-8'))
    page=OUT/'reports/16_source_row_reference_atlas_v5.html';parsed=Links();parsed.feed(page.read_text(encoding='utf-8'));missing=[q for q in parsed.refs if not (page.parent/q).resolve().exists()];assert not missing,missing;assert parsed.rows==16;verify_source_seal()
    write_json(OUT/'tests/row_benchmark_v5/artifact_validation.json',dict(parsed_scripts=len(files),native_atlas_rows=parsed.rows,local_image_links=len(parsed.refs),missing_links=missing,source_seal_unchanged=True))
    print('Parsed',len(files),'scripts;16 native panels, all image links valid',flush=True)
if __name__=='__main__':main()
