from datetime import datetime, timedelta
from typing import Any

from config.database import get_database


_fallback_records: dict[str, list[dict[str, Any]]] = {}


def expand_demo_records(seed_records: list[dict[str, Any]], days: int = 30) -> list[dict[str, Any]]:
	"""Create deterministic domain-specific demo history from the domain seed examples."""
	result = []
	start = datetime(2026, 9, 1, 9, 0)
	for day in range(days):
		for index, seed in enumerate(seed_records):
			record = dict(seed)
			base_id = record.get('order_id') or record.get('sale_id') or record.get('booking_id') or record.get('id') or f'record-{index + 1}'
			record['order_id' if 'order_id' in record else 'sale_id' if 'sale_id' in record else 'record_id'] = f'{base_id}-{day + 1:02d}'
			timestamp = start + timedelta(days=day, hours=index * 2)
			record['timestamp'] = timestamp.isoformat()
			record.setdefault('date', timestamp.date().isoformat())
			for key in ('volume', 'units', 'demand', 'sales', 'customer_density'):
				if isinstance(record.get(key), (int, float)):
					record[key] = round(record[key] * (1 + (day % 7) * 0.015), 2)
			if record.get('latitude') is None and record.get('longitude') is None:
				record['latitude'] = round(18.50 + (index * 0.012) + ((day % 5) * 0.001), 6)
				record['longitude'] = round(73.83 + (index * 0.014) + ((day % 4) * 0.001), 6)
			result.append(record)
	return result


def read_domain_records(collection_name: str, seed_records: list[dict[str, Any]], user_id: str | None = None) -> list[dict[str, Any]]:
	"""Read MongoDB records, seeding a named collection only when it is empty."""
	database = get_database()
	if database is None:
		return [*seed_records, *_fallback_records.get(collection_name, [])] if user_id is None else [*seed_records, *[record for record in _fallback_records.get(collection_name, []) if record.get('userId') == user_id]]
	collection = database[collection_name]
	query = {'userId': user_id} if user_id else {}
	if user_id and seed_records:
		synthetic_query = {'userId': user_id, 'synthetic': True}
		synthetic_count = collection.count_documents(synthetic_query)
		missing_coordinates = collection.count_documents({**synthetic_query, 'latitude': {'$exists': False}})
		if synthetic_count and (synthetic_count < len(seed_records) or missing_coordinates):
			collection.delete_many(synthetic_query)
			collection.insert_many([dict(record, userId=user_id, synthetic=True) for record in seed_records])
	if collection.count_documents(query) == 0 and seed_records:
		documents = [dict(record, userId=user_id, synthetic=True) for record in seed_records] if user_id else [dict(record, synthetic=True) for record in seed_records]
		collection.insert_many(documents)
	return [{key: value for key, value in record.items() if key != '_id'} for record in collection.find(query, {'_id': 0})]


def write_domain_records(collection_name: str, records: list[dict[str, Any]]) -> int:
	database = get_database()
	if database is None:
		_fallback_records.setdefault(collection_name, []).extend(records)
		return len(records)
	if records:
		database[collection_name].insert_many(records)
	return len(records)


def domain_records_are_persisted(collection_name: str, user_id: str | None = None) -> bool:
	database = get_database()
	query = {'userId': user_id, 'synthetic': {'$ne': True}} if user_id else {'synthetic': {'$ne': True}}
	return database is not None and database[collection_name].count_documents(query) > 0