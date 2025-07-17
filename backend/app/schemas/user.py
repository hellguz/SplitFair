from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class UserCreate(UserBase):
    uuid: str

class User(UserBase):
    uuid: str

    class Config:
        from_attributes = True

class UserBalance(BaseModel):
    user_uuid: str
    balance: float
