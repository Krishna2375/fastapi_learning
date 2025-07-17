from fastapi import FastAPI , HTTPException
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

@app.post("/register/",response_model=userout)
def resgister_user(user:userin):
    if user.email in user_db:
        raise HTTPException(status_code=400,detail=f"User Already Registered With Same Email ID. ")
    
    user_db[user.email]=user
    return user