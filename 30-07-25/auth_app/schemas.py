from pydantic import BaseModel


class Usercreate(BaseModel):
    username : str
    password : str
    email : str
    mobile_no : int
    role : str

class userlogin (BaseModel):
    username : str
    password : str
    role : str

class showuser (BaseModel):
    id : int
    username : str
    role : str

    class config :
        omr_mode = True 

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
