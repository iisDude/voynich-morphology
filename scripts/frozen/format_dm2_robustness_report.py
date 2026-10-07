from dm2_robustness_common import *
import re
guard()
path=OUT/'reports/27_direct_morphology_trial2_robustness.md'
text=path.read_text(encoding='utf-8')
text=text.replace('The28-parent-and-dyad-constrained selection','The selection constrained by parent and caption-dyad')
text=text.replace('The pre-outcome robustness rubric identifies sensitivity','The robustness protocol was sealed before this investigation’s subset and repeat outcomes, after Trial2 results were already known. Its descriptive rubric identifies sensitivity')
text=text.replace('All108 conditions use the same preregistered5,000 draws', 'The108 sensitivity conditions are strongly correlated. Their intervals are pointwise, not simultaneous guarantees, and they are not108 independent confirmations. No p-value is selected across them.\n\nAll108 conditions use the same preregistered5,000 draws')
text=text.replace('Extent-clean unrestricted results therefore equal the original result.', 'Extent-clean unrestricted results therefore equal the original result. This redundant filter cannot test morphology generalization to the excluded unknown physical extents.')
lines=[]
for line in text.splitlines():
    if '](' not in line and not line.startswith('|'):
        line=re.sub(r'(?<=[A-Za-z])(?=[0-9])',' ',line)
        line=re.sub(r'(?<=[0-9])(?=[A-Za-z])',' ',line)
        line=re.sub(r';(?=[A-Za-z0-9])','; ',line)
        line=re.sub(r'\.(?=[A-Z])','. ',line)
        line=re.sub(r'(?<=[0-9])\((?=[0-9])',' (',line)
    lines.append(line)
path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Current robustness report prose clarified; no prior evidence edited')
