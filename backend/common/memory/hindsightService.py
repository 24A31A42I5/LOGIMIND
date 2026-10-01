from typing import Any

from services.hindsightService import hindsight_service


def retain(experience: dict[str, Any]) -> dict[str, Any]:
	return hindsight_service.retain_memory(experience)


def recall(query: str) -> dict[str, Any]:
	return hindsight_service.recall_memory(query)


def reflect(context: dict[str, Any]) -> dict[str, Any]:
	return hindsight_service.reflect_memory(context)
