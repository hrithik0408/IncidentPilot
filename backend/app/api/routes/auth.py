from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.core.security import verify_password, create_access_token
from app.services.demo_data import ensure_demo_data

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    ensure_demo_data(db)
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token(user.id), "user": {"id": user.id, "email": user.email, "name": user.name, "role": user.role}}
