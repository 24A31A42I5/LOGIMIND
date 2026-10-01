class BusinessError(Exception):
	"""Expected domain validation or evidence error."""


class InsufficientEvidenceError(BusinessError):
	pass
