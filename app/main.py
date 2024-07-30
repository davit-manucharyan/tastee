# FastAPI
import time
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware


# SQL - postgres
import psycopg2
from psycopg2.extras import RealDictCursor


from database import engine
from models.models import Base


from api.andpoints.restaurant import restaurant_router
from api.andpoints.food import food_router
from api.andpoints.restaurant_work_time import restaurant_work_time_router


Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=5432,
            database='tastee-admin-panel',
            user='postgres',
            password='password',
            cursor_factory=RealDictCursor
            )
        print("Connection successfully")

        cursor = conn.cursor()
        break
    except Exception as error:
        print(error)
        time.sleep(3)


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def main():

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "OK"})


app.include_router(food_router)
app.include_router(restaurant_router)
app.include_router(restaurant_work_time_router)
