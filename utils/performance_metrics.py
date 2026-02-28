"""Lightweight in-session performance metric tracking."""

from __future__ import annotations

from statistics import mean
from typing import Dict, List, Optional
import time

import streamlit as st


def _ensure_metrics_store() -> None:
    if "performance_metrics" not in st.session_state:
        st.session_state.performance_metrics = []


def record_metric(metric_name: str, duration_seconds: float, context: Optional[Dict] = None) -> None:
    """Record a latency metric in session state."""
    _ensure_metrics_store()
    st.session_state.performance_metrics.append(
        {
            "metric": metric_name,
            "duration_seconds": round(float(duration_seconds), 4),
            "timestamp": time.time(),
            "context": context or {},
        }
    )

    # Keep history bounded.
    if len(st.session_state.performance_metrics) > 500:
        st.session_state.performance_metrics = st.session_state.performance_metrics[-500:]


def get_metrics(metric_name: Optional[str] = None) -> List[Dict]:
    """Fetch all metrics or only those for a specific metric name."""
    _ensure_metrics_store()
    if not metric_name:
        return list(st.session_state.performance_metrics)
    return [m for m in st.session_state.performance_metrics if m.get("metric") == metric_name]


def summarize_metric(metric_name: str) -> Dict[str, float]:
    """Return count/min/max/avg/p95 summary for a metric."""
    rows = get_metrics(metric_name)
    if not rows:
        return {"count": 0, "min": 0.0, "max": 0.0, "avg": 0.0, "p95": 0.0}

    values = sorted(float(item.get("duration_seconds", 0.0)) for item in rows)
    count = len(values)
    p95_index = min(count - 1, int(round(0.95 * (count - 1))))
    return {
        "count": count,
        "min": values[0],
        "max": values[-1],
        "avg": mean(values),
        "p95": values[p95_index],
    }
