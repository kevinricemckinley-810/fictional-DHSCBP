from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Fictional CBP Traveler Service")
EXPECTED_INTERNAL_KEY = "demo-internal-key"

TRAVELERS = {
    "T-1001": {
        "traveler_id": "T-1001",
        "name": "Alex Morgan",
        "dob": "1988-04-12",
        "passport": "X0001001",
        "assigned_office": "JFK",
        "risk_score": 87,
        "watchlist_note": "Synthetic training flag: secondary review required.",
    },
    "T-1002": {
        "traveler_id": "T-1002",
        "name": "Jordan Lee",
        "dob": "1991-09-30",
        "passport": "X0001002",
        "assigned_office": "IAD",
        "risk_score": 21,
        "watchlist_note": "",
    },
}

def require_internal_key(x_internal_key: str | None):
    if x_internal_key != EXPECTED_INTERNAL_KEY:
        raise HTTPException(status_code=403, detail="invalid internal key")

@app.get("/internal/travelers/{traveler_id}")
def get_traveler(
    traveler_id: str,
    x_user_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
    x_user_office: str | None = Header(default=None),
    x_internal_key: str | None = Header(default=None),
):
    require_internal_key(x_internal_key)
    traveler = TRAVELERS.get(traveler_id)
    if not traveler:
        raise HTTPException(status_code=404, detail="traveler not found")

    if x_user_role not in {"officer", "supervisor", "analyst"}:
        raise HTTPException(status_code=403, detail="role not permitted")

    if x_user_role == "officer" and x_user_office != traveler["assigned_office"]:
        raise HTTPException(status_code=403, detail="record outside assigned office")

    return traveler

@app.post("/internal/travelers/{traveler_id}/risk")
def update_risk(
    traveler_id: str,
    payload: dict,
    x_user_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
    x_internal_key: str | None = Header(default=None),
):
    require_internal_key(x_internal_key)
    traveler = TRAVELERS.get(traveler_id)
    if not traveler:
        raise HTTPException(status_code=404, detail="traveler not found")

    if x_user_role not in {"analyst", "supervisor"}:
        raise HTTPException(status_code=403, detail="insufficient role")

    new_score = payload.get("risk_score")
    if not isinstance(new_score, int) or not 0 <= new_score <= 100:
        raise HTTPException(status_code=400, detail="risk_score must be 0-100")

    traveler["risk_score"] = new_score
    return {
        "traveler_id": traveler_id,
        "risk_score": new_score,
        "updated_by": x_user_id,
    }
