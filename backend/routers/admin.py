from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import User, Resident, UserRole
from security import get_password_hash
from pydantic import BaseModel
import pandas as pd
import io

router = APIRouter()

# --- SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    role: UserRole
    password: str

# --- ENDPOINTS ---

# 1. BULK IMPORT RESIDENTS (Excel/CSV)
@router.post("/admin/residents/import")
def import_residents(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = file.file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    finally:
        file.file.close()

    required_columns = ['first_name', 'last_name', 'address', 'birthday', 'contact']
    for col in required_columns:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing required column: {col}")

    imported_count = 0
    errors = []

    for index, row in df.iterrows():
        try:
            first_name = str(row['first_name']).strip()
            last_name = str(row['last_name']).strip()
            
            base_username = f"{first_name.lower()}.{last_name.lower()}"
            username = base_username
            counter = 1
            while db.query(User).filter(User.username == username).first():
                username = f"{base_username}{counter}"
                counter += 1

            hashed_password = get_password_hash("barangay123")

            new_user = User(
                username=username,
                password=hashed_password,
                roles=UserRole.resident
            )
            db.add(new_user)
            db.flush()

            new_resident = Resident(
                user_id=new_user.user_id,
                first_name=first_name,
                middle_name=str(row.get('middle_name', '')).strip(),
                last_name=last_name,
                address=str(row['address']).strip(),
                birthday=str(row['birthday']).strip(),
                gender=str(row.get('gender', '')).strip(),
                contact=str(row['contact']).strip()
            )
            db.add(new_resident)
            imported_count += 1
        except Exception as e:
            errors.append(f"Row {index+2}: {str(e)}")
            db.rollback()
            continue

    db.commit()
    return {"message": "Import completed", "imported_count": imported_count, "errors": errors}

# 2. GET ALL USERS (For the Table)
@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    # Returns all users to populate the User Management table
    return db.query(User).all()

# 3. ADD MANUAL USER (From React Form)
@router.post("/users")
def add_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username, 
        roles=user_data.role, 
        password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

# 4. DELETE A USER (From Delete Modal)
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}