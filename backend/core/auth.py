import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.database import get_users_collection, get_fallback_user, save_fallback_user


def normalize_user_id(email: str) -> str:
	return hashlib.sha256(email.strip().lower().encode('utf-8')).hexdigest()[:12]


def _hash_password(password: str, salt: bytes | None = None) -> str:
	salt = salt or secrets.token_bytes(16)
	digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 120_000)
	return f'{base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}'


def _check_password(password: str, encoded: str) -> bool:
	try:
		salt_text, digest_text = encoded.split('$', 1)
		salt = base64.urlsafe_b64decode(salt_text.encode())
		expected = base64.urlsafe_b64decode(digest_text.encode())
		actual = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 120_000)
		return hmac.compare_digest(actual, expected)
	except (ValueError, TypeError):
		return False


def _secret() -> bytes:
	return os.getenv('LOGIMIND_AUTH_SECRET', 'development-only-change-this-secret').encode()


def _token(user_id: str) -> str:
	payload = {'sub': user_id, 'exp': int((datetime.now(timezone.utc) + timedelta(hours=12)).timestamp())}
	body = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
	signature = hmac.new(_secret(), body.encode(), hashlib.sha256).hexdigest()
	return f'{body}.{signature}'


def _user_document(email: str, password: str) -> dict[str, str]:
	return {'userId': normalize_user_id(email), 'email': email.strip().lower(), 'passwordHash': _hash_password(password)}


def authenticate(email: str, password: str) -> dict[str, str] | None:
	user_id = normalize_user_id(email)
	collection = get_users_collection()
	user = collection.find_one({'userId': user_id}, {'_id': 0}) if collection is not None else get_fallback_user(user_id)
	if user is None:
		user = _user_document(email, password)
		if collection is not None:
			collection.insert_one(user)
		else:
			save_fallback_user(user)
	elif not _check_password(password, user.get('passwordHash', '')):
		return None
	return {'userId': user['userId'], 'email': user['email'], 'access_token': _token(user['userId']), 'token_type': 'bearer'}


def build_user(email: str) -> dict[str, str]:
	return authenticate(email, 'demo123') or {'userId': normalize_user_id(email), 'email': email.strip().lower()}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> dict[str, str]:
	try:
		body, signature = credentials.credentials.split('.', 1)
		expected = hmac.new(_secret(), body.encode(), hashlib.sha256).hexdigest()
		if not hmac.compare_digest(signature, expected):
			raise ValueError
		payload = json.loads(base64.urlsafe_b64decode(body + '=' * (-len(body) % 4)))
		if int(payload['exp']) < int(datetime.now(timezone.utc).timestamp()):
			raise ValueError
		return {'userId': payload['sub']}
	except (ValueError, KeyError, TypeError, json.JSONDecodeError):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired access token')
