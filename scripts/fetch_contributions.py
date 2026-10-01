import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "KhairatMouhcine"

url = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30,
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for element in soup.select(
    "td.ContributionCalendar-day, rect.ContributionCalendar-day"
):
    contribution_date = element.get("data-date")

    if not contribution_date:
        continue

    days.append(
        {
            "date": contribution_date,
            "count": int(element.get("data-count") or 0),
            "level": int(element.get("data-level") or 0),
        }
    )


# IMPORTANT : créer le dossier data avant d'écrire le fichier
data_dir = Path("data")
data_dir.mkdir(parents=True, exist_ok=True)

output_file = data_dir / "contributions.json"

output_file.write_text(
    json.dumps(
        {
            "username": USERNAME,
            "days": days,
        },
        indent=2,
    ),
    encoding="utf-8",
)

print(f"✅ {len(days)} days fetched")
print(f"🔥 {sum(day['count'] for day in days)} contributions")
print(f"💾 Saved to {output_file}")