import asyncio
import time
from functools import lru_cache
from typing import Dict, Any

import httpx
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from jose.utils import base64url_decode

from app.core.settings import get_settings

bearer = HTTPBearer(auto_error=True)


def _normalize_issuer(iss: str) -> str:
    return iss if iss.endswith("/") else iss + "/"


class JWKSCache:
    def __init__(self, url: str, ttl_seconds: int = 600):
        self.url = url
        self.ttl = ttl_seconds
        self._keys: list[dict] | None = None
        self._exp: float = 0.0
        self._lock = asyncio.Lock()

    async def get(self, force_refresh: bool = False) -> list[dict]:
        async with self._lock:
            now = time.time()
            if force_refresh or self._keys is None or now >= self._exp:
                async with httpx.AsyncClient(timeout=5.0) as c:
                    r = await c.get(self.url)
                    r.raise_for_status()
                    self._keys = r.json()["keys"]
                    self._exp = now + self.ttl
            return self._keys


def _jwk_to_public_key(jwk: Dict[str, Any]):
    e = int.from_bytes(base64url_decode(jwk["e"].encode()), "big")
    n = int.from_bytes(base64url_decode(jwk["n"].encode()), "big")
    return rsa.RSAPublicNumbers(e, n).public_key()


class JWTVerifier:
    def __init__(self, issuer: str, audience: str):
        self.issuer = _normalize_issuer(issuer)
        self.audience = audience
        self.jwks = JWKSCache(f"{self.issuer}.well-known/jwks.json")

    async def _select_key(self, token: str, refresh=False):
        unverified = jwt.get_unverified_header(token)
        kid = unverified.get("kid")
        keys = await self.jwks.get(force_refresh=refresh)
        return next((k for k in keys if k.get("kid") == kid), None)

    async def verify_token(self, token: str) -> dict:
        key_jwk = await self._select_key(token)
        if not key_jwk:
            key_jwk = await self._select_key(token, refresh=True)
            if not key_jwk:
                raise HTTPException(status_code=401, detail="Unknown key id (kid)")
        public_key = _jwk_to_public_key(key_jwk)
        opts = {
            "verify_at_hash": False,
            "leeway": 30,
        }  # python-jose: leeway goes inside options
        try:
            return jwt.decode(
                token,
                key=public_key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
                options=opts,
            )
        except jwt.JWTError:
            # retry once in case of rotation
            key_jwk = await self._select_key(token, refresh=True)
            if not key_jwk:
                raise HTTPException(status_code=401, detail="Invalid token")
            public_key = _jwk_to_public_key(key_jwk)
            return jwt.decode(
                token,
                key=public_key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
                options=opts,
            )


@lru_cache(maxsize=1)
def get_jwt_verifier() -> JWTVerifier:
    s = get_settings()
    return JWTVerifier(issuer=s.issuer, audience=s.auth0_audience)


async def verify_jwt(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    verifier: JWTVerifier = Depends(get_jwt_verifier),
) -> dict:
    return await verifier.verify_token(creds.credentials)


def current_user_id(claims: dict = Depends(verify_jwt)) -> str:
    return claims["sub"]


def require_scope(scope: str):
    async def _dep(claims=Depends(verify_jwt)):
        scopes = set((claims.get("scope") or "").split())
        if scope not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient scope"
            )
        return claims

    return _dep
