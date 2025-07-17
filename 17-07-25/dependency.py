from fastapi import FastAPI , HTTPException,Depends
from pydantic import BaseModel 

app=FastAPI()

user_db={}

class userin (BaseModel):
    username : str
    password : str
    email : str

class userout (BaseModel):
    username: str
    email: str

class logininput(BaseModel):
    email : str
    password : str

def get_user_db():
    return user_db

@app.post("/register/",response_model=userout)
def resgister_user(user:userin,db: dict= Depends(get_user_db)):
    if user.email in db:
        raise HTTPException(status_code=400,detail=f"{user.email} Already Registered.")
    db[user.email] = user
    return user

@app.post("/login/",response_model=userout)
def login_user(login_data:logininput,db: dict= Depends(get_user_db)):
    user=db.get(login_data.email)

    if not user :
        raise HTTPException (status_code=404,detail=f"User Not Found.")
    if user.password!=login_data.password:
        raise HTTPException (status_code=400,detail="Invalid Password.")
    return user