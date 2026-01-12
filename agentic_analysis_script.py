import os
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime

# Paths & setup
DATA_PATH = "/private/var/folders/s5/myv5w8gx3632hwpjscfthjfh0000gn/T/gradio/33b22b978a72e21240ab9125cb59ce5295c6128abebd6a15493e9ad1fe522788/sales_data.csv"
CHART_DIR = "./"
results = {
    "insights": [],
    "charts": [],
    "errors": []
}

# Helper to save chart and register filename
def save_chart(fig, filename):
    path = os.path.join(CHART_DIR, filename)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    results['charts'].append(filename)

# Load Data
try:
    df = pd.read_csv(DATA_PATH)
    results['insights'].append(f"Loaded data with {df.shape[0]} rows and {df.shape[1]} columns.")
except Exception as e:
    results['errors'].append(f"Error loading dataset: {e}")
    print(json.dumps(results, indent=2))
    exit()

# Ensure non-empty
if df.empty:
    results['errors'].append("The dataset is empty.")
    print(json.dumps(results, indent=2))
    exit()

# ----- 1. Histogram of First Numeric Column -----
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
if numeric_cols:
    col = numeric_cols[0]
    fig, ax = plt.subplots()
    df[col].hist(ax=ax, bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f'Histogram of {col}')
    ax.set_xlabel(col)
    ax.set_ylabel('Frequency')
    fname = f"histogram_{col}.png"
    save_chart(fig, fname)
    results['insights'].append(f"Showing distribution for '{col}' (first numeric column). Mean={df[col].mean():.2f}, Std={df[col].std():.2f}.")
else:
    results['errors'].append("No numeric columns found for histogram.")

# ----- 2. Revenue over Time -----
date_cols = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()]
revenue_possible = [c for c in df.columns if 'revenue' in c.lower()]

revenue_chart_drawn = False
if date_cols and revenue_possible:
    date_col = date_cols[0]
    revenue_col = revenue_possible[0]

    # Try to parse date
    try:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df_filtered = df.dropna(subset=[date_col, revenue_col])
        df_grouped = df_filtered.groupby(df_filtered[date_col].dt.date)[revenue_col].sum()
        if not df_grouped.empty:
            fig, ax = plt.subplots(figsize=(8,4))
            df_grouped.plot(ax=ax)
            ax.set_title('Revenue over Time')
            ax.set_xlabel('Date')
            ax.set_ylabel('Revenue')
            fname = "revenue_over_time.png"
            save_chart(fig, fname)
            results['insights'].append("Visualized revenue trend over time.")
            revenue_chart_drawn = True
        else:
            results['errors'].append("No valid data after filtering for revenue over time.")
    except Exception as e:
        results['errors'].append(f"Error drawing revenue over time: {e}")
else:
    results['errors'].append("Missing 'Date'/'Time' or 'Revenue' columns for revenue trend.")

# ----- 3. Profit by Region -----
region_col = next((c for c in df.columns if 'region' in c.lower()), None)
profit_col = next((c for c in df.columns if 'profit' in c.lower()), None)

if region_col and profit_col:
    try:
        df_grouped = df.groupby(region_col)[profit_col].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8,4))
        df_grouped.plot(kind='bar', color='seagreen', ax=ax)
        ax.set_title('Total Profit by Region')
        ax.set_xlabel('Region')
        ax.set_ylabel('Profit')
        fname = "profit_by_region.png"
        save_chart(fig, fname)
        top_regions = df_grouped.head(3).to_dict()
        results['insights'].append(f"Top regions by profit: {top_regions}")
    except Exception as e:
        results['errors'].append(f"Error visualizing profit by region: {e}")
else:
    results['errors'].append("Missing 'Region' and/or 'Profit' columns for profit by region analysis.")

# ----- 4. Revenue vs Profit Scatter -----
if revenue_possible and profit_col:
    try:
        revenue_col = revenue_possible[0]
        df_scatter = df.dropna(subset=[revenue_col, profit_col])
        fig, ax = plt.subplots()
        ax.scatter(df_scatter[revenue_col], df_scatter[profit_col], alpha=0.7, edgecolor='k')
        ax.set_title('Revenue vs Profit')
        ax.set_xlabel(revenue_col)
        ax.set_ylabel(profit_col)
        fname = "revenue_vs_profit_scatter.png"
        save_chart(fig, fname)
        corr = df_scatter[revenue_col].corr(df_scatter[profit_col])
        results['insights'].append(f"Correlation between revenue and profit: {corr:.2f}")
    except Exception as e:
        results['errors'].append(f"Error plotting Revenue vs Profit: {e}")
else:
    results['errors'].append("Missing 'Revenue' and/or 'Profit' for scatter plot.")

# ----- Final output -----
print(json.dumps(results, indent=2))