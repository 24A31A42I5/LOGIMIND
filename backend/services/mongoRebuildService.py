from __future__ import annotations

import os
from datetime import datetime
from typing import Any

from bson import ObjectId

from config.database import get_database
from services.seedService import get_demo_store


COLLECTIONS = [
    'areas',
    'riders',
    'customers',
    'products',
    'shipments',
    'recommendations',
    'hindsight_memories',
    'interventions',
    'restaurant_orders',
    'supplier_orders',
    'retail_sales',
    'service_bookings',
]


def rebuild_linked_database() -> dict[str, Any]:
    database = get_database()
    if database is None:
        raise RuntimeError('MongoDB is not connected.')

    store = get_demo_store()
    for collection_name in COLLECTIONS:
        database.drop_collection(collection_name)

    areas = {}
    area_documents = []
    for area in store['areas']:
        area_id = ObjectId()
        areas[area['name']] = area_id
        area_documents.append({
            '_id': area_id,
            'area_code': area['name'].replace(' ', '-').upper(),
            'name': area['name'],
            'coordinates': {'lat': area['lat'], 'lng': area['lng']},
            'performance': area['performance'],
            'deliveries': area['deliveries'],
            'average_delivery_time': area['average_delivery_time'],
        })

    riders = {}
    rider_documents = []
    for agent in store['delivery_agents']:
        rider_id = ObjectId()
        riders[agent['agent_id']] = rider_id
        rider_documents.append({
            '_id': rider_id,
            'rider_code': agent['agent_id'],
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
        })

    customers = {}
    customer_documents = []
    for shipment in store['shipments']:
        customer_name = shipment['customer']
        if customer_name not in customers:
            customer_id = ObjectId()
            customers[customer_name] = customer_id
            customer_documents.append({
                '_id': customer_id,
                'customer_code': customer_name.replace(' ', '-').lower(),
                'name': customer_name,
            })

    products = {}
    product_documents = []
    for shipment in store['shipments']:
        product_name = shipment['product']
        if product_name not in products:
            product_id = ObjectId()
            products[product_name] = product_id
            product_documents.append({
                '_id': product_id,
                'name': product_name,
                'category': shipment['category'],
            })

    memory_documents = []
    memories = {}
    for memory in store['memories']:
        memory_id = ObjectId()
        memories[memory['id']] = memory_id
        memory_documents.append({
            '_id': memory_id,
            'memory_code': memory['id'],
            'bank_id': os.getenv('HINDSIGHT_BANK_ID', 'logimind-distributor-hub-01'),
            'title': memory['title'],
            'content': memory['summary'],
            'pattern': memory['pattern'],
            'outcome': memory['outcome'],
            'evidence': memory['evidence'],
            'source': 'logimind-demo',
            'created_at': memory['date'],
        })

    shipment_documents = []
    for shipment in store['shipments']:
        shipment_documents.append({
            '_id': ObjectId(),
            'shipment_id': shipment['shipment_id'],
            'area': areas[shipment['area']],
            'rider': riders[shipment['agent_id']],
            'customer': customers[shipment['customer']],
            'product': products[shipment['product']],
            'area_name': shipment['area'],
            'rider_code': shipment['agent_id'],
            'customer_name': shipment['customer'],
            'product_name': shipment['product'],
            'status': shipment['status'],
            'dispatch_time': shipment['dispatch_time'],
            'expected_delivery': shipment['expected_delivery'],
            'actual_delivery': shipment['actual_delivery'],
            'duration_minutes': shipment['duration_minutes'],
            'distance_km': shipment['distance_km'],
            'delay_minutes': shipment['delay_minutes'],
            'destination': shipment['destination'],
            'coordinates': {
                'lat': shipment['customer_lat'],
                'lng': shipment['customer_lng'],
            },
            'category': shipment['category'],
            'timestamp': shipment['timestamp'],
        })

    recommendation_memory = {'rec-001': 'mem-002', 'rec-002': 'mem-001'}
    recommendation_documents = []
    recommendations = {}
    for recommendation in store['recommendations']:
        recommendation_id = ObjectId()
        recommendations[recommendation['id']] = recommendation_id
        recommendation_documents.append({
            '_id': recommendation_id,
            'recommendation_code': recommendation['id'],
            'area': areas[recommendation['area']],
            'memory': memories[recommendation_memory[recommendation['id']]],
            'title': recommendation['title'],
            'why': recommendation['why'],
            'current_evidence': recommendation['current_evidence'],
            'historical_memory': recommendation['historical_memory'],
            'expected_impact': recommendation['expected_impact'],
            'confidence': recommendation['confidence'],
            'status': recommendation['status'],
            'created_at': datetime.utcnow(),
        })

    intervention_documents = [{
        '_id': ObjectId(),
        'intervention_code': 'int-001',
        'recommendation': recommendations['rec-001'],
        'area': areas['Area C'],
        'rider': riders['R03'],
        'action': 'Assigned an additional delivery rider',
        'before_average_minutes': 48,
        'after_average_minutes': 31,
        'outcome': 'Successful',
        'date': '2026-08-12',
        'source': 'logimind-demo',
    }]

    documents = {
        'areas': area_documents,
        'riders': rider_documents,
        'customers': customer_documents,
        'products': product_documents,
        'shipments': shipment_documents,
        'recommendations': recommendation_documents,
        'hindsight_memories': memory_documents,
        'interventions': intervention_documents,
    }
    for collection_name, collection_documents in documents.items():
        database[collection_name].insert_many(collection_documents)

    from domains.raw_material.service import SUPPLY_ORDERS
    from domains.restaurant.service import RESTAURANT_ORDERS
    from domains.retail.service import RETAIL_SALES
    from domains.service_provider.service import SERVICE_BOOKINGS
    domain_documents = {
        'restaurant_orders': RESTAURANT_ORDERS,
        'supplier_orders': SUPPLY_ORDERS,
        'retail_sales': RETAIL_SALES,
        'service_bookings': SERVICE_BOOKINGS,
    }
    for collection_name, records in domain_documents.items():
        database[collection_name].insert_many([dict(record, userId='demo-user', businessType=collection_name.split('_')[0], synthetic=True) for record in records])

    indexes = {
        'areas': ['area_code'],
        'riders': ['rider_code'],
        'customers': ['customer_code'],
        'products': ['name'],
        'shipments': ['shipment_id', 'area', 'rider', 'customer', 'product'],
        'recommendations': ['recommendation_code', 'area', 'memory'],
        'hindsight_memories': ['memory_code'],
        'interventions': ['intervention_code', 'recommendation', 'area', 'rider'],
        'restaurant_orders': ['userId', 'location'],
        'supplier_orders': ['userId', 'location'],
        'retail_sales': ['userId', 'location'],
        'service_bookings': ['userId', 'location'],
    }
    for collection_name, fields in indexes.items():
        for field in fields:
            database[collection_name].create_index(field, unique=field.endswith('_code'))

    return {
        'status': 'rebuilt',
        'database': database.name,
        'collections': {name: len(items) for name, items in documents.items()},
        'reference_fields': {
            'shipments': ['area', 'rider', 'customer', 'product'],
            'recommendations': ['area', 'memory'],
            'interventions': ['recommendation', 'area', 'rider'],
        },
    }
