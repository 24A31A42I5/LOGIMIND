from typing import Any


def score_candidate(candidate: dict[str, Any], factors: list[str]) -> dict[str, Any]:
	values = [float(candidate.get(factor, 0)) for factor in factors]
	score = round(sum(values) / len(values)) if values else 0
	category = 'High expansion potential' if score >= 75 else 'Medium expansion potential' if score >= 55 else 'Insufficient evidence'
	return {**candidate, 'score': score, 'category': category}
