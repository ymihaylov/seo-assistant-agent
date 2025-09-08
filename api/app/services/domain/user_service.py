from fastapi import HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.models.user import User


class UserService:
    def __init__(self, db: OrmSession):
        self.db = db

    def ensure_user(self, claims: dict) -> User:
        sub = claims.get("sub")
        email = claims.get("email")
        name = claims.get("name") or claims.get("nickname")

        if not sub and not email:
            raise HTTPException(status_code=401, detail="Invalid token (no sub/email)")

        user = self._find_existing_user(sub, email)

        if not user:
            user = self._create_user(sub, email, name)

        return user

    def _find_existing_user(self, sub: str, email: str) -> User:
        user = None

        if sub:
            user = self.db.query(User).filter(User.auth_sub == sub).one_or_none()

        if not user and email:
            user = self.db.query(User).filter(User.email == email).one_or_none()

        return user

    def _create_user(self, sub: str, email: str, name: str) -> User:
        user = User(auth_sub=sub, email=email, display_name=name)
        self.db.add(user)
        self.db.flush()

        return user
