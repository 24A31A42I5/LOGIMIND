from typing import Any


def score_candidate(candidate: dict[str, Any], factors: list[str]) -> dict[str, Any]:
	values = [float(candidate[factor]) for factor in factors if isinstance(candidate.get(factor), (int, float))]
	score = round(sum(values) / len(values), 2) if values else None
	category = 'High expansion potential' if score is not None and score >= 75 else 'Medium expansion potential' if score is not None and score >= 55 else 'Insufficient evidence'
	return {**candidate, 'score': score, 'category': category}
