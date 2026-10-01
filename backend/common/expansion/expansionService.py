from typing import Any

from common.memory.hindsightService import recall
from common.expansion.locationScoring import score_candidate


FACTORS = {
	'distributor': ['demand', 'customer_density', 'coverage_gap', 'operational_feasibility'],
	'restaurant': ['demand', 'customer_density', 'foot_traffic', 'coverage_gap'],
	'raw_material': ['demand', 'customer_density', 'coverage_gap', 'operational_feasibility'],
	'retail': ['demand', 'customer_density', 'purchasing_potential', 'coverage_gap'],
	'service_provider': ['demand', 'customer_density', 'coverage_gap', 'operational_feasibility'],
}


def get_expansion_analysis(business_type: str, records: list[dict[str, Any]] | None = None, user_id: str | None = None) -> dict[str, Any]:
	if business_type not in FACTORS:
		raise ValueError('Invalid business type for expansion analysis')
	if records is None:
		from domains.distributor.service import list_operations
		from domains.raw_material.service import list_supplies
		from domains.restaurant.service import list_orders
		from domains.retail.service import list_sales
		from domains.service_provider.service import list_bookings
		record_sources = {'distributor': list_operations, 'restaurant': list_orders, 'raw_material': list_supplies, 'retail': list_sales, 'service_provider': list_bookings}
		records = record_sources[business_type](user_id)
	if len(records) < 2:
		return {'businessType': business_type, 'sufficientEvidence': False, 'synthetic': True, 'candidates': [], 'historicalMemory': {'available': False, 'message': 'Insufficient current data for a reliable expansion assessment.'}}
	grouped = {}
	for record in records:
		location = record.get('location', 'Unknown')
		grouped.setdefault(location, []).append(record)
	candidates = []
	for name, items in grouped.items():
		candidate = {'name': name, 'historical_evidence': 'Derived from current domain records.'}
		for factor in set(FACTORS[business_type] + ['coverage_gap']):
			values = [float(item.get(factor, 0)) for item in items]
			candidate[factor] = round(sum(values) / len(values), 2) if values else 0
		candidates.append(candidate)
	factors = FACTORS[business_type]
	historical = recall(f'{business_type} expansion demand and coverage performance')
	historical_available = historical.get('status') not in {'fallback', 'error'} and bool(historical.get('memories') or historical.get('results') or historical.get('data'))
	historical_text = 'Relevant Hindsight evidence was recalled.' if historical_available else 'Historical memory currently unavailable.'
	scored = [score_candidate(candidate, factors) for candidate in candidates]
	for candidate in scored:
		candidate['historical_evidence'] = historical_text
		candidate['reason'] = 'Strong business-specific demand with a meaningful current coverage gap.'
	return {'businessType': business_type, 'sufficientEvidence': True, 'factors': factors, 'synthetic': True, 'currentRecordCount': len(records), 'historicalMemory': {'available': historical_available, 'message': historical_text}, 'candidates': scored}
