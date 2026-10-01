import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

USERNAME = "KhairatMouhcine"

url = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for element in soup.select(
    "td.ContributionCalendar-day, rect.ContributionCalendar-day"
):
    date = element.get("data-date")

    if not date:
        continue

    count = int(element.get("data-count") or 0)
    level = int(element.get("data-level") or 0)

    days.append({
        "date": date,
        "count": count,
        "level": level
    })


# ✅ Create data/ automatically if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(parents=True, exist_ok=True)


output = {
    "username": USERNAME,
    "days": days
}

Path("data/contributions.json").write_text(
    json.dumps(output, indent=2),
    encoding="utf-8"
)

print(f"✅ Fetched {len(days)} contribution days")
print(f"🔥 Total contributions: {sum(day['count'] for day in days)}")