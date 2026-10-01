import json
from pathlib import Path
from datetime import date


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("assets/contrib-heatmap.svg")

WIDTH = 860
HEIGHT = 190

CELL_SIZE = 11
CELL_GAP = 4

START_X = 38
START_Y = 52

ANIMATION_DURATION = 8

# GitHub-like dark palette
PALETTE = [
    "#161b22",  # 0 contributions
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]


# ============================================================
# LOAD CONTRIBUTION DATA
# ============================================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Contribution data not found: {INPUT_FILE}"
    )

data = json.loads(
    INPUT_FILE.read_text(encoding="utf-8")
)

username = data.get("username", "KhairatMouhcine")
days = data.get("days", [])


if not days:
    raise ValueError(
        "No contribution data found in contributions.json"
    )


# ============================================================
# CALCULATE STATISTICS
# ============================================================

total_contributions = sum(
    day.get("count", 0)
    for day in days
)

active_days = sum(
    1
    for day in days
    if day.get("count", 0) > 0
)

best_day = max(
    days,
    key=lambda day: day.get("count", 0)
)

best_day_count = best_day.get("count", 0)
best_day_date = best_day.get("date", "")


# ============================================================
# ALIGN FIRST DAY WITH GITHUB CALENDAR
# ============================================================

first_date = date.fromisoformat(
    days[0]["date"]
)

# Python:
# Monday = 0
#
# GitHub:
# Sunday = 0

leading_empty_days = (
    first_date.weekday() + 1
) % 7


calendar_cells = (
    [None] * leading_empty_days
    + days
)


# ============================================================
# SVG HEADER
# ============================================================

svg = [

    f'''
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>
''',

    f'''
<style>

    /* ===============================
       TEXT
       =============================== */

    .title {{
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Helvetica,
            Arial,
            sans-serif;

        font-size: 16px;
        font-weight: 600;

        fill: #c9d1d9;
    }}

    .subtitle {{
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Helvetica,
            Arial,
            sans-serif;

        font-size: 11px;

        fill: #8b949e;
    }}


    /* ===============================
       CONTRIBUTION CELLS
       =============================== */

    .contribution-cell {{

        opacity: 0.30;

        transform-box: fill-box;
        transform-origin: center;

        animation-name: contributionWave;

        animation-duration:
            {ANIMATION_DURATION}s;

        animation-timing-function:
            ease-in-out;

        animation-iteration-count:
            infinite;
    }}


    /* ===============================
       LOOP ANIMATION
       =============================== */

    @keyframes contributionWave {{

        0% {{
            opacity: 0.30;
            transform: scale(1);
        }}

        8% {{
            opacity: 0.45;
            transform: scale(1);
        }}

        15% {{
            opacity: 1;
            transform: scale(1.18);
        }}

        22% {{
            opacity: 0.80;
            transform: scale(1);
        }}

        35% {{
            opacity: 0.50;
            transform: scale(1);
        }}

        100% {{
            opacity: 0.30;
            transform: scale(1);
        }}
    }}


    /* ===============================
       TITLE ANIMATION
       =============================== */

    .live-dot {{

        animation:
            livePulse
            2s
            ease-in-out
            infinite;
    }}

    @keyframes livePulse {{

        0% {{
            opacity: .35;
        }}

        50% {{
            opacity: 1;
        }}

        100% {{
            opacity: .35;
        }}
    }}

</style>
''',

    # Background
    f'''
<rect
    width="{WIDTH}"
    height="{HEIGHT}"
    rx="14"
    fill="#0d1117"
    stroke="#30363d"
/>
''',

    # Live indicator
    '''
<circle
    class="live-dot"
    cx="26"
    cy="25"
    r="4"
    fill="#39d353"
/>
''',

    # Title
    f'''
<text
    x="38"
    y="30"
    class="title"
>
    {total_contributions:,} contributions in the last year
</text>
''',

]


# ============================================================
# WEEKDAY LABELS
# ============================================================

weekday_labels = {
    1: "Mon",
    3: "Wed",
    5: "Fri",
}


for row, label in weekday_labels.items():

    y = START_Y + row * (
        CELL_SIZE + CELL_GAP
    ) + 9

    svg.append(
        f'''
<text
    x="7"
    y="{y}"
    class="subtitle"
>
    {label}
</text>
'''
    )


# ============================================================
# CONTRIBUTION CELLS
# ============================================================

for index, contribution in enumerate(
    calendar_cells
):

    if contribution is None:
        continue


    week = index // 7

    weekday = index % 7


    x = (
        START_X
        + week
        * (CELL_SIZE + CELL_GAP)
    )


    y = (
        START_Y
        + weekday
        * (CELL_SIZE + CELL_GAP)
    )


    # ----------------------------------
    # Contribution intensity
    # ----------------------------------

    level = contribution.get(
        "level",
        0
    )

    level = max(
        0,
        min(
            level,
            len(PALETTE) - 1
        )
    )


    color = PALETTE[level]


    # ----------------------------------
    # Animation delay
    #
    # Creates the left → right wave.
    # ----------------------------------

    delay = (
        week / 53
    ) * ANIMATION_DURATION


    # Negative delay means the animation
    # starts immediately instead of waiting.

    animation_delay = -delay


    contribution_date = (
        contribution.get(
            "date",
            ""
        )
    )


    count = contribution.get(
        "count",
        0
    )


    # ----------------------------------
    # Generate cell
    # ----------------------------------

    svg.append(

        f'''
<rect
    class="contribution-cell"
    x="{x}"
    y="{y}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="2"

    fill="{color}"

    style="
        animation-delay:
        {animation_delay:.2f}s;
    "
>

    <title>
        {count} contributions
        on {contribution_date}
    </title>

</rect>
'''

    )


# ============================================================
# LEGEND
# ============================================================

legend_y = 176

svg.append(

    f'''
<text
    x="650"
    y="{legend_y}"
    class="subtitle"
>
    Less
</text>
'''

)


legend_start_x = 690


for index, color in enumerate(
    PALETTE[:5]
):

    x = (
        legend_start_x
        + index * 15
    )

    svg.append(

        f'''
<rect
    x="{x}"
    y="{legend_y - 10}"
    width="10"
    height="10"
    rx="2"
    fill="{color}"
/>
'''

    )


svg.append(

    f'''
<text
    x="770"
    y="{legend_y}"
    class="subtitle"
>
    More
</text>
'''

)


# ============================================================
# CLOSE SVG
# ============================================================

svg.append(
    "</svg>"
)


# ============================================================
# SAVE FILE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_FILE.write_text(
    "\n".join(svg),
    encoding="utf-8"
)


# ============================================================
# TERMINAL OUTPUT
# ============================================================

print()
print("========================================")
print(" GitHub Contribution Graph")
print("========================================")

print(
    f"User              : {username}"
)

print(
    f"Days              : {len(days)}"
)

print(
    f"Active days       : {active_days}"
)

print(
    f"Total contributions: {total_contributions}"
)

print(
    f"Best day          : {best_day_date}"
)

print(
    f"Best day count    : {best_day_count}"
)

print(
    f"Animation         : {ANIMATION_DURATION}s infinite loop"
)

print(
    f"Generated         : {OUTPUT_FILE}"
)

print("========================================")
print()