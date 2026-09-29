import os
from typing import Any

import httpx

from config.hindsight import is_hindsight_configured


class HindsightService:
    def __init__(self) -> None:
        self.base_url = os.getenv('HINDSIGHT_API_URL', '').rstrip('/')
        self.api_key = os.getenv('HINDSIGHT_API_KEY', '')
        self.bank_id = os.getenv('HINDSIGHT_BANK_ID', 'logimind-distributor-hub-01')

    def retain_memory(self, experience: dict[str, Any]) -> dict[str, Any]:
        if not is_hindsight_configured():
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}
        try:
            response = httpx.post(
                f'{self.base_url}/retain',
                json={'bank_id': self.bank_id, 'experience': experience},
                headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}

    def recall_memory(self, query: str) -> dict[str, Any]:
        if not is_hindsight_configured():
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}
        try:
            response = httpx.post(
                f'{self.base_url}/recall',
                json={'bank_id': self.bank_id, 'query': query},
                headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}

    def reflect_memory(self, context: dict[str, Any]) -> dict[str, Any]:
        if not is_hindsight_configured():
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}
        try:
            response = httpx.post(
                f'{self.base_url}/reflect',
                json={'bank_id': self.bank_id, 'context': context},
                headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}


hindsight_service = HindsightService()
