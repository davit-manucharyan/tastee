from fastapi import HTTPException, status, APIRouter
from fastapi.responses import JSONResponse


from services.db_service import get_row, add_row
from schemas.shemas import RestaurantWorkTimeAdd

restaurant_work_time_router = APIRouter(tags=["Work Times"], prefix="/restaurant/work-time")

headers = {"Access-Control-Allow-Origin": "*",
           "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
           "Access-Control-Allow-Headers": "Content-Type, Authorization",
           "Access-Control-Allow-Credentials": "true"}


@restaurant_work_time_router.post("/add")
def add_work_time(data: RestaurantWorkTimeAdd):
    restaurant = get_row(
        "restaurants",
        {
            "restaurant_id": data.restaurant_id
        }
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with ID ({data.restaurant_id}) not found"
        )

    row = add_row(
        "work_time",
        {
            "restaurant_id": data.restaurant_id,
            "day_of_week": data.day_of_week,
            "opening_time": data.opening_time,
            "closing_time": data.closing_time
        }
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Work time added successfully"
        },
        headers=headers
    )


@restaurant_work_time_router.get("/get_all_work_times/{restaurant_id}")
def get_restaurant_work_times(restaurant_id: int):
    restaurant = get_row(
        "work_time",
        {
            "restaurant_id": restaurant_id
        }
    )
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with ID ({restaurant_id}) not found"
        )

    times = get_row(
        "work_time",
        {
            "restaurant_id": restaurant_id
        }
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content=times, headers=headers)
