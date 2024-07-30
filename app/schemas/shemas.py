# For Data Validations
from pydantic import BaseModel, EmailStr


class UpdateRestaurant(BaseModel):
    restaurant_name: str
    restaurant_email: str
    phone_number: str
    rating: float


class UpdateFood(BaseModel):

    kind: str
    price: float
    cook_time: int
    food_name: str
    description: str
    restaurant_id: int


class RestaurantWorkTimeAdd(BaseModel):
    restaurant_id: str
    day_of_week: str
    opening_time: str
    closing_time: str
