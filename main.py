from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

wsd_app = FastAPI()

user_list = [
    {
        'mail': 'abc@yandex.ru',
        'password': 'abc_pwd'
    },
    {
        'mail': 'qwerty@gmail.com',
        'password': 'qwerty'
    }
]


@wsd_app.get("/statistics/")
async def get_statistics(indicator: str):
    if indicator == "num_of_users":
        return {'number of users': len(user_list)}
    raise HTTPException(status_code=404, detail="Don't know this indicator")


class User(BaseModel):
    mail: str = Field(..., regex=r".+@.+\..+")
    password1: str
    password2: str


@wsd_app.post("/registration/", status_code=201)
async def create_account(user: User):
    if user.mail in [d['mail'] for d in user_list]:
        raise HTTPException(status_code=403, detail="This mail has been already registered")
    if user.password1 != user.password2:
        raise HTTPException(status_code=403, detail="Passwords don't match")
    user_list.append({'mail': user.mail, 'password': user.password1})
    return "Account is created"
