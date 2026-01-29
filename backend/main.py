from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import User, Resident, Admin, Official, UserRole
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

# --- MIDDLEWARE ---
# Allows React and Flutter to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- SCHEMAS ---
class LoginRequest(BaseModel):
    username: str
    password: str

# --- ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Barangay API is Running (Strict Version)"}

@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    # 1. Find the user in the database
    user = db.query(User).filter(User.username == req.username).first()
    
    # 2. Validate User and Password
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check if password is hashed (bcrypt starts with $2b$, $2a$, or $2y$)
    if user.password.startswith('$2'):
        # Password is hashed, use verify
        if not pwd_context.verify(req.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        # Password is plain text (temporary fix - hash it on the fly)
        if req.password != user.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3. Determine the Full Name based on Role
    full_name = "User"
    role_str = user.roles.value if hasattr(user.roles, 'value') else str(user.roles)

    if user.roles == UserRole.super_admin:
        profile = db.query(Admin).filter(Admin.user_id == user.user_id).first()
        if profile:
            full_name = f"{profile.first_name} {profile.last_name}"
            
    elif user.roles == UserRole.barangay_official:
        profile = db.query(Official).filter(Official.user_id == user.user_id).first()
        if profile:
            full_name = f"{profile.first_name} {profile.last_name}"
            
    elif user.roles == UserRole.resident:
        profile = db.query(Resident).filter(Resident.user_id == user.user_id).first()
        if profile:
            full_name = f"{profile.first_name} {profile.last_name}"

    # 4. Return the data
    return {
        "user_id": user.user_id,
        "username": user.username,
        "role": role_str,
        "full_name": full_name
    }