"""
FIFA World Cup — Data Preprocessing & Histogram Analysis
=========================================================
داده‌ها:
  - WorldCups.csv       : اطلاعات کلی هر دوره جام‌جهانی
  - WorldCupMatches.csv : نتایج بازی‌ها
  - WorldCupPlayers.csv : اطلاعات بازیکنان
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ═══════════════════════════════════════════════
#  1. LOAD DATA  —  بارگذاری داده‌ها
# ═══════════════════════════════════════════════
players   = pd.read_csv("WorldCupPlayers.csv")
matches   = pd.read_csv("WorldCupMatches.csv")
world_cup = pd.read_csv("WorldCups.csv")


# ═══════════════════════════════════════════════
#  2. PREPROCESSING  —  پیش‌پردازش
# ═══════════════════════════════════════════════

# 2-1. حذف ردیف‌های خالی (matches خیلی null row داره)
matches.dropna(subset=["Year"], inplace=True)
matches["Year"] = matches["Year"].astype(int)

# 2-2. پاک‌سازی اسم‌های تیم که HTML artifact دارن
def fix_name(name):
    """اسم‌هایی مثل  Germany' را تمیز می‌کند"""
    if isinstance(name, str) and 'rn">' in name:
        return name.split(">")[1]
    return name

matches["Home Team Name"] = matches["Home Team Name"].apply(fix_name)
matches["Away Team Name"] = matches["Away Team Name"].apply(fix_name)

# 2-3. اصلاح اسم‌های شناخته‌شده اشتباه (encoding مشکل‌دار)
replacements = {
    "Germany FR"  : "Germany",
    "Maracan\xe3 - Est\xe1dio Jornalista M\xe1rio Filho": "Maracana Stadium",
    "Estadio do Maracana": "Maracana Stadium",
}
matches.replace(replacements, inplace=True)
world_cup.replace(replacements, inplace=True)

# 2-4. ساخت ستون جدید: مجموع گل هر بازی
matches["Total Goals"] = matches["Home Team Goals"] + matches["Away Team Goals"]

# 2-5. مقدار خالی Attendance را با میانه جایگزین می‌کنیم
matches["Attendance"] = matches["Attendance"].fillna(matches["Attendance"].median())

print("=== Preprocessing Complete ===")
print(f"Matches  : {len(matches):,} rows")
print(f"WorldCups: {len(world_cup):,} rows")
print(f"Players  : {len(players):,} rows")
print(f"Null in Total Goals: {matches['Total Goals'].isnull().sum()}")


# ═══════════════════════════════════════════════
#  3. VISUALIZATION  —  رسم نمودارها
# ═══════════════════════════════════════════════

# ── تنظیمات رنگ و استایل
BG      = "#0d1117"
CARD    = "#161b22"
GREEN   = "#00d26a"
GOLD    = "#f5c518"
RED     = "#e05c5c"
BLUE    = "#4fa3e0"
TEXT    = "#e6edf3"
SUBTEXT = "#8b949e"

plt.rcParams.update({
    "figure.facecolor"  : BG,
    "axes.facecolor"    : CARD,
    "text.color"        : TEXT,
    "axes.labelcolor"   : TEXT,
    "xtick.color"       : SUBTEXT,
    "ytick.color"       : SUBTEXT,
    "axes.edgecolor"    : "#30363d",
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
})

fig = plt.figure(figsize=(18, 14), facecolor=BG)
fig.suptitle("FIFA World Cup — Data Analysis", fontsize=22,
             color=TEXT, fontweight="bold", y=0.97)

gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38)


# ── نمودار 1: توزیع گل در هر بازی ──────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
goals_data = matches["Total Goals"].dropna()

ax1.hist(goals_data, bins=range(0, 14), color=GREEN,
         edgecolor=BG, linewidth=0.8, rwidth=0.85)

mean_val = goals_data.mean()
ax1.axvline(mean_val, color=GOLD, linestyle="--", linewidth=1.8,
            label=f"Mean: {mean_val:.1f}")

ax1.set_title("Goals Per Match", color=TEXT, fontsize=13, pad=10)
ax1.set_xlabel("Goals", color=SUBTEXT)
ax1.set_ylabel("Number of Matches", color=SUBTEXT)
ax1.legend(facecolor=CARD, edgecolor="none", labelcolor=TEXT, fontsize=9)


