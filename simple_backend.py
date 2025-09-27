from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
import json
import os

app = FastAPI(title="YSense Backend v3.0")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple file-based storage (no database issues)
USERS_FILE = "users.json"

# Load existing users
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

# Models
class UserRegistration(BaseModel):
    username: str
    email: str
    attribution_name: Optional[str]
    age: int
    jurisdiction: str
    consents: Dict[str, bool]

@app.get("/")
def root():
    return {
        "platform": "YSense Backend v3.0",
        "status": "operational",
        "storage": "file-based"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "users_count": len(users)}

@app.post("/register")
def register(user: UserRegistration):
    # Check if user exists
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Save user
    users[user.username] = {
        "email": user.email,
        "attribution_name": user.attribution_name,
        "age": user.age,
        "jurisdiction": user.jurisdiction,
        "consents": user.consents,
        "registered_at": datetime.now().isoformat()
    }
    
    # Save to file
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return {"message": "Registration successful", "username": user.username}

@app.get("/users")
def get_users():
    return {"users": users, "count": len(users)}

if __name__ == "__main__":
    import uvicorn
    print("Starting Simple YSense Backend on port 8000...")
    print("No database required - using file storage")
    uvicorn.run(app, host="0.0.0.0", port=8000)
