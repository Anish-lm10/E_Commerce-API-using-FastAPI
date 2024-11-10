from pydantic import BaseModel
from typing import List


class SignupModel(BaseModel):
    id: int | None = None
    username: str
    email: str
    password: str
    is_staff: bool | None = None
    is_active: bool | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_active": True,
                "is_staff": False,
            }
        }


# for jwt auth
class Token(BaseModel):
    access_token: str
    token_type: str


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    order_id: int | None = None
    quantity: int
    order_status: str | None = "PENDING"
    order_size: str | None = "MEDIUM"
    user_id: int | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "quantity": 1,
                "order_size": "MEDIUM",
            }
        }

class OrderStatusModel(BaseModel):
    order_status: str | None = "PENDING"

    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "order_status": "PENDING",
            }
        }

