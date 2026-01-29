from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import User, Resident, UserRole
from security import get_password_hash
import pandas as pd
import io

router = APIRouter()

@router.post("/admin/residents/import")
def import_residents(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """
    FR2 & Req #5: Allows Super Admin to upload Excel/CSV to bulk create residents.
    Expected Columns in File: first_name, middle_name, last_name, address, birthday, gender, contact
    """
    
    # 1. Read the file content
    try:
        contents = file.file.read()
        # Determine file type (Excel or CSV) based on extension
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            # Assumes Excel .xlsx
            df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    finally:
        file.file.close()

    # 2. Validate required columns
    required_columns = ['first_name', 'last_name', 'address', 'birthday', 'contact']
    for col in required_columns:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing required column in Excel: {col}")

    imported_count = 0
    errors = []

    # 3. Iterate through rows and create users
    for index, row in df.iterrows():
        try:
            # Clean data
            first_name = str(row['first_name']).strip()
            last_name = str(row['last_name']).strip()
            address = str(row['address']).strip()
            birthday = str(row['birthday']).strip() # Ideally format this to Date object
            contact = str(row['contact']).strip()
            middle_name = str(row.get('middle_name', '')).strip()
            gender = str(row.get('gender', '')).strip()

            # Generate Username: firstname.lastname (lowercase)
            base_username = f"{first_name.lower()}.{last_name.lower()}"
            username = base_username
            
            # Ensure unique username (append number if exists)
            counter = 1
            while db.query(User).filter(User.username == username).first():
                username = f"{base_username}{counter}"
                counter += 1

            # Generate Default Password: "barangay123"
            default_password = "barangay123"
            hashed_password = get_password_hash(default_password)

            # A. Create User Account
            new_user = User(
                username=username,
                password=hashed_password,
                roles=UserRole.resident
            )
            db.add(new_user)
            db.flush() # Get the ID without committing yet

            # B. Create Resident Profile
            new_resident = Resident(
                user_id=new_user.user_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                address=address,
                birthday=birthday, # Ideally convert to datetime object here
                gender=gender,
                contact=contact
            )
            db.add(new_resident)
            
            imported_count += 1

        except Exception as e:
            errors.append(f"Row {index+2}: {str(e)}")
            db.rollback() # Rollback this specific row if error
            continue

    # 4. Commit all successful additions
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database commit failed: {str(e)}")

    return {
        "message": "Import completed",
        "imported_count": imported_count,
        "errors_count": len(errors),
        "errors": errors
    }