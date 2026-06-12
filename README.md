# FIFA World Cup — Data Preprocessing & Histogram Analysis  
### Project Documentation

## 1. Overview  
This project analyzes historical FIFA World Cup data using Python, Pandas, and Matplotlib.  
The goal is to clean the datasets, prepare meaningful features, and visualize important patterns such as goal distributions, attendance trends, and team performance.

The project uses three CSV files:

- WorldCups.csv — summary of each tournament  
- WorldCupMatches.csv — match-level data  
- WorldCupPlayers.csv — player information  

---

## 2. Data Loading  
We begin by importing the required libraries and loading the datasets:

```python
players   = pd.read_csv("WorldCupPlayers.csv")
matches   = pd.read_csv("WorldCupMatches.csv")
world_cup = pd.read_csv("WorldCups.csv")
```

Each dataset is stored in a Pandas DataFrame for further processing.

---

## 3. Preprocessing Steps  

### 3.1 Removing Empty Rows  
The WorldCupMatches.csv file contains many rows with missing values.  
We remove rows where the Year column is missing:

```python
matches.dropna(subset=["Year"], inplace=True)
matches["Year"] = matches["Year"].astype(int)
```

---

### 3.2 Cleaning Team Names  
Some team names contain HTML artifacts such as `rn">Germany`.  
A helper function extracts the clean name:

```python
def fix_name(name):
    if isinstance(name, str) and 'rn">' in name:
        return name.split(">")[1]
    return name
```

Applied to both home and away team names.

---

### 3.3 Fixing Encoding Issues  
Some stadium names and team names have encoding problems.  
We replace them with corrected versions:

```python
replacements = {
    "Germany FR": "Germany",
    "Maracan\xe3 - Est\xe1dio Jornalista M\xe1rio Filho": "Maracana Stadium",
    "Estadio do Maracana": "Maracana Stadium",
}
matches.replace(replacements, inplace=True)
world_cup.replace(replacements, inplace=True)
```

---

### 3.4 Creating a New Feature: Total Goals  
We compute the total number of goals scored in each match:

```python
matches["Total Goals"] = (
    matches["Home Team Goals"] + matches["Away Team Goals"]
)
```

---

### 3.5 Filling Missing Attendance Values  
Attendance is an important feature, so missing values are replaced with the median:

```python
matches["Attendance"] = matches["Attendance"].fillna(
    matches["Attendance"].median()
)
```

---

## 4. Visualization  
We use Matplotlib with a custom dark theme to create six visualizations:

### 4.1 Histogram — Goals Per Match  
Shows how many goals are typically scored in a match.  
A vertical line marks the mean value.

### 4.2 Histogram — Match Attendance  
Attendance values are converted to thousands for readability.  
The distribution shows how crowded matches usually are.

### 4.3 Bar Chart — Total Goals per Tournament  
Displays how offensive or defensive each World Cup edition was.

### 4.4 Overlapping Histograms — Home vs Away Goals  
Compares scoring patterns between home and away teams.

### 4.5 Bar Chart — Number of Qualified Teams  
Shows how the tournament expanded over time.

### 4.6 Horizontal Bar Chart — Top 10 All-Time Scoring Teams  
Ranks the highest-scoring teams in World Cup history.

---

## 5. Output  
All charts are saved as:

```
fifa_histograms.png
```

The figure contains all six subplots arranged in a 2×3 grid..
