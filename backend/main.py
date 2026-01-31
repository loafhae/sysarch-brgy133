from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import User, Resident, Admin, Official, UserRole
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

# --- ADD THIS MIDDLEWARE ---
# This tells the Browser: "It is safe to connect to me"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (like Chrome)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str

class AnnouncementRequest(BaseModel):
    title: str
    body: str
    created_by: int

@app.get("/")
def home():
    return {"message": "Barangay API is Running (Strict Version)"}

@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or user.password != req.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    full_name = "User"
    role_str = str(user.roles)

    if role_str == "Super Admin":
        profile = db.query(Admin).filter(Admin.user_id == user.user_id).first()
        if profile:
            full_name = f"{profile.first_name} {profile.last_name}"
    elif role_str == "Barangay Official":
        profile = db.query(Official).filter(Official.user_id == user.user_id).first()
        if profile:
            full_name = f"{profile.first_name} {profile.last_name}"
    elif role_str == "Resident":
        profile = db.query(Resident).filter(Resident.user_id == user.user_id).first()
        if profile:
            full_name = f"{profile.first_name} {profile.last_name}"

    return {
        "user_id": user.user_id,
        "username": user.username,
        "role": role_str,
        "full_name": full_name
    }

@app.post("/announcements")
def create_announcement(req: AnnouncementRequest, db: Session = Depends(get_db)):
    new_ann = Announcement(
        title=req.title,
        body=req.body,
        created_by=req.created_by
    )
    db.add(new_ann)
    db.commit()
    return {"message": "Announcement posted successfully!"}