# ── نمودار 2: توزیع تعداد تماشاگران ─────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
att = matches["Attendance"].dropna() / 1000   # تبدیل به هزار

ax2.hist(att, bins=20, color=BLUE, edgecolor=BG, linewidth=0.8, rwidth=0.85)
ax2.axvline(att.mean(), color=GOLD, linestyle="--", linewidth=1.8,
            label=f"Mean: {att.mean():.0f}k")

ax2.set_title("Match Attendance", color=TEXT, fontsize=13, pad=10)
ax2.set_xlabel("Attendance (thousands)", color=SUBTEXT)
ax2.set_ylabel("Number of Matches", color=SUBTEXT)
ax2.legend(facecolor=CARD, edgecolor="none", labelcolor=TEXT, fontsize=9)


# ── نمودار 3: مجموع گل در هر دوره جام‌جهانی ────────────────
ax3 = fig.add_subplot(gs[0, 2])
ax3.bar(world_cup["Year"].astype(str), world_cup["GoalsScored"],
        color=RED, edgecolor=BG, linewidth=0.6)

ax3.set_title("Total Goals per Tournament", color=TEXT, fontsize=13, pad=10)
ax3.set_xlabel("Year", color=SUBTEXT)
ax3.set_ylabel("Goals Scored", color=SUBTEXT)
ax3.tick_params(axis="x", rotation=70, labelsize=7.5)


# ── نمودار 4: مقایسه گل‌های خانه و مهمان (overlapping histogram)
ax4 = fig.add_subplot(gs[1, 0])
home_g = matches["Home Team Goals"].dropna()
away_g = matches["Away Team Goals"].dropna()

ax4.hist(home_g, bins=range(0, 12), color=GREEN, alpha=0.7,
         edgecolor=BG, linewidth=0.6, rwidth=0.85, label="Home")
ax4.hist(away_g, bins=range(0, 12), color=RED, alpha=0.7,
         edgecolor=BG, linewidth=0.6, rwidth=0.85, label="Away")

ax4.set_title("Home vs Away Goals", color=TEXT, fontsize=13, pad=10)
ax4.set_xlabel("Goals", color=SUBTEXT)
ax4.set_ylabel("Frequency", color=SUBTEXT)
ax4.legend(facecolor=CARD, edgecolor="none", labelcolor=TEXT, fontsize=9)


# ── نمودار 5: تعداد تیم‌های حاضر در هر دوره ────────────────
ax5 = fig.add_subplot(gs[1, 1])
ax5.bar(world_cup["Year"].astype(str), world_cup["QualifiedTeams"],
        color=GOLD, edgecolor=BG, linewidth=0.6)

ax5.set_title("Qualified Teams per Tournament", color=TEXT, fontsize=13, pad=10)
ax5.set_xlabel("Year", color=SUBTEXT)
ax5.set_ylabel("Number of Teams", color=SUBTEXT)
ax5.tick_params(axis="x", rotation=70, labelsize=7.5)


# ── نمودار 6: ۱۰ تیم پرگل‌ترین تاریخ جام‌جهانی ─────────────
ax6 = fig.add_subplot(gs[1, 2])

home_df = matches[["Home Team Name", "Home Team Goals"]].rename(
    columns={"Home Team Name": "Team", "Home Team Goals": "Goals"})
away_df = matches[["Away Team Name", "Away Team Goals"]].rename(
    columns={"Away Team Name": "Team", "Away Team Goals": "Goals"})

all_goals = (
    pd.concat([home_df, away_df])
    .groupby("Team")["Goals"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

bar_colors = [GOLD if i == 0 else GREEN for i in range(len(all_goals))]
ax6.barh(all_goals.index[::-1], all_goals.values[::-1],
         color=bar_colors[::-1], edgecolor=BG, linewidth=0.6)

ax6.set_title("Top 10 Teams — All-Time Goals", color=TEXT, fontsize=13, pad=10)
ax6.set_xlabel("Total Goals", color=SUBTEXT)
ax6.tick_params(axis="y", labelsize=8.5)


# ── ذخیره و نمایش
plt.savefig("fifa_histograms.png", dpi=160, bbox_inches="tight", facecolor=BG)
plt.show()
print("\nChart saved: fifa_histograms.png")