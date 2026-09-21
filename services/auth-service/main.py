from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Auth Service",
    description="Microservicio de autenticación para el sistema de reservas",
    version="1.0.0"
)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {
        "service": "auth-service",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/login")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "cloud123":
        return {
            "authenticated": True,
            "token": "demo-token"
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )