import json
from pathlib import Path
from datetime import date
D=json.loads(Path("data/contributions.json").read_text());days=D["days"]
P=["#161b22","#0e4429","#006d32","#26a641","#39d353","#69f0a0"]
first=date.fromisoformat(days[0]["date"]); lead=(first.weekday()+1)%7; cells=[None]*lead+days
s=['<svg xmlns="http://www.w3.org/2000/svg" width="860" height="190">','<style>.t{font:13px monospace;fill:#8b949e}.h{font:17px monospace;fill:#c9d1d9}.c{opacity:0;animation:i .3s ease forwards}@keyframes i{to{opacity:1}}</style>','<rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/>',f'<text x="24" y="28" class="h">{sum(x["count"] for x in days):,} contributions in the last year</text>']
for i,v in enumerate(cells):
    if v is None: continue
    w,d=i//7,i%7
    s.append(f'<rect class="c" style="animation-delay:{(w+d)*.018:.3f}s" x="{38+w*15}" y="{48+d*15}" width="11" height="11" rx="2" fill="{P[min(v["level"],5)]}"/>')
s.append('<text x="650" y="178" class="t">Less  ▫ ▪ ▪ ▪ ▪  More</text></svg>')
Path("assets/contrib-heatmap.svg").write_text("\n".join(s))
