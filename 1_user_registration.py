# Assignment 1: User Registration with Nested Conditionals
# Issues: Deeply nested conditionals (arrow anti-pattern), hard to follow logic flow
# Goal: Flatten the nesting, use early returns, improve readability

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.post("/register")
def register_user(username: str, email: str, age: int, country: str):
    if username:
        if len(username) >= 3:
            if email:
                if "@" in email and "." in email:
                    if age:
                        if age >= 18:
                            if country:
                                if country in ["US", "UK", "CA", "AU"]:
                                    return {"status": "success", "user": username}
                                else:
                                    raise HTTPException(400, "Country not supported")
                            else:
                                raise HTTPException(400, "Country required")
                        else:
                            raise HTTPException(400, "Must be 18+")
                    else:
                        raise HTTPException(400, "Age required")
                else:
                    raise HTTPException(400, "Invalid email")
            else:
                raise HTTPException(400, "Email required")
        else:
            raise HTTPException(400, "Username too short")
    else:
        raise HTTPException(400, "Username required")
