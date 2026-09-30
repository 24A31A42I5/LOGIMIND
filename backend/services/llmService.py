import json
import os
from typing import Any

import httpx

from config.llm import get_llm_config


class LLMService:
    endpoint = 'https://api.groq.com/openai/v1/chat/completions'

    def generate_recommendation(self, facts: dict[str, Any]) -> dict[str, Any] | None:
        config = get_llm_config()
        if config['provider'] != 'groq' or not config['api_key']:
            return None

        try:
            response = httpx.post(
                self.endpoint,
                json={
                    'model': config['model'],
                    'messages': [
                        {
                            'role': 'system',
                            'content': (
                                'You are a logistics operations analyst. Return only a JSON object with '
                                    'the keys title, why, expected_impact, and confidence. Confidence must be '
                                    'an integer from 0 to 100. Use only the supplied facts.'
                            ),
                        },
                        {'role': 'user', 'content': json.dumps(facts)},
                    ],
                    'temperature': 0.2,
                    'max_tokens': 512,
                },
                headers={
                    'Authorization': f"Bearer {config['api_key']}",
                    'Content-Type': 'application/json',
                },
                timeout=30,
            )
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content'].strip()
            if content.startswith('```'):
                content = content.removeprefix('```json').removesuffix('```').strip()
            result = json.loads(content)
            if not isinstance(result, dict):
                return None

            recommendation = {
                key: result[key]
                for key in ('title', 'why', 'expected_impact')
                if isinstance(result.get(key), str) and result[key].strip()
            }
            confidence = result.get('confidence')
            if isinstance(confidence, (int, float)):
                recommendation['confidence'] = max(0, min(100, round(confidence)))
            required = {'title', 'why', 'expected_impact', 'confidence'}
            return recommendation if required.issubset(recommendation) else None
        except (KeyError, TypeError, ValueError, httpx.HTTPError, json.JSONDecodeError):
            return None


llm_service = LLMService()
