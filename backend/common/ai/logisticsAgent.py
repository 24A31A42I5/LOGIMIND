from typing import Any, Iterable

from common.analytics.analyticsService import normalize_metrics


def analyze_business_evidence(records: Iterable[dict[str, Any]], business_type: str) -> dict[str, Any]:
	"""Translate any domain record set into common evidence for AI prompts."""
	items = list(records)
	metrics = normalize_metrics(items)
	areas = sorted({item.get('location') or item.get('area') for item in items if item.get('location') or item.get('area')})
	return {'businessType': business_type, 'recordCount': len(items), 'areas': areas, 'metrics': metrics, 'evidenceStatus': 'available' if items else 'insufficient'}
