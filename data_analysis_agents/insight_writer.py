

def write_insights(state: dict):
    """Generate insights from analysis results."""
    insights = []
    df = state.get("df")
    summary = state.get("summary", {})
    missing = state.get("missing", {})

    if df is not None:
        # Basic dataset info
        insights.append(f"The dataset has {len(df)} rows and {len(df.columns)} columns.")

        # Missing values
        missing_cols = [col for col, val in missing.items() if val > 0]
        if missing_cols:
            insights.append(f"Missing data found in columns: {', '.join(missing_cols)}")
        else:
            insights.append("No missing values detected.")

        # Profit analysis
        if "Profit" in df.columns:
            avg_profit = df["Profit"].mean()
            top_region = df.groupby("Region")["Profit"].mean().idxmax()
            insights.append(f"Average profit is {avg_profit:.2f}, highest in {top_region} region.")

        # Revenue analysis
        if "Revenue" in df.columns and "Profit" in df.columns:
            corr = df["Revenue"].corr(df["Profit"])
            insights.append(f"Revenue and Profit correlation: {corr:.2f} (positive means higher revenue leads to higher profit).")

    state["insights"] = insights
    return {"status": "insights_generated", "insights": insights}
