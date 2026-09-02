"""Unit tests for the cost analyzer."""
from src.billing_data_generator import generate_fake_billing_usage
from src.cost_analyzer import (
    detect_cost_anomalies,
    summarize_cost_by_cluster,
    to_dataframe,
)


def test_to_dataframe_shape():
    records = generate_fake_billing_usage(num_records=50, seed=1, inject_anomaly=False)
    df = to_dataframe(records)
    assert len(df) == 50
    assert "estimated_cost_usd" in df.columns


def test_summarize_cost_by_cluster_sorted_desc():
    records = generate_fake_billing_usage(num_records=200, seed=2, inject_anomaly=False)
    df = to_dataframe(records)
    summary = summarize_cost_by_cluster(df)
    costs = summary["total_cost_usd"].tolist()
    assert costs == sorted(costs, reverse=True)


def test_detect_cost_anomalies_finds_injected_spike():
    records = generate_fake_billing_usage(num_records=300, seed=3, inject_anomaly=True)
    df = to_dataframe(records)
    anomalies = detect_cost_anomalies(df, threshold_pct=25.0)
    assert not anomalies.empty
    assert "etl-1" in anomalies["cluster_name"].values


def test_detect_cost_anomalies_no_false_positive_without_spike():
    records = generate_fake_billing_usage(num_records=300, seed=4, inject_anomaly=False)
    df = to_dataframe(records)
    anomalies = detect_cost_anomalies(df, threshold_pct=200.0)
    assert anomalies.empty
