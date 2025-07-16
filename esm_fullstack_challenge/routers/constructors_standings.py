from fastapi import APIRouter, Response
from typing import List
import aiosqlite
from esm_fullstack_challenge.config import DB_FILE
from pydantic import BaseModel

class ConstructorStandingsOut(BaseModel):
    id: int  
    constructor_name: str
    total_points: float

constructors_router = APIRouter()

@constructors_router.get("/my_constructor_standings", response_model=List[ConstructorStandingsOut])
async def get_constructor_standings(response: Response):
    query = '''
        SELECT
            c.id as id,
            c.name as constructor_name,
            SUM(cr.points) as total_points
        FROM
            constructor_results cr
            JOIN races r ON cr.race_id = r.id
            JOIN constructors c ON cr.constructor_id = c.id
        WHERE
            r.year = 2024
        GROUP BY
            c.id, c.name
        ORDER BY
            total_points DESC
        LIMIT 10
    '''
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(query)
        rows = await cursor.fetchall()
        total = len(rows)
        response.headers["Content-Range"] = f"constructor_standings 0-{max(total-1,0)}/{total}"
        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
        
        return [dict(row) for row in rows]