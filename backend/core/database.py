import os
from typing import Any

from pymongo import MongoClient


_client: MongoClient | None = None
_fallback_profiles: dict[str, dict[str, Any]] = {}
_fallback_users: dict[str, dict[str, Any]] = {}


def get_profiles_collection():
	"""Use MongoDB when configured, while keeping local demo development runnable."""
	global _client
	uri = os.getenv('MONGODB_URI') or os.getenv('MONGO_URI')
	database_name = os.getenv('MONGODB_DATABASE', 'logimind')
	if not uri:
		return None
	if _client is None:
		_client = MongoClient(uri, serverSelectionTimeoutMS=1500)
	return _client[database_name]['business_profiles']


def get_fallback_profile(user_id: str) -> dict[str, Any] | None:
	return _fallback_profiles.get(user_id)


def save_fallback_profile(profile: dict[str, Any]) -> dict[str, Any]:
	_fallback_profiles[profile['userId']] = profile
	return profile


def get_users_collection():
	collection = get_profiles_collection()
	return collection.database['users'] if collection is not None else None


def get_fallback_user(user_id: str) -> dict[str, Any] | None:
	return _fallback_users.get(user_id)


def save_fallback_user(user: dict[str, Any]) -> dict[str, Any]:
	_fallback_users[user['userId']] = user
	return user
