from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from . import schemas, models, utils
from .database import sessionlocal

router = APIRouter()

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup",response_model= schemas.showuser)
def signup(user:schemas.Usercreate,db = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username==user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User Already Exits.")
    
    hashed_pw = utils.get_password_hash(user.password)
    new_user = models.User(username=user.username,email=user.email,mobile_no=user.mobile_no,role=user.role,hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model=schemas.TokenResponse)
def login(user:schemas.userlogin,db = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username==user.username).first()
    if not db_user or not utils.verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = utils.create_access_token({"sub":db_user.username})
    return {"access_token": token, "token_type": "bearer"}