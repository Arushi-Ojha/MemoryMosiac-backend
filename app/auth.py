from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from app import schemas, models
from app.schemas import EmailSchema
from app.database import get_db
from google.oauth2 import id_token
from google.auth.transport import requests
from app.verify import generate_otp, send_otp_email, verify_otp


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not verify_otp(user.email, user.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = models.User(
        username=user.username,
        password=hashed_pw,
        email=user.email
    )
    


    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or Email already exists")

    return new_user
def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "Logged in successfully", "username": db_user.username}

@router.get("/get-user-id")
def get_user_id(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id}
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
@router.post("/google-login")
def google_login(token: str, db: Session = Depends(get_db)):

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo['email']
        name = idinfo.get('name', email.split("@")[0])

        user = db.query(models.User).filter(models.User.email == email).first()

        if not user:

            user = models.User(username=name, email=email, password="google_auth_user")
            db.add(user)
            db.commit()
            db.refresh(user)

        return {
            "message": "logged in successful",
            "username": user.username,
            "email": user.email
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    
@router.post("/send-otp")
def send_otp(request: EmailSchema, background_tasks: BackgroundTasks):
    email = request.email
    otp = generate_otp(email)
    background_tasks.add_task(send_otp_email, email, otp)
    return {"message": "OTP sent to your email"}