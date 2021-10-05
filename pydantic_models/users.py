from pydantic import BaseModel, EmailStr, SecretStr, validator
from utils import validate_new_password


class UserAuthModel(BaseModel):
    email: EmailStr
    password: SecretStr

    @validator('password')
    def password_acceptable(cls, v):
        validate_new_password(v)
        return v


class UserCreateModel(UserAuthModel):
    name: str

    @validator('name')
    def name_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
