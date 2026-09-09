import os
import httpx
from fastapi import Depends, FastAPI, Header, HTTPException

from common.auth import parse_identity

app = FastAPI(title="Fictional CBP Traveler Gateway")

TRAVELER_SERVICE_URL = os.getenv("TRAVELER_SERVICE_URL", "http://127.0.0.1:8001")
INSPECTION_SERVICE_URL = os.getenv("INSPECTION_SERVICE_URL", "http://127.0.0.1:8002")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "demo-internal-key")

def downstream_headers(identity: dict, x_user_role: str | None) -> dict:
    effective_role = x_user_role or identity["role"]
    return {
        "X-User-Id": identity["user_id"],
        "X-User-Role": effective_role,
        "X-User-Office": identity["office"],
        "X-Internal-Key": INTERNAL_API_KEY,
    }

@app.get("/api/travelers/{traveler_id}")
async def get_traveler(
    traveler_id: str,
    identity: dict = Depends(parse_identity),
    x_user_role: str | None = Header(default=None),
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TRAVELER_SERVICE_URL}/internal/travelers/{traveler_id}",
            headers=downstream_headers(identity, x_user_role),
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.post("/api/travelers/{traveler_id}/risk")
async def update_risk(
    traveler_id: str,
    payload: dict,
    identity: dict = Depends(parse_identity),
    x_user_role: str | None = Header(default=None),
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TRAVELER_SERVICE_URL}/internal/travelers/{traveler_id}/risk",
            json=payload,
            headers=downstream_headers(identity, x_user_role),
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.post("/api/cases/{case_id}/release")
async def release_case(
    case_id: str,
    identity: dict = Depends(parse_identity),
    x_user_role: str | None = Header(default=None),
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{INSPECTION_SERVICE_URL}/internal/cases/{case_id}/release",
            headers=downstream_headers(identity, x_user_role),
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()
