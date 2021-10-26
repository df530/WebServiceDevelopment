from fastapi import FastAPI, HTTPException
from pydantic_models.users import UserCreateModel, UserAuthModel
from databases.users import get_user_by_auth, is_email_occupied, add_user, get_num_of_users

datagram_app = FastAPI()


@datagram_app.get("/statistics/")
async def get_statistics(indicator: str):
    if indicator != "num_of_users":
        raise HTTPException(status_code=404, detail="Don't know this indicator")
    get_num_of_users()


@datagram_app.post("/users/registration", status_code=201)
async def register_user(user: UserCreateModel):
    if is_email_occupied(user.email):
        raise HTTPException(status_code=403, detail="This mail has been already registered")
    add_user(user.email, user.name, user.password.get_secret_value())
    return "Registered successfully"


@datagram_app.post("/users/auth")
async def authorize(user_auth: UserAuthModel):
    user = get_user_by_auth(user_auth.email, user_auth.password.get_secret_value())
    if user is None:
        raise HTTPException(status_code=403, detail="Wrong mail or password")
    return user
