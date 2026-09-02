"""
Cost analysis logic for the Databricks cost-monitoring agent demo.

Aggregates synthetic billing usage records and flags clusters whose cost
deviates significantly from their historical average, similarly to the
cost-monitoring agent I built professionally on top of
system.billing.usage.
"""
from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd


def to_dataframe(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert raw billing usage records into a pandas DataFrame."""
    if not records:
        raise ValueError("records must not be empty")
    return pd.DataFrame.from_records(records)


def summarize_cost_by_cluster(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize total cost and DBUs consumed per cluster.

    Args:
        df: billing usage DataFrame, as produced by to_dataframe.

    Returns:
        A DataFrame with one row per cluster_name, sorted by total cost
        descending.
    """
    summary = (
        df.groupby("cluster_name")
        .agg(
            total_cost_usd=("estimated_cost_usd", "sum"),
            total_dbus=("dbus", "sum"),
            usage_events=("record_id", "count"),
        )
        .reset_index()
        .sort_values("total_cost_usd", ascending=False)
    )
    return summary


def detect_cost_anomalies(
    df: pd.DataFrame,
    threshold_pct: float = 25.0,
) -> pd.DataFrame:
    """Flag clusters whose daily cost is far above their own average.

    A cluster-day is flagged as anomalous when its daily cost exceeds the
    cluster's average daily cost by more than threshold_pct percent.

    Args:
        df: billing usage DataFrame, as produced by to_dataframe.
        threshold_pct: percentage above the cluster's average daily cost
            that triggers an anomaly flag.

    Returns:
        A DataFrame with anomalous cluster-day rows only.
    """
    daily = (
        df.groupby(["cluster_name", "usage_date"])["estimated_cost_usd"]
        .sum()
        .reset_index()
    )

    cluster_avg = (
        daily.groupby("cluster_name")["estimated_cost_usd"]
        .mean()
        .rename("avg_daily_cost_usd")
    )

    merged = daily.join(cluster_avg, on="cluster_name")
    merged["pct_above_avg"] = (
        (merged["estimated_cost_usd"] - merged["avg_daily_cost_usd"])
        / merged["avg_daily_cost_usd"]
        * 100
    )

    anomalies = merged[merged["pct_above_avg"] > threshold_pct].sort_values(
        "pct_above_avg", ascending=False
    )
    return anomalies
