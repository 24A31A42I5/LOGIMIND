from typing import Any


def require_non_empty(value: Any, field: str) -> Any:
	if value is None or value == '' or value == []:
		raise ValueError(f'{field} is required')
	return value


def validate_coordinates(latitude: float, longitude: float) -> None:
	if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
		raise ValueError('Location coordinates are invalid')
