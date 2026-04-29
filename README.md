# 🍫 Nassau Candy Distributor — Product Line Profitability & Margin Performance Analysis

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Project Overview

Nassau Candy Distributor is a candy distribution company dealing in multiple product lines across divisions like **Chocolate**, **Sugar**, and **Other**. This project provides a comprehensive, data-driven analysis of **product profitability**, **margin performance**, and **cost efficiency** across all product lines and divisions.

The goal is to move beyond raw sales numbers and uncover **which products truly drive profit**, which divisions underperform financially, and where pricing or sourcing decisions need attention.

---

## 🎯 Problem Statement

The organization currently lacks visibility into:

- Which product lines deliver the highest gross margin
- Whether high-sales products are actually profitable
- How profitability varies across product divisions and factories
- Which products represent margin risk

---

## 📊 Dataset Overview

| Field | Description |
|-------|-------------|
| Order ID | Unique order identifier |
| Order Date | Date of order |
| Ship Mode | Shipping method |
| Customer ID | Unique customer identifier |
| Division | Product division (Chocolate / Sugar / Other) |
| Region | Customer region |
| Product Name | Product name |
| Sales | Total sales value |
| Units | Total units sold |
| Gross Profit | Sales - Cost |
| Cost | Manufacturing cost |

**Total Records:** 10,194 orders  
**Time Period:** 2024 - 2025  
**Total Products:** 15  
**Divisions:** Chocolate, Sugar, Other  
**Factories:** 5

---

## 🏭 Factory Information

| Factory | Location |
|---------|----------|
| Lot's O' Nuts | Arizona |
| Wicked Choccy's | Georgia |
| Sugar Shack | Minnesota |
| Secret Factory | Illinois/Iowa |
| The Other Factory | Tennessee |

---

## 🔍 Key Insights

### 💰 Overall Performance
- **Total Revenue:** $141,783.63
- **Total Gross Profit:** $93,442.80
- **Overall Gross Margin:** 65.9%

### 🏆 Top Performing Products
- Wonka Bar - Scrumdiddlyumptious → 69.44% margin
- Wonka Bar - Nutty Crunch Surprise → 71.35% margin
- Everlasting Gobstopper → 80% margin (highest!)

### 🚨 Risk Products
- Kazookles → 7.69% margin (Critical Risk)
- Fun Dip → 40% margin
- Nerds & SweeTARTS → 46.67% margin

### 📊 Division Summary
- **Chocolate** → 92.88% of revenue, 95.06% of profit
- **Other** → 6.82% of revenue, 4.64% of profit
- **Sugar** → 0.30% of revenue, 0.30% of profit

### 📈 Pareto Finding
- Only **5 out of 15 products** drive **80%+ of total profit**
- High concentration risk in Chocolate division

---

## 🛠️ Tech Stack

- **Python** — Data analysis
- **Pandas** — Data manipulation
- **Matplotlib / Seaborn** — Static visualizations
- **Plotly** — Interactive charts
- **Streamlit** — Web dashboard

---

## 📁 Project Structure


---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/kshitij472/Massua-Candy-Distributor.git
cd Massua-Candy-Distributor

2. Create virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run Streamlit dashboard
streamlit run streamlit_app/app.py

👨‍💻 Author
Kshitij
Data Analytics Project — Nassau Candy Distributor