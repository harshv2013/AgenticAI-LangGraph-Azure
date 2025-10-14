import os
import matplotlib
matplotlib.use("Agg")  # ✅ use non-GUI backend
import matplotlib.pyplot as plt
import pandas as pd


def visualize_data(state: dict):
    """Generate multiple visualizations for sales dataset."""
    df: pd.DataFrame = state.get("df")
    if df is None:
        return {"error": "No dataframe to visualize"}

    charts = {}

    try:
        # 1. Histogram
        hist_path = "charts_histogram.png"
        df[["Units", "Revenue", "Profit"]].hist(figsize=(8, 6))
        plt.tight_layout()
        plt.savefig(hist_path)
        plt.close()
        charts["histogram"] = hist_path

        # 2. Line chart
        line_path = "charts_revenue_over_time.png"
        df_sorted = df.sort_values("Date")
        plt.figure(figsize=(8, 5))
        plt.plot(df_sorted["Date"], df_sorted["Revenue"], marker="o")
        plt.xticks(rotation=45)
        plt.title("Revenue Over Time")
        plt.xlabel("Date")
        plt.ylabel("Revenue")
        plt.tight_layout()
        plt.savefig(line_path)
        plt.close()
        charts["line"] = line_path

        # 3. Bar chart
        bar_path = "charts_profit_by_region.png"
        profit_by_region = df.groupby("Region")["Profit"].mean()
        profit_by_region.plot(kind="bar", figsize=(6, 4))
        plt.title("Average Profit by Region")
        plt.ylabel("Profit")
        plt.tight_layout()
        plt.savefig(bar_path)
        plt.close()
        charts["bar"] = bar_path

        # 4. Scatter
        scatter_path = "charts_revenue_vs_profit.png"
        plt.figure(figsize=(6, 5))
        plt.scatter(df["Revenue"], df["Profit"], alpha=0.7)
        plt.title("Revenue vs Profit")
        plt.xlabel("Revenue")
        plt.ylabel("Profit")
        plt.tight_layout()
        plt.savefig(scatter_path)
        plt.close()
        charts["scatter"] = scatter_path

        return {
            "status": "visualized",
            "charts": charts,
            "df": df   # ✅ keep dataframe alive for insight_writer
        }

    except Exception as e:
        return {"error": f"Visualization failed: {str(e)}"}
