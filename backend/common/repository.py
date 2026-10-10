from typing import Any

from config.database import get_database


class OperationalDataUnavailable(RuntimeError):
	"""Raised when MongoDB cannot provide authoritative operational records."""


def read_domain_records(collection_name: str, user_id: str) -> list[dict[str, Any]]:
	"""Read tenant-scoped operational records from MongoDB only.

	Seed files and in-memory fallbacks are intentionally not part of this path:
	an empty collection is valid evidence that no records have been imported yet.
	"""
	database = get_database()
	if database is None:
		raise OperationalDataUnavailable('MongoDB is unavailable')
	collection = database[collection_name]
	return list(collection.find({'userId': user_id}, {'_id': 0}))


def write_domain_records(collection_name: str, records: list[dict[str, Any]]) -> int:
	database = get_database()
	if database is None:
		raise OperationalDataUnavailable('MongoDB is unavailable; records were not imported')
	if records:
		database[collection_name].insert_many(records)
	return len(records)


def update_domain_record(
	collection_name: str,
	filter_query: dict[str, Any],
	update: dict[str, Any],
) -> bool:
	"""Update one tenant-scoped operational record in MongoDB."""
	database = get_database()
	if database is None:
		raise OperationalDataUnavailable('MongoDB is unavailable')
	result = database[collection_name].update_one(filter_query, {'$set': update})
	return result.matched_count > 0


def domain_records_are_persisted(collection_name: str, user_id: str | None = None) -> bool:
	if not user_id:
		return False
	database = get_database()
	return database is not None and database[collection_name].count_documents({'userId': user_id}) > 0