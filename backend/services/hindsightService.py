import os
import json
from typing import Any

import httpx

from config.hindsight import is_hindsight_configured


class HindsightService:
    def __init__(self) -> None:
        self.base_url = os.getenv('HINDSIGHT_API_URL', '').rstrip('/')
        self.api_key = os.getenv('HINDSIGHT_API_KEY', '')
        self.bank_id = os.getenv('HINDSIGHT_BANK_ID', 'logimind-distributor-hub-01')

    def _bank_url(self, resource: str) -> str:
        return f'{self.base_url}/v1/default/banks/{self.bank_id}/{resource}'

    def retain_memory(self, experience: dict[str, Any]) -> dict[str, Any]:
        if not is_hindsight_configured():
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}
        try:
            response = httpx.post(
                self._bank_url('memories'),
                json={'items': [{'content': json.dumps(experience), 'context': 'logimind'}]},
                headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                timeout=10,
            )
            response.raise_for_status()
            result = response.json()
            result.setdefault('status', 'success' if result.get('success') else 'unknown')
            return result
        except Exception:
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}

    def recall_memory(self, query: str | dict[str, Any]) -> dict[str, Any]:
        if not is_hindsight_configured():
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}
        try:
            response = httpx.post(
                self._bank_url('memories/recall'),
                json={'query': json.dumps(query) if isinstance(query, dict) else query},
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
                self._bank_url('reflect'),
                json={'query': json.dumps(context)},
                headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}


hindsight_service = HindsightService()
