from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any


def _iso(ts: datetime) -> str:
    return ts.isoformat()


def build_demo_data() -> dict[str, Any]:
    start = datetime(2026, 8, 1, 8, 0)
    shipments = []
    agents = [
        {'agent_id': 'R03', 'status': 'Out for Delivery', 'region': 'Area C', 'today_deliveries': 12, 'completed': 10, 'delayed': 1, 'failed': 1, 'avg_duration': 39, 'distance_km': 92, 'frequent_areas': ['Area C', 'Area A'], 'current_workload': 6},
        {'agent_id': 'R12', 'status': 'Assigned', 'region': 'Area B', 'today_deliveries': 9, 'completed': 7, 'delayed': 1, 'failed': 1, 'avg_duration': 44, 'distance_km': 80, 'frequent_areas': ['Area B', 'Area D'], 'current_workload': 5},
        {'agent_id': 'L08', 'status': 'Out for Delivery', 'region': 'Area A', 'today_deliveries': 11, 'completed': 9, 'delayed': 1, 'failed': 1, 'avg_duration': 36, 'distance_km': 75, 'frequent_areas': ['Area A', 'Area C'], 'current_workload': 4},
        {'agent_id': 'H21', 'status': 'Delayed', 'region': 'Area C', 'today_deliveries': 8, 'completed': 5, 'delayed': 2, 'failed': 1, 'avg_duration': 58, 'distance_km': 111, 'frequent_areas': ['Area C'], 'current_workload': 7},
        {'agent_id': 'Q14', 'status': 'Delivered', 'region': 'Area D', 'today_deliveries': 7, 'completed': 6, 'delayed': 0, 'failed': 1, 'avg_duration': 32, 'distance_km': 65, 'frequent_areas': ['Area D', 'Area B'], 'current_workload': 3},
        {'agent_id': 'N41', 'status': 'Assigned', 'region': 'Area A', 'today_deliveries': 10, 'completed': 8, 'delayed': 1, 'failed': 1, 'avg_duration': 41, 'distance_km': 87, 'frequent_areas': ['Area A'], 'current_workload': 5},
    ]

    areas = {
        'Area A': {'lat': 18.5204, 'lng': 73.8567, 'delay_rate': 0.12, 'density': 210},
        'Area B': {'lat': 18.5304, 'lng': 73.8707, 'delay_rate': 0.17, 'density': 260},
        'Area C': {'lat': 18.509, 'lng': 73.845, 'delay_rate': 0.26, 'density': 330},
        'Area D': {'lat': 18.548, 'lng': 73.884, 'delay_rate': 0.14, 'density': 200},
    }

    area_sequence = ['Area A', 'Area B', 'Area C', 'Area D']

    for day_offset in range(30):
        current_day = start + timedelta(days=day_offset)
        for index in range(30):
            area = area_sequence[index % len(area_sequence)]
            if index % 5 == 0:
                area = 'Area C'
            dispatch = current_day + timedelta(hours=8 + (index % 9), minutes=(index * 7) % 60)
            if area == 'Area C' and dispatch.hour in {17, 18, 19, 20}:
                duration = 52 + (index % 6)
                delay_flag = True
                status = 'Delayed' if index % 3 == 0 else 'Out for Delivery'
            elif area == 'Area D' and index % 7 == 0:
                duration = 62 + (index % 9)
                delay_flag = True
                status = 'Failed' if index % 5 == 0 else 'Delayed'
            else:
                duration = 28 + (index % 12)
                delay_flag = False
                status = 'Delivered' if dispatch.hour > 14 else 'Out for Delivery'

            if status == 'Delivered':
                actual = dispatch + timedelta(minutes=duration)
            else:
                actual = None

            shipment = {
                'shipment_id': f'LOG-{day_offset + 1:02d}-{index + 1:03d}',
                'product': ['Fresh Produce', 'Pharma', 'Consumer Goods', 'Equipment', 'Household Essentials'][index % 5],
                'customer': f'Customer {index + 1:03d}',
                'destination': f'{area} Lane {index % 8 + 1}',
                'area': area,
                'agent_id': agents[index % len(agents)]['agent_id'],
                'status': status,
                'dispatch_time': _iso(dispatch),
                'expected_delivery': _iso(dispatch + timedelta(minutes=45 + (index % 10) * 6)),
                'actual_delivery': _iso(actual) if actual else None,
                'duration_minutes': duration,
                'distance_km': 12 + (index % 8) * 4 + (8 if area == 'Area C' else 0),
                'delay_minutes': 15 if delay_flag else 0,
                'customer_lat': areas[area]['lat'] + (index % 3) * 0.003,
                'customer_lng': areas[area]['lng'] + (index % 4) * 0.004,
                'category': ['Food', 'Health', 'Retail', 'Industrial', 'Home'][index % 5],
                'day_index': day_offset + 1,
                'timestamp': _iso(dispatch),
            }
            shipments.append(shipment)

    memories = [
        {'id': 'mem-001', 'date': '2026-08-05', 'title': 'Area C evening delays detected', 'summary': 'Area C saw elevated delivery times during the 6 PM to 8 PM peak window.', 'pattern': 'Evening bottleneck', 'outcome': 'Intervention required', 'evidence': ['Average delivery time: 47 min', 'Delay rate: 21%', 'Peak period: 6 PM – 8 PM']},
        {'id': 'mem-002', 'date': '2026-08-12', 'title': 'Two-agent intervention improved delivery time', 'summary': 'Assigning an additional rider reduced Area C delivery duration from 48 minutes to 31 minutes.', 'pattern': 'Successful intervention', 'outcome': 'Improved performance', 'evidence': ['Before: 48 min', 'After: 31 min', 'Outcome: Successful']},
        {'id': 'mem-003', 'date': '2026-08-20', 'title': 'Recurring Route Congestion in Area C', 'summary': 'Repeated evening delays in Area C match earlier patterns and signal recurring route congestion.', 'pattern': 'Recurring operational pattern', 'outcome': 'Repeat intervention recommended', 'evidence': ['Historical memory: Sept 12 and Sept 14', 'Route density remained high', 'Late-afternoon surcharge risk']},
    ]

    recommendations = [
        {'id': 'rec-001', 'title': 'Assign an additional delivery agent to Area C between 6 PM and 8 PM', 'why': 'Area C repeatedly experiences evening delays and route congestion.', 'current_evidence': '47 min average delivery duration today, 21% delay rate, and a clear 6 PM to 8 PM spike.', 'historical_memory': 'A similar two-agent intervention on Aug 12 reduced average delivery duration from 48 min to 31 min.', 'expected_impact': 'Potential reduction of 15-20 minutes in evening deliveries.', 'confidence': 86, 'status': 'Open', 'area': 'Area C'},
        {'id': 'rec-002', 'title': 'Advance dispatch timing for Area C orders', 'why': 'Evening backups are created by dense late-day route clustering.', 'current_evidence': 'Delivery density is concentrated between 5:30 PM and 7:30 PM.', 'historical_memory': 'Earlier intervention on Aug 5 also improved service when dispatch was moved earlier.', 'expected_impact': 'Reduce burst load at the peak evening period.', 'confidence': 78, 'status': 'Open', 'area': 'Area C'},
    ]

    demo = {
        'shipments': shipments,
        'delivery_agents': agents,
        'memories': memories,
        'recommendations': recommendations,
        'areas': [
            {'name': 'Area A', 'lat': 18.5204, 'lng': 73.8567, 'performance': 'Healthy', 'deliveries': 284, 'average_delivery_time': 39},
            {'name': 'Area B', 'lat': 18.5304, 'lng': 73.8707, 'performance': 'Stable', 'deliveries': 261, 'average_delivery_time': 41},
            {'name': 'Area C', 'lat': 18.509, 'lng': 73.845, 'performance': 'Hotspot', 'deliveries': 344, 'average_delivery_time': 47},
            {'name': 'Area D', 'lat': 18.548, 'lng': 73.884, 'performance': 'Problem', 'deliveries': 198, 'average_delivery_time': 53},
        ],
    }
    return demo


_demo_store: dict[str, Any] | None = None


def get_demo_store() -> dict[str, Any]:
    global _demo_store
    if _demo_store is None:
        _demo_store = build_demo_data()
    return _demo_store


def reset_demo_store() -> dict[str, Any]:
    global _demo_store
    _demo_store = build_demo_data()
    return _demo_store
