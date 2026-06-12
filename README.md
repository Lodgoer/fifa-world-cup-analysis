# 📊 FIFA World Cup Data Preprocessing & Histogram Analysis

## Project Overview
This project analyzes historical FIFA World Cup data using three datasets:
- `WorldCups.csv` – Tournament-level info (year, host, goals, teams, etc.)
- `WorldCupMatches.csv` – Individual match results
- `WorldCupPlayers.csv` – Player-level details (not directly used in plots)

The goal was to clean messy real-world data, fix encoding issues, and create meaningful histograms to understand goal distributions, attendance, team performance, and tournament trends.

---

## 🧹 Data Preprocessing (Cleaning)

| Step | Action | Why |
|------|--------|-----|
| 1 | Dropped rows with missing `Year` in matches | Many empty rows existed at the end of the file |
| 2 | Converted `Year` to integer type | Needed for sorting and plotting |
| 3 | Fixed HTML artifacts in team names (e.g., `Germany'`) | Extracted clean names using string splitting |
| 4 | Replaced known wrong names: `Germany FR` → `Germany`, fixed stadium names | Encoding issues from original CSV |
| 5 | Created `Total Goals` column = Home + Away goals | Needed for goal distribution analysis |
| 6 | Filled missing `Attendance` values with median | Avoids breaking histogram while keeping realistic values |

**Results after cleaning:**
- Matches: `~800+` rows
- World Cups: `20` rows (1930–2014)
- Players: `~37,000+` rows
- No null values remain in `Total Goals`

---

## 📈 Histogram Charts & Insights

### 1. Goals Per Match
- **Bins**: 0 to 13 goals
- **Mean**: `~3.0` goals per match
- **Observation**: Most matches end with 2–3 total goals. Very few matches exceed 7 goals.
- **Green line** shows the average.

### 2. Match Attendance Distribution
- **Unit**: Thousands of spectators
- **Mean**: `~50k` per match
- **Observation**: Histogram is right-skewed — many matches have 30–50k attendance, but some finals exceed 90k.

### 3. Total Goals per Tournament
- **Bar chart** of all World Cups from 1930 to 2014
- **Peak**: 1998 and 2014 (over 170 goals each)
- **Lowest**: 1934 and 1938 (around 70 goals) — fewer matches, different format.

### 4. Home vs Away Goals (Overlapping Histogram)
- **Green**: Home team goals  
- **Red**: Away team goals  
- **Insight**: Home teams score slightly more often. The mode for both is 1 goal, but home teams have a taller bar at 2 and 3 goals.

### 5. Qualified Teams per Tournament
- **Growth over time**: From 13 teams (1930) → 32 teams (1998–2014)
- **Sharp jump** in 1998 when FIFA expanded the tournament.

### 6. Top 10 All-Time Goal-Scoring Teams
- **Brazil** is #1 (by far)
- Followed by Germany, Argentina, Italy, Spain
- The chart is horizontal for easy reading of long team names.

---

## 🧠 Final Notes
- All histograms use clean, modern styling (dark background, bright colors, clear labels).
- The code handles **real data problems** like HTML leftovers, encoding mistakes, and missing values.
- No outliers were removed — we kept the data authentic.

---

## 📁 Output
- Chart saved as: `fifa_histograms.png`

---
