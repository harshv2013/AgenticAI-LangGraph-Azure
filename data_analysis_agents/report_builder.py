

# def build_report(state: dict):
#     """Assemble Markdown report with insights and multiple charts."""
#     insights = state.get("insights", [])
#     charts = state.get("charts", {})

#     report_md = "# 📊 Data Analysis Report\n\n"
#     report_md += "## Key Insights\n"
#     for point in insights:
#         report_md += f"- {point}\n"

#     if charts:
#         report_md += "\n## Visualizations\n"
#         if "histogram" in charts:
#             report_md += f"### Distribution of Numeric Features\n![Histogram]({charts['histogram']})\n"
#         if "line" in charts:
#             report_md += f"### Revenue Over Time\n![Line Chart]({charts['line']})\n"
#         if "bar" in charts:
#             report_md += f"### Average Profit by Region\n![Bar Chart]({charts['bar']})\n"
#         if "scatter" in charts:
#             report_md += f"### Revenue vs Profit\n![Scatter Plot]({charts['scatter']})\n"

#     state["report"] = report_md
#     return {"status": "report_built", "report": report_md}



# data_analysis_agents/report_builder.py
def build_report(state):
    """
    state expected to include:
     - 'ingest' output (columns, rows)
     - 'executor' output (insights, charts)
     - 'summary' (text)
     - 'suggestions'
    Returns final report dict
    """
    ingest = state.get("ingest", {})
    exec_res = state.get("executor", {})
    summary = state.get("summarizer", {}).get("summary") or ""
    suggestions = state.get("suggestor", {}).get("suggestions") or ""

    report_lines = []
    report_lines.append("# 📊 Data Analysis Report")
    report_lines.append("")
    report_lines.append("## Dataset")
    report_lines.append(f"- Rows: {ingest.get('rows')}")
    report_lines.append(f"- Columns: {', '.join(ingest.get('columns') or [])}")
    report_lines.append("")
    report_lines.append("## Key Insights")
    for s in exec_res.get("insights", []):
        report_lines.append(f"- {s}")
    if summary:
        report_lines.append("")
        report_lines.append("## Summary")
        report_lines.append(summary)

    if suggestions:
        report_lines.append("")
        report_lines.append("## Suggested follow-ups")
        report_lines.append(suggestions)

    final = "\n".join(report_lines)
    out = {
        "status": "report_built",
        "report": final,
        "charts": exec_res.get("charts", {}),
    }
    return out
