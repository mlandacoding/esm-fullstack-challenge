from typing import List, Optional
import aiosqlite
from fastapi import APIRouter
from esm_fullstack_challenge.config import DB_FILE
from esm_fullstack_challenge.models import AutoGenModels
from esm_fullstack_challenge.routers.utils import \
    get_route_list_function, get_route_id_function
from pydantic import BaseModel

drivers_router = APIRouter()

table_model = AutoGenModels['drivers']

# Route to get driver by id
get_driver = get_route_id_function('drivers', table_model)
drivers_router.add_api_route(
    '/{id}', get_driver,
    methods=["GET"], response_model=table_model,
)

# Route to get a list of drivers
get_drivers = get_route_list_function('drivers', table_model)
drivers_router.add_api_route(
    '', get_drivers,
    methods=["GET"], response_model=List[table_model],
)

class DriverCreateModel(BaseModel):
    driver_ref: str
    number: str
    code: str
    forename: str
    surname: str
    dob: str
    nationality: str
    url: str
    id: Optional[int] = None


@drivers_router.post("", response_model=table_model)
async def create_driver(driver: DriverCreateModel):
    driver_data = driver.dict(exclude_unset=True)
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT MAX(id) as max_id FROM drivers")
        row = await cursor.fetchone()
        next_id = (row["max_id"] or 0) + 1
    driver_data["id"] = next_id
    columns = ', '.join(driver_data.keys())
    placeholders = ', '.join(['?' for _ in driver_data])
    values = list(driver_data.values())
    query = f"INSERT INTO drivers ({columns}) VALUES ({placeholders})"
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(query, values)
        await db.commit()
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM drivers WHERE id = ?", (next_id,))
        row = await cursor.fetchone()
        return table_model(**dict(row))


# Add route to update driver
@drivers_router.put("/{driver_id}", response_model=table_model)
async def update_driver(driver_id: int, driver: table_model):
    async with aiosqlite.connect(DB_FILE) as db:
        fields = [f"{key}=?" for key in driver.dict().keys() if key != "id"]
        values = [value for key, value in driver.dict().items() if key != "id"]
        values.append(driver_id)
        query = f"UPDATE drivers SET {', '.join(fields)} WHERE id=?"
        await db.execute(query, values)
        await db.commit()
    return driver


# Add route to delete driver
@drivers_router.delete("/{driver_id}")
async def delete_driver(driver_id: int):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("DELETE FROM drivers WHERE id = ?", (driver_id,))
        await db.commit()
    return {"status": "deleted"}



