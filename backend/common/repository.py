from typing import Any

from config.database import get_database


def read_domain_records(collection_name: str, seed_records: list[dict[str, Any]], user_id: str | None = None) -> list[dict[str, Any]]:
	"""Read MongoDB records, seeding a named collection only when it is empty."""
	database = get_database()
	if database is None:
		return seed_records
	collection = database[collection_name]
	query = {'userId': user_id} if user_id else {}
	if collection.count_documents(query) == 0 and seed_records:
		documents = [dict(record, userId=user_id, synthetic=True) for record in seed_records] if user_id else [dict(record, synthetic=True) for record in seed_records]
		collection.insert_many(documents)
	return [{key: value for key, value in record.items() if key != '_id'} for record in collection.find(query, {'_id': 0})]


def domain_records_are_persisted(collection_name: str, user_id: str | None = None) -> bool:
	database = get_database()
	query = {'userId': user_id, 'synthetic': {'$ne': True}} if user_id else {'synthetic': {'$ne': True}}
	return database is not None and database[collection_name].count_documents(query) > 0