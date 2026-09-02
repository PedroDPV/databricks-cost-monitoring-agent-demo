"""
Automated report generator.

Renders cost summary and anomaly detection results as a Markdown report,
similar in spirit to the automated pipeline documentation generator I
built professionally alongside the cost-monitoring agent.
"""
from __future__ import annotations

import os
from datetime import datetime

import pandas as pd


def generate_markdown_report(
    cost_summary: pd.DataFrame,
    anomalies: pd.DataFrame,
    output_dir: str,
) -> str:
    """Render a Markdown cost report and write it to output_dir.

    Args:
        cost_summary: output of cost_analyzer.summarize_cost_by_cluster.
        anomalies: output of cost_analyzer.detect_cost_anomalies.
        output_dir: directory where the report file will be written.

    Returns:
        The full path to the generated report file.
    """
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Databricks Cost Monitoring Report (Demo)",
        "",
        f"Generated at: {timestamp}",
        "",
        "This report is based on synthetic sample data and is intended for demonstration purposes only.",
        "",
        "## Cost by cluster",
        "",
        cost_summary.to_markdown(index=False),
        "",
        "## Anomalies detected",
        "",
    ]

    if anomalies.empty:
        lines.append("No cost anomalies detected in this run.")
    else:
        lines.append(anomalies.to_markdown(index=False))

    report_text = "\n".join(lines) + "\n"
    output_path = os.path.join(output_dir, "cost_report.md")

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(report_text)

    return output_path
