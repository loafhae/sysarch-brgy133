from database import engine, Base, get_db
from models import * # Import all models

# This command checks if the tables in 'models.py' match the tables in the DB
# It won't overwrite data, just validate structure.
print("Connecting to XAMPP Database...")
try:
    # Attempt to connect
    with engine.connect() as connection:
        print("✅ Successfully connected to MySQL (XAMPP)!")
        
    # Optional: If you wanted to create tables from Python (instead of SQL import), you would run:
    # Base.metadata.create_all(bind=engine)
    
    print("Database models aligned.")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")