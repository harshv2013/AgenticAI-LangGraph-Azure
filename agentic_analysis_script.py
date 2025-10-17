import os
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Initialize results dict
results = {
    "insights": [],
    "charts": [],
    "errors": []
}

# Dataset path
dataset_path = r"C:\Users\HarshVardhan\AppData\Local\Temp\gradio\219845c9196d8c8c1810a31b197f1063ff9be9327bc720a763268d36e7be9357\sales_data.csv"

# Prepare a folder for charts
charts_dir = "charts"
os.makedirs(charts_dir, exist_ok=True)

# Load dataset
try:
    df = pd.read_csv(dataset_path)
    results["insights"].append(f"Dataset loaded: {dataset_path}")
    results["insights"].append(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    results["insights"].append("Columns: " + ", ".join(df.columns))
except Exception as e:
    results["errors"].append(f"Failed to load CSV: {str(e)}")
    print(json.dumps(results, indent=2))
    exit()

# 1. Histogram (first numeric column)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
histogram_chart_file = ""
if numeric_cols:
    first_numeric = numeric_cols[0]
    plt.figure(figsize=(6,4))
    plt.hist(df[first_numeric].dropna(), bins=20, color="skyblue", edgecolor="black")
    plt.title(f"Histogram of {first_numeric}")
    plt.xlabel(first_numeric)
    plt.ylabel("Frequency")
    histogram_chart_file = os.path.join(charts_dir, f"hist_{first_numeric}.png")
    plt.tight_layout()
    plt.savefig(histogram_chart_file)
    plt.close()
    results["charts"].append(histogram_chart_file)
    results["insights"].append(f"Histogram of '{first_numeric}' created. Mean: {df[first_numeric].mean():.2f}, Std: {df[first_numeric].std():.2f}, Min: {df[first_numeric].min()}, Max: {df[first_numeric].max()}, Median: {df[first_numeric].median()}")
else:
    results["errors"].append("No numeric column found for histogram.")

# 2. Revenue over time
revenue_over_time_chart_file = ""
date_col = None
for col in ["Date", "date", "OrderDate", "Order Date", "Time", "Datetime", "datetime"]:
    if col in df.columns:
        date_col = col
        break

revenue_col = None
for col in ["Revenue", "revenue", "Sales", "sales"]:
    if col in df.columns:
        revenue_col = col
        break

if date_col and revenue_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    time_group = df.dropna(subset=[date_col]).groupby(df[date_col].dt.to_period("M"))[revenue_col].sum()
    plt.figure(figsize=(8,4))
    time_group.sort_index().plot(marker='o')
    plt.title(f"{revenue_col} over Time")
    plt.xlabel("Time (by Month)")
    plt.ylabel(revenue_col)
    plt.tight_layout()
    revenue_over_time_chart_file = os.path.join(charts_dir, f"{revenue_col}_over_time.png")
    plt.savefig(revenue_over_time_chart_file)
    plt.close()
    results["charts"].append(revenue_over_time_chart_file)
    results["insights"].append(f"Revenue over time chart created. Peak revenue: {time_group.max():.2f} at {time_group.idxmax()}. Overall revenue: {df[revenue_col].sum():.2f}")
else:
    if not date_col:
        results["errors"].append("No suitable date/time column found for revenue over time.")
    if not revenue_col:
        results["errors"].append("No suitable revenue column found for revenue over time.")

# 3. Profit by Region
region_col = None
for col in ["Region", "region", "Territory", "Market"]:
    if col in df.columns:
        region_col = col
        break

profit_col = None
for col in ["Profit", "profit", "Net Profit", "net profit"]:
    if col in df.columns:
        profit_col = col
        break

profit_by_region_chart_file = ""
if region_col and profit_col:
    region_profit = df.groupby(region_col)[profit_col].sum().sort_values(ascending=False)
    plt.figure(figsize=(7,4))
    region_profit.plot(kind='bar', color="seagreen")
    plt.title(f"Total Profit by {region_col}")
    plt.xlabel(region_col)
    plt.ylabel(profit_col)
    plt.tight_layout()
    profit_by_region_chart_file = os.path.join(charts_dir, f"profit_by_{region_col}.png")
    plt.savefig(profit_by_region_chart_file)
    plt.close()
    results["charts"].append(profit_by_region_chart_file)
    top_region = region_profit.idxmax()
    results["insights"].append(f"Profit by region chart created. Top region: {top_region} with profit {region_profit.max():.2f}. Regions: {region_profit.index.tolist()}.")
else:
    if not region_col:
        results["errors"].append("No suitable region column found for profit by region.")
    if not profit_col:
        results["errors"].append("No suitable profit column found for profit by region.")

# 4. Revenue vs Profit scatter
revenue_vs_profit_chart_file = ""
if revenue_col and profit_col:
    plt.figure(figsize=(6,5))
    plt.scatter(df[revenue_col], df[profit_col], alpha=0.6, color="darkorange")
    plt.title(f"{revenue_col} vs {profit_col}")
    plt.xlabel(revenue_col)
    plt.ylabel(profit_col)
    plt.tight_layout()
    revenue_vs_profit_chart_file = os.path.join(charts_dir, f"{revenue_col}_vs_{profit_col}.png")
    plt.savefig(revenue_vs_profit_chart_file)
    plt.close()
    results["charts"].append(revenue_vs_profit_chart_file)
    correlation = df[[revenue_col, profit_col]].corr().iloc[0,1]
    results["insights"].append(f"Revenue vs Profit scatter created. Correlation coefficient: {correlation:.2f}")
else:
    if not revenue_col:
        results["errors"].append("No suitable revenue column found for revenue vs profit scatter.")
    if not profit_col:
        results["errors"].append("No suitable profit column found for revenue vs profit scatter.")

print(json.dumps(results, indent=2))