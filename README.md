# ⚽ FIFA Men's International Football Results — EDA Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Dataset:** `results.csv` — FIFA Men's International Football Matches (1872–2023)

---

## 📁 Project Structure

```
dashboard_project/
├── data/
│   └── results.csv              ← Dataset (DO NOT rename)
├── notebooks/
│   └── analysis.py              ← EDA script (generates all charts)
├── app.py                       ← Main Streamlit dashboard
├── charts.py                    ← All chart/visualization functions
├── filters.py                   ← Data loading & filter functions
├── requirements.txt             ← Python dependencies
└── README.md                    ← This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### 3. Run EDA Analysis (without Streamlit)

```bash
cd notebooks
python analysis.py
```

Charts will be saved to `notebooks/eda_output/`.

---

## 📊 Dataset: `results.csv`

| Column       | Description                                       |
|--------------|---------------------------------------------------|
| `date`       | Match date (YYYY-MM-DD)                           |
| `home_team`  | Home team name                                    |
| `away_team`  | Away team name                                    |
| `home_score` | Goals scored by home team                         |
| `away_score` | Goals scored by away team                         |
| `tournament` | Tournament name (e.g. FIFA World Cup, UEFA Euro)  |
| `city`       | City where match was played                       |
| `country`    | Country where match was played                    |
| `neutral`    | TRUE if played at a neutral venue                 |

---

## 🖼️ Charts Implemented (All 10 Required + 1 Bonus)

| # | Chart Type   | Purpose                                          |
|---|--------------|--------------------------------------------------|
| 1 | Pie Chart    | Match result distribution (Win/Draw/Loss %)      |
| 2 | Histogram    | Total goals per match frequency distribution     |
| 3 | Line Chart   | Average goals per match over the years           |
| 4 | Bar Chart    | Top 15 teams by matches won                      |
| 5 | Scatter Plot | Home score vs Away score coloured by result      |
| 6 | Box Plot     | Goals spread across top 5 tournaments            |
| 7 | Heatmap      | Feature correlation matrix                       |
| 8 | Area Chart   | Match results stacked over time                  |
| 9 | Count Plot   | Match count per tournament                       |
|10 | Violin Plot  | Goals density by match result                    |
|🎁 | Pair Plot    | Bonus — pairwise scatter of score features       |

---

## 🔽 Dashboard Filters (All 6 Required)

| Filter                  | Type              | Description                            |
|-------------------------|-------------------|----------------------------------------|
| Year Range              | Range Slider      | Filter matches by year range           |
| Tournament              | Multi-Select      | Filter by one or more tournaments      |
| Team                    | Multi-Select      | Filter where team is home or away      |
| Match Result            | Multi-Select      | Filter by Home Win / Draw / Away Win   |
| Search                  | Text Input        | Search by team, city, or country name  |
| Reset All Filters       | Button            | Resets all filters to defaults         |

All charts update dynamically when any filter changes.

---

## 📦 Tech Stack

| Tool        | Role                                  |
|-------------|---------------------------------------|
| Python 3.x  | Core language                         |
| Pandas      | Data loading, cleaning, aggregation   |
| NumPy       | Numerical operations                  |
| Matplotlib  | Core chart rendering                  |
| Seaborn     | Statistical styling                   |
| Streamlit   | Interactive dashboard frontend        |

---

## 💡 Key Insights

- **Home advantage is real:** ~47% of matches are won by the home team vs ~27% away wins.
- **Goals are declining slightly** in modern football compared to the high-scoring 1950s–70s era.
- **Brazil and Germany** lead all teams in total wins across international history.
- **FIFA World Cup** accounts for the majority of high-stakes international matches.
- **Home score and total goals** are strongly correlated (as expected).
- Draws are most common in **UEFA Euro** group-stage matches.

---

## ☁️ Deployment

This dashboard can be deployed to the cloud. See `Deployment_Guide_Vercel_Render_Railway.pdf`.

**Recommended:** Deploy on **Railway** (supports Python + Streamlit in one click).

```bash
# Railway deployment
railway login
railway link
railway up
```

Or use **Render**:
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

---

*Built with ❤️ using Python, Pandas, Matplotlib, Seaborn, and Streamlit.*
