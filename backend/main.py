from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import User, Admin, Official, Resident, UserRole
from schemas import LoginRequest, LoginResponse
from security import verify_password, create_access_token
from routers import admin  # <--- Added this

app = FastAPI(title="Barangay System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Admin Router
app.include_router(admin.router) # <--- Added this

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    full_name = "Unknown User"
    if user.roles == UserRole.super_admin:
        profile = db.query(Admin).filter(Admin.user_id == user.user_id).first()
        if profile: full_name = f"{profile.first_name} {profile.last_name}"
    elif user.roles == UserRole.barangay_official:
        profile = db.query(Official).filter(Official.user_id == user.user_id).first()
        if profile: full_name = f"{profile.first_name} {profile.last_name}"
    elif user.roles == UserRole.resident:
        profile = db.query(Resident).filter(Resident.user_id == user.user_id).first()
        if profile: full_name = f"{profile.first_name} {profile.last_name}"

    access_token = create_access_token(data={"sub": user.username, "role": user.roles, "id": user.user_id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "role": user.roles,
        "full_name": full_name
    }

@app.get("/")
def read_root():
    return {"status": "System Online"}