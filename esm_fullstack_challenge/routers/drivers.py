from typing import List
import aiosqlite
from fastapi import APIRouter
from esm_fullstack_challenge.config import DB_FILE
from esm_fullstack_challenge.models import AutoGenModels
from esm_fullstack_challenge.routers.utils import \
    get_route_list_function, get_route_id_function


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


# Add route to create a new driver
@drivers_router.post('', response_model=table_model)
def create_driver():
    """
    Create a new driver.
    """
    new_driver = {
        'id': 12345,
        'driver_ref': 'Doe',
        'number': '12345',
        'code': 'DOE',
        'forename': 'John',
        'surname': 'Doe',
        'dob': '1990-01-01',
        'nationality': 'American',
        'url': 'http://example.com/driver/12345',
    }

    return table_model(**new_driver)


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
@drivers_router.delete('/{id}', response_model=table_model)
def delete_driver(id: int):
    """
    Delete driver.
    """
    updated_driver = {
        'id': f'{id}',
        'driver_ref': 'Doe',
        'number': '12345',
        'code': 'DOE',
        'forename': 'John',
        'surname': 'Doe',
        'dob': '1990-01-01',
        'nationality': 'American',
        'url': 'http://example.com/driver/12345',
    }

    return table_model(**updated_driver)
