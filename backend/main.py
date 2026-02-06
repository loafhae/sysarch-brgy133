from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import get_db, engine, Base
from models import User, Resident, Admin, Official, Announcement, Feedback, AuditLog
from pydantic import BaseModel
from security import verify_password, hash_password
import csv
import codecs

# --- INITIALIZATION ---
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SCHEMAS ---
class LoginRequest(BaseModel):
    username: str
    password: str

class ResidentCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    address: str
    birthday: str 
    gender: str
    contact: str

class UserCreateGeneric(BaseModel):
    username: str
    password: str
    role: str

class AnnouncementCreate(BaseModel):
    title: str
    body: str
    created_by: int

class FeedbackCreate(BaseModel):
    resident_id: int
    message: str

# --- STARTUP DOCTOR (This fixes your Login!) ---
@app.on_event("startup")
def startup_db_check():
    db = next(get_db())
    # Try to find the admin
    admin = db.query(User).filter(User.username == "admin").first()
    
    if not admin:
        print("\n-------------------------------------")
        print("🔧 ADMIN MISSING! CREATING SUPER ADMIN...")
        # 1. Create the User Login
        new_user = User(username="admin", password=hash_password("admin123"), roles="super_admin")
        db.add(new_user)
        db.commit()
        
        # 2. Create the Admin Profile
        new_profile = Admin(user_id=new_user.user_id, first_name="Super", last_name="Admin", contact="09123456789")
        db.add(new_profile)
        db.commit()
        print("✅ ADMIN CREATED SUCCESSFULLY.")
        print("👉 Username: admin")
        print("👉 Password: admin123")
        print("-------------------------------------\n")
    else:
        print("✅ SYSTEM READY: Admin account exists.")

# --- ENDPOINTS ---

@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    # 1. Find User
    user = db.query(User).filter(User.username == req.username).first()
    
    # 2. Verify Password (Securely)
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 3. Get Role & Name
    full_name = "User"
    # Convert Enum to string safely
    user_role = user.roles.value if hasattr(user.roles, 'value') else str(user.roles)
    
    if user_role == "super_admin":
        p = db.query(Admin).filter(Admin.user_id == user.user_id).first()
        full_name = f"{p.first_name} {p.last_name}" if p else "Admin"
    elif user_role == "resident":
        p = db.query(Resident).filter(Resident.user_id == user.user_id).first()
        full_name = f"{p.first_name} {p.last_name}" if p else "Resident"
    elif user_role == "barangay_official":
        p = db.query(Official).filter(Official.user_id == user.user_id).first()
        full_name = f"{p.first_name} {p.last_name}" if p else "Official"

    return {
        "user_id": user.user_id,
        "username": user.username,
        "role": user_role,
        "full_name": full_name
    }

# --- USER MANAGEMENT ---

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    result = []
    for user in users:
        role_str = user.roles.value if hasattr(user.roles, 'value') else str(user.roles)
        result.append({
            "id": user.user_id,
            "username": user.username,
            "role": role_str.replace("_", " ").title(),
            "status": "Active"
        })
    return result

@app.post("/users")
def create_generic_user(req: UserCreateGeneric, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=400, detail="Username taken")

    role_map = {"Admin": "super_admin", "Official": "barangay_official", "Resident": "resident"}
    db_role = role_map.get(req.role, "resident")

    hashed = hash_password(req.password)
    new_user = User(username=req.username, password=hashed, roles=db_role)
    db.add(new_user)
    db.commit()
    
    # Create empty profile to prevent errors
    if db_role == "barangay_official":
        db.add(Official(user_id=new_user.user_id, first_name="New", last_name="Official"))
    elif db_role == "resident":
        db.add(Resident(user_id=new_user.user_id, first_name="New", last_name="Resident", address="TBD"))
    elif db_role == "super_admin":
        db.add(Admin(user_id=new_user.user_id, first_name="New", last_name="Admin"))
    
    db.commit()
    return {"message": "User created successfully"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username == "admin":
        raise HTTPException(status_code=400, detail="Cannot delete Super Admin")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

# --- OTHER ENDPOINTS ---

@app.get("/announcements")
def get_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).order_by(desc(Announcement.created_at)).all()

@app.post("/announcements")
def create_announcement(req: AnnouncementCreate, db: Session = Depends(get_db)):
    new_ann = Announcement(title=req.title, body=req.body, created_by=req.created_by)
    db.add(new_ann)
    db.commit()
    return {"message": "Announcement posted"}

@app.post("/feedback")
def submit_feedback(req: FeedbackCreate, db: Session = Depends(get_db)):
    new_fb = Feedback(resident_id=req.resident_id, message=req.message, status="Pending")
    db.add(new_fb)
    db.commit()
    return {"message": "Feedback submitted"}