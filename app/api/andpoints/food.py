from fastapi import HTTPException, status, APIRouter, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse, FileResponse
import datetime
import os
import shutil
import main

from schemas.shemas import UpdateFood

food_router = APIRouter(tags=["food"], prefix="/food")

headers = {"Access-Control-Allow-Origin": "*",
           "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
           "Access-Control-Allow-Headers": "Content-Type, Authorization",
           "Access-Control-Allow-Credentials": "true"}


@food_router.post("/add_food/{restaurant_id}")
def add_food(restaurant_id: int, kind: str = Form(...), price: int = Form(...),
                   cook_time: int = Form(...), food_name: str = Form(...), description: str = Form(...),
                   image_food: UploadFile = File(...)):

    current_date_time = (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    food_image_name = f"food_image_{current_date_time}.{image_food.filename.split('.')[-1]}"

    try:
        main.cursor.execute("""INSERT INTO foods (kind, price, cook_time,
                        image, food_name, description, restaurant_id) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (kind, price, cook_time, food_image_name,
                             food_name, description, restaurant_id))

        main.conn.commit()

        with open(f"{os.getcwd()}/static/images/food/{food_image_name}", "wb") as file_object:
            shutil.copyfileobj(image_food.file, file_object)

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Food successfully added"},
                        headers=headers)


@food_router.put("/update_food/{food_id}")
def update_food(food_id: int, data: UpdateFood):
    try:
        main.cursor.execute("""SELECT * FROM foods WHERE food_id= %s""",
                            (food_id,))

        target_food = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    if target_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Food not found")

    try:
        main.cursor.execute("""UPDATE foods SET  kind=%s, price=%s, 
                            cook_time=%s, food_name=%s, description=%s,  
                            WHERE food_id = %s""",
                            (data.kind, data.price, data.cook_time,
                             data.food_name, data.description, food_id))

        main.conn.commit()

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Food updated successfully"},
                        headers=headers)


@food_router.put("/update_images_foods/{food_id}")
def update_images(food_id, image_food: UploadFile = File(...)):
    current_date_time = (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    food_image_name = f"food_image_{current_date_time}.{image_food.filename.split('.')[-1]}"

    try:
        main.cursor.execute("""SELECT * FROM foods WHERE food_id= %s""", (food_id,))
        target_food = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    if target_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Food not found")

    old_image_path = target_food.get('image')

    try:

        main.cursor.execute("""UPDATE foods SET image = %s WHERE food_id = %s""",
                            (food_image_name, food_id))
        main.conn.commit()

        if old_image_path and os.path.exists(f"{os.getcwd()}/static/images/food/{old_image_path}"):
            os.remove(f"{os.getcwd()}/static/images/food/{old_image_path}")

        with open(f"{os.getcwd()}/static/images/food/{food_image_name}", "wb") as file_object:
            shutil.copyfileobj(image_food.file, file_object)

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": str(error)})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Food images updated successfully"},
                        headers=headers)


@food_router.delete("/delete_food/{food_id}")
def delete_food(food_id: int):
    try:
        main.cursor.execute("""SELECT * FROM foods WHERE food_id= %s""",
                            (food_id,))

        target_food = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": error})

    if target_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Food not found")

    try:
        main.cursor.execute("""DELETE FROM foods WHERE food_id=%s""",
                            (food_id,))

        main.conn.commit()

    except Exception as error:
        main.conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": "There was an error deleting the food"
                                    f"ERROR: {error}"})

    if os.path.exists(target_food.get('image')):
        os.remove(target_food.get('image'))

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Food successfully deleted"},
                        headers=headers)


@food_router.get("/get_food_by_id/{food_id}")
def get_food_by_id(food_id: int):
    try:
        main.cursor.execute("""SELECT * FROM foods WHERE food_id=%s""",
                            (food_id,))

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No food found with {food_id} id"
                                   f"ERROR: {error}")

    try:
        food = main.cursor.fetchone()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while searching for the food"
                            f"ERROR: {error}")

    if food is None:
        raise HTTPException(status_code=404,
                            detail=f"Restaurant with id {food_id} was not found!")

    return JSONResponse(status_code=status.HTTP_200_OK, content=food, headers=headers)


@food_router.get("/get_all_foods")
def get_all_foods(page: int = Query(default=1, ge=1)):
    per_page = 20

    main.cursor.execute("SELECT count(*) FROM foods")
    count = main.cursor.fetchall()[0]['count']

    if count == 0:
        return JSONResponse(status_code=status.HTTP_200_OK, content=[], headers=headers)
    max_page = (count - 1) // per_page + 1

    if page > max_page:
        page = max_page

    offset = (page - 1) * per_page

    try:
        main.cursor.execute(f"""SELECT * FROM foods LIMIT %s OFFSET %s""", (per_page, offset))

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": str(error)})

    try:

        foods = main.cursor.fetchall()

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred while searching for all foods. ERROR: {str(error)}")

    if not foods:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Foods were not found!")

    content = {
        "foods": foods,
        "page": page,
        "total_pages": max_page,
        "total_foods": count
    }

    return JSONResponse(content=content,
                        headers=headers)


@food_router.get("/get_image/{file}")
def get_food_image(file: str):
    path = f"{os.getcwd()}/static/images/food/{file}"
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse(
        headers=headers,
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "File not found"
        }
    )
