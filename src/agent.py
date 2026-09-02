"""
Cost-monitoring agent entry point.

Runs the full flow: generate synthetic billing usage, summarize cost per
cluster, detect anomalies, and write a Markdown report. This script is
self-contained and does not connect to any real Databricks workspace.
"""
from __future__ import annotations

import logging

from src.billing_data_generator import generate_fake_billing_usage
from src.config import settings
from src.cost_analyzer import (
    detect_cost_anomalies,
    summarize_cost_by_cluster,
    to_dataframe,
)
from src.report_generator import generate_markdown_report

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


def run_agent(num_records: int = 1000) -> str:
    """Run the cost-monitoring agent end to end and return the report path."""
    logger.info("Starting cost-monitoring agent demo (environment=%s)", settings.environment)

    records = generate_fake_billing_usage(num_records=num_records)
    logger.info("Generated %d synthetic billing usage records", len(records))

    df = to_dataframe(records)
    cost_summary = summarize_cost_by_cluster(df)
    anomalies = detect_cost_anomalies(df, threshold_pct=settings.cost_anomaly_threshold_pct)

    logger.info("Detected %d anomalous cluster-day entries", len(anomalies))

    report_path = generate_markdown_report(cost_summary, anomalies, settings.report_output_dir)
    logger.info("Report written to %s", report_path)
    return report_path


if __name__ == "__main__":
    run_agent()
