from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
import time

app=FastAPI()

user_db={}

class userin(BaseModel):
    username : str
    email : str
    password : str

class userout(BaseModel):
    username : str
    email : str 

def get_db():
    return user_db

def welcome_mail(email : str):
    time.sleep(2)
    print(f"sent welcome mail to {email}")

@app.post("/register/",response_model=userout)
def register(user:userin,background_task: BackgroundTasks,db: dict=Depends(get_db)):
    if user.email in  db:
        raise HTTPException (status_code=400, detail=f"Email already registered")
    
    db[user.email]=user
    
    background_task.add_task(welcome_mail,user.email)

    return user