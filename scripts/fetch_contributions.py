import json,requests
from bs4 import BeautifulSoup
from pathlib import Path
u="KhairatMouhcine"
r=requests.get(f"https://github.com/users/{u}/contributions",headers={"User-Agent":"Mozilla/5.0"},timeout=30);r.raise_for_status()
s=BeautifulSoup(r.text,"html.parser");days=[]
for e in s.select("td.ContributionCalendar-day, rect.ContributionCalendar-day"):
    if e.get("data-date"): days.append({"date":e["data-date"],"count":int(e.get("data-count") or 0),"level":int(e.get("data-level") or 0)})
Path("data/contributions.json").write_text(json.dumps({"username":u,"days":days},indent=2))
