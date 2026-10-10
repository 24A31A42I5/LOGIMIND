from typing import Any

from services.llmService import llm_service


def generate_business_recommendation(facts: dict[str, Any]) -> dict[str, Any]:
	"""Use the configured LLM without fabricating a recommendation."""
	llm_result = llm_service.generate_recommendation(facts)
	if llm_result:
		return {'source': 'llm', **llm_result}
	return {}
