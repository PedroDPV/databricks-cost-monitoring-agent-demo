"""
Synthetic Databricks billing usage generator.

Generates fake records that mimic the shape of Databricks'
system.billing.usage table, used only to demonstrate a cost-monitoring
agent. No real workspace, account, or billing data is used anywhere in
this project.
"""
from __future__ import annotations

import random
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List

_FAKE_WORKSPACES = ["analytics-prod", "analytics-staging", "ml-platform"]
_FAKE_SKUS = [
    ("JOBS_COMPUTE", 0.15),
    ("ALL_PURPOSE_COMPUTE", 0.40),
    ("SQL_COMPUTE", 0.22),
    ("DLT_ADVANCED", 0.36),
]
_FAKE_CLUSTER_PREFIXES = ["etl", "reporting", "ml-training", "ad-hoc"]


def generate_fake_billing_usage(
    num_records: int = 1000,
    seed: int = 42,
    inject_anomaly: bool = True,
) -> List[Dict[str, Any]]:
    """Generate synthetic Databricks billing usage records.

    Args:
        num_records: number of synthetic usage records to generate.
        seed: random seed for reproducibility.
        inject_anomaly: if True, injects a synthetic cost spike on one
            cluster so the anomaly detection logic has something to find.

    Returns:
        A list of dictionaries shaped like system.billing.usage rows.
    """
    rng = random.Random(seed)
    records: List[Dict[str, Any]] = []
    base_time = datetime(2026, 8, 1)

    for _ in range(num_records):
        sku_name, dbu_rate = rng.choice(_FAKE_SKUS)
        cluster_name = f"{rng.choice(_FAKE_CLUSTER_PREFIXES)}-{rng.randint(1, 9)}"
        dbus = round(rng.uniform(0.5, 12.0), 2)
        record = {
            "record_id": str(uuid.uuid4()),
            "workspace_id": rng.choice(_FAKE_WORKSPACES),
            "sku_name": sku_name,
            "cluster_name": cluster_name,
            "usage_date": (base_time + timedelta(days=rng.randint(0, 29))).date().isoformat(),
            "dbus": dbus,
            "estimated_cost_usd": round(dbus * dbu_rate, 4),
        }
        records.append(record)

    if inject_anomaly and records:
        spike_cluster = "etl-1"
        for _ in range(10):
            records.append(
                {
                    "record_id": str(uuid.uuid4()),
                    "workspace_id": "analytics-prod",
                    "sku_name": "JOBS_COMPUTE",
                    "cluster_name": spike_cluster,
                    "usage_date": base_time.date().isoformat(),
                    "dbus": 150.0,
                    "estimated_cost_usd": round(150.0 * 0.15, 4),
                }
            )

    return records
