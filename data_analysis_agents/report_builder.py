

def build_report(state: dict):
    """Assemble Markdown report with insights and multiple charts."""
    insights = state.get("insights", [])
    charts = state.get("charts", {})

    report_md = "# 📊 Data Analysis Report\n\n"
    report_md += "## Key Insights\n"
    for point in insights:
        report_md += f"- {point}\n"

    if charts:
        report_md += "\n## Visualizations\n"
        if "histogram" in charts:
            report_md += f"### Distribution of Numeric Features\n![Histogram]({charts['histogram']})\n"
        if "line" in charts:
            report_md += f"### Revenue Over Time\n![Line Chart]({charts['line']})\n"
        if "bar" in charts:
            report_md += f"### Average Profit by Region\n![Bar Chart]({charts['bar']})\n"
        if "scatter" in charts:
            report_md += f"### Revenue vs Profit\n![Scatter Plot]({charts['scatter']})\n"

    state["report"] = report_md
    return {"status": "report_built", "report": report_md}

