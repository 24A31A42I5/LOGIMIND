from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ShipmentRecord:
    shipment_id: str
    product: str
    customer: str
    destination: str
    area: str
    agent_id: str
    status: str
    dispatch_time: str
    expected_delivery: str
    actual_delivery: str | None = None
    duration_minutes: int = 0
    distance_km: int = 0
    delay_minutes: int = 0
    category: str = 'General'
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentRecord:
    agent_id: str
    status: str
    region: str
    today_deliveries: int = 0
    completed: int = 0
    delayed: int = 0
    failed: int = 0
    avg_duration: int = 0
    distance_km: int = 0
    frequent_areas: list[str] = field(default_factory=list)
    current_workload: int = 0
