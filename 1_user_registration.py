from fastapi import FastAPI, HTTPException

app = FastAPI()

SUPPORTED_COUNTRIES = {"US", "UK", "CA", "AU"}


@app.post("/register")
def register_user(username: str, email: str, age: int, country: str):

    # Username validation
    if not username:
        raise HTTPException(status_code=400, detail="Username required")
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username too short")

    # Email validation
    if not email:
        raise HTTPException(status_code=400, detail="Email required")
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Invalid email")

    # Age validation
    if age is None:
        raise HTTPException(status_code=400, detail="Age required")
    if age < 18:
        raise HTTPException(status_code=400, detail="Must be 18+")

    # Country validation
    if not country:
        raise HTTPException(status_code=400, detail="Country required")
    if country not in SUPPORTED_COUNTRIES:
        raise HTTPException(status_code=400, detail="Country not supported")

    return {
        "status": "success",
        "user": username
    }
       