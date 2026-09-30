from __future__ import annotations

import os
import re
from typing import Any

from config.database import get_database
from services.seedService import get_demo_store


def _area_id(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def _upsert_documents(collection: Any, key: str, documents: list[dict[str, Any]]) -> int:
    for document in documents:
        collection.update_one({key: document[key]}, {'$set': document}, upsert=True)
    return len(documents)


def seed_linked_database() -> dict[str, Any]:
    database = get_database()
    if database is None:
        raise RuntimeError('MongoDB is not connected.')

    store = get_demo_store()
    areas = [
        {
            'area_id': _area_id(area['name']),
            'name': area['name'],
            'lat': area['lat'],
            'lng': area['lng'],
            'performance': area['performance'],
            'deliveries': area['deliveries'],
            'average_delivery_time': area['average_delivery_time'],
        }
        for area in store['areas']
    ]
    area_by_name = {area['name']: area['area_id'] for area in areas}

    riders = []
    rider_by_id = {}
    for agent in store['delivery_agents']:
        rider = {
            'rider_id': agent['agent_id'],
            'name': agent['agent_id'],
            'status': agent['status'],
            'region': agent['region'],
            'vehicle_type': 'delivery-vehicle',
            'today_deliveries': agent['today_deliveries'],
            'completed': agent['completed'],
            'delayed': agent['delayed'],
            'failed': agent['failed'],
            'avg_duration': agent['avg_duration'],
            'distance_km': agent['distance_km'],
            'frequent_areas': agent['frequent_areas'],
            'current_workload': agent['current_workload'],
        }
        riders.append(rider)
        rider_by_id[rider['rider_id']] = rider

    shipments = []
    for shipment in store['shipments']:
        linked_shipment = dict(shipment)
        linked_shipment.update({
            'area_id': area_by_name[shipment['area']],
            'area_name': shipment['area'],
            'rider_id': shipment['agent_id'],
            'rider_name': rider_by_id[shipment['agent_id']]['name'],
        })
        shipments.append(linked_shipment)

    memory_id_by_recommendation = {'rec-001': 'mem-002', 'rec-002': 'mem-001'}
    recommendations = []
    for recommendation in store['recommendations']:
        linked_recommendation = dict(recommendation)
        linked_recommendation.update({
            'recommendation_id': recommendation['id'],
            'area_id': area_by_name[recommendation['area']],
            'memory_id': memory_id_by_recommendation.get(recommendation['id']),
        })
        recommendations.append(linked_recommendation)

    memories = []
    for memory in store['memories']:
        linked_memory = dict(memory)
        linked_memory.update({
            'memory_id': memory['id'],
            'bank_id': os.getenv('HINDSIGHT_BANK_ID', 'logimind-distributor-hub-01'),
            'source': 'logimind-demo',
            'tags': [memory['pattern']],
        })
        memories.append(linked_memory)

    interventions = [
        {
            'intervention_id': 'int-001',
            'recommendation_id': 'rec-001',
            'area_id': area_by_name['Area C'],
            'rider_id': 'R03',
            'action': 'Assigned an additional delivery rider',
            'before_average_minutes': 48,
            'after_average_minutes': 31,
            'outcome': 'Successful',
            'date': '2026-08-12',
            'source': 'logimind-demo',
        }
    ]
    for index, intervention in enumerate(store.get('interventions', []), start=2):
        linked_intervention = dict(intervention)
        linked_intervention.update({
            'intervention_id': f'int-{index:03d}',
            'recommendation_id': intervention.get('recommendation_id', 'rec-001'),
            'area_id': area_by_name.get(intervention.get('area', 'Area C'), 'area-c'),
            'source': 'logimind-demo',
        })
        interventions.append(linked_intervention)

    collections = {
        'areas': ('area_id', areas),
        'riders': ('rider_id', riders),
        'shipments': ('shipment_id', shipments),
        'recommendations': ('recommendation_id', recommendations),
        'hindsight_memories': ('memory_id', memories),
        'interventions': ('intervention_id', interventions),
    }
    counts = {}
    for name, (key, documents) in collections.items():
        counts[name] = _upsert_documents(database[name], key, documents)

    indexes = {
        'areas': ['area_id'],
        'riders': ['rider_id'],
        'shipments': ['shipment_id', 'area_id', 'rider_id'],
        'recommendations': ['recommendation_id', 'area_id', 'memory_id'],
        'hindsight_memories': ['memory_id', 'bank_id'],
        'interventions': ['intervention_id', 'recommendation_id', 'area_id'],
    }
    for collection_name, fields in indexes.items():
        existing_indexes = database[collection_name].index_information()
        for field in fields:
            has_field_index = any(
                index.get('key') == [(field, 1)]
                for index in existing_indexes.values()
            )
            if has_field_index:
                continue
            unique = (
                (collection_name == 'areas' and field == 'area_id')
                or (collection_name == 'riders' and field == 'rider_id')
                or (collection_name == 'shipments' and field == 'shipment_id')
                or (collection_name == 'recommendations' and field == 'recommendation_id')
                or (collection_name == 'hindsight_memories' and field == 'memory_id')
                or (collection_name == 'interventions' and field == 'intervention_id')
            )
            database[collection_name].create_index(field, unique=unique)

    return {'status': 'seeded', 'database': database.name, 'counts': counts}
