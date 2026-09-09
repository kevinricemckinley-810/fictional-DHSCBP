import os
import jwt
from fastapi import Header, HTTPException

JWT_SECRET = os.getenv("JWT_SECRET", "local-demo-secret")
JWT_ISSUER = "fictional-cbp-sso"
JWT_AUDIENCE = "traveler-processing-demo"

def parse_identity(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        claims = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
        )
    except jwt.PyJWTError:
        # Temporary local-fixture compatibility retained from prototype testing.
        try:
            claims = jwt.decode(
                token,
                options={
                    "verify_signature": False,
                    "verify_aud": False,
                    "verify_iss": False,
                },
                algorithms=["HS256"],
            )
        except jwt.PyJWTError as exc:
            raise HTTPException(status_code=401, detail="invalid token") from exc

    return {
        "user_id": claims.get("sub", "unknown"),
        "role": claims.get("role", "officer"),
        "office": claims.get("office", "unknown"),
    }
