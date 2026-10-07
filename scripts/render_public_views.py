"""Link-adapted publication derivatives; original reports are never rewritten."""
from pathlib import Path
import posixpath,re,argparse
from evidence import Evidence
def render(output):
 e=Evidence();out=e.outside(output);n=0
 for s,r in e.files.items():
  if not s.startswith('reports/') or not re.match(r'reports/\d',s) or not s.endswith(('.md','.html')):continue
  target=out/('atlases/'+Path(s).name if s.endswith('.html') else 'reports/public/'+Path(s).name);target.parent.mkdir(parents=True,exist_ok=True);base=target.relative_to(out).parent.as_posix()
  def adapt(u):
   if re.match(r'^[a-z]+:|^#',u):return u
   path=posixpath.normpath(posixpath.join('reports',u.split('#')[0]));q=e.files.get(path)
   if q is None:return u
   if q['storage']=='external_source':return q.get('source_url') or u
   public=q['public_path']
   if path.startswith('reports/') and re.match(r'reports/\d',path):public=('atlases/' if path.endswith('.html') else 'reports/public/')+Path(path).name
   return posixpath.relpath(public,base)+('#'+u.split('#',1)[1] if '#' in u else '')
  text=e.bytes(s).decode('utf-8-sig')
  if s.endswith('.html'):
   text=re.sub(r'''(src|href)=(['"])([^'"]+)\2''',lambda m:m[1]+'='+m[2]+adapt(m[3])+m[2],text)
   text='<p>Publication link-adapted view. Original report bytes remain in reports/ and the frozen evidence transport. Source imagery: Beinecke MS408, Yale University; see NOTICE.md.</p>\n'+text
  else:
   text=re.sub(r'(!?\[[^\]]*\]\()([^\s)]+)(\))',lambda m:m[1]+adapt(m[2])+m[3],text)
   text='> Publication link-adapted view; the original report is preserved unchanged in `reports/`.\n\n'+text
  target.write_text(text,encoding='utf-8');n+=1
 print('Rendered public report/atlas views:',n);return n
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();render(a.output)
