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
	candidates = [
		{'name': 'Area C', 'latitude': 18.509, 'longitude': 73.845, 'demand': 86, 'customer_density': 82, 'coverage_gap': 88, 'operational_feasibility': 74, 'foot_traffic': 84, 'purchasing_potential': 79, 'competition': 'Medium', 'historical_evidence': 'Similar operating areas previously showed strong performance.'},
		{'name': 'Area D', 'latitude': 18.548, 'longitude': 73.884, 'demand': 68, 'customer_density': 71, 'coverage_gap': 76, 'operational_feasibility': 62, 'foot_traffic': 65, 'purchasing_potential': 72, 'competition': 'Low', 'historical_evidence': 'Historical evidence is limited for this area.'},
	]
	factors = FACTORS[business_type]
	historical = recall(f'{business_type} expansion demand and coverage performance')
	historical_available = historical.get('status') not in {'fallback', 'error'} and bool(historical.get('memories') or historical.get('results') or historical.get('data'))
	historical_text = 'Relevant Hindsight evidence was recalled.' if historical_available else 'Historical memory currently unavailable.'
	scored = [score_candidate(candidate, factors) for candidate in candidates]
	for candidate in scored:
		candidate['historical_evidence'] = historical_text
		candidate['reason'] = 'Strong business-specific demand with a meaningful current coverage gap.'
	return {'businessType': business_type, 'sufficientEvidence': True, 'factors': factors, 'synthetic': True, 'currentRecordCount': len(records), 'historicalMemory': {'available': historical_available, 'message': historical_text}, 'candidates': scored}
