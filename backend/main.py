from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Dict

app = FastAPI()

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

# Fake DB
users_db: Dict[str, Dict] = {}

# Models
class User(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    password: str

# Utils
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_token(username: str):
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in users_db:
            raise HTTPException(status_code=401)
        return username
    except JWTError:
        raise HTTPException(status_code=401)

# Routes
@app.post("/signup")
def signup(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User exists")
    users_db[user.username] = {
        "password": hash_password(user.password)
    }
    return {"msg": "User created"}

@app.post("/signin")
def signin(user: User):
    db_user = users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user.username)
    return {"access_token": token}

@app.put("/user")
def update_user(data: UserUpdate, username=Depends(get_current_user)):
    users_db[username]["password"] = hash_password(data.password)
    return {"msg": "User updated"}

@app.delete("/user")
def delete_user(username=Depends(get_current_user)):
    del users_db[username]
    return {"msg": "User deleted"}
