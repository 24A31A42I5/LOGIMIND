from typing import Any

from services.llmService import llm_service


def generate_business_recommendation(facts: dict[str, Any]) -> dict[str, Any]:
	"""Use the configured LLM when available and retain an honest fallback."""
	llm_result = llm_service.generate_recommendation(facts)
	if llm_result:
		return {'source': 'llm', **llm_result}
	return {
		'source': 'rule_based',
		'title': 'Review the highest-evidence expansion candidate',
		'why': 'Current evidence is available, but no external AI response was returned.',
		'expected_impact': 'Improve coverage only after validating operating feasibility.',
		'confidence': 45,
	}
