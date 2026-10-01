BUSINESS_TYPES = {'distributor', 'restaurant', 'raw_material', 'retail', 'service_provider'}


def validate_business_type(business_type: str) -> str:
	if business_type not in BUSINESS_TYPES:
		raise ValueError(f'Unsupported business type: {business_type}')
	return business_type
