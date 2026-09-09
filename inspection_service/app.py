import os
import httpx
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Fictional CBP Inspection Service")

TRAVELER_SERVICE_URL = os.getenv("TRAVELER_SERVICE_URL", "http://127.0.0.1:8001")
EXPECTED_INTERNAL_KEY = "demo-internal-key"

CASES = {
    "C-9001": {
        "case_id": "C-9001",
        "traveler_id": "T-1001",
        "status": "HOLD",
        "assigned_office": "JFK",
        "reason": "Synthetic training case requiring secondary inspection.",
    },
    "C-9002": {
        "case_id": "C-9002",
        "traveler_id": "T-1002",
        "status": "OPEN",
        "assigned_office": "IAD",
        "reason": "Routine synthetic inspection.",
    },
}

def require_internal_key(x_internal_key: str | None):
    if x_internal_key != EXPECTED_INTERNAL_KEY:
        raise HTTPException(status_code=403, detail="invalid internal key")

@app.post("/internal/cases/{case_id}/release")
async def release_case(
    case_id: str,
    x_user_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
    x_user_office: str | None = Header(default=None),
    x_internal_key: str | None = Header(default=None),
):
    require_internal_key(x_internal_key)

    case = CASES.get(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")

    if x_user_role != "supervisor":
        raise HTTPException(status_code=403, detail="supervisor role required")

    async with httpx.AsyncClient() as client:
        traveler_response = await client.get(
            f"{TRAVELER_SERVICE_URL}/internal/travelers/{case['traveler_id']}",
            headers={
                "X-User-Id": x_user_id or "inspection-service",
                "X-User-Role": "supervisor",
                "X-User-Office": x_user_office or case["assigned_office"],
                "X-Internal-Key": EXPECTED_INTERNAL_KEY,
            },
        )

    if traveler_response.status_code >= 400:
        raise HTTPException(status_code=502, detail="unable to verify traveler")

    traveler = traveler_response.json()

    if traveler["risk_score"] > 50:
        raise HTTPException(
            status_code=409,
            detail="traveler risk remains above release threshold",
        )

    case["status"] = "RELEASED"
    case["released_by"] = x_user_id
    return case
