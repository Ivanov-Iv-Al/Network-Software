from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Other Service")

class OtherItem(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

other_db = [
    OtherItem(id=1, name="Документация API", description="Описание всех endpoints", created_at=datetime.now()),
    OtherItem(id=2, name="Логи сервера", description="Логи за последний час", created_at=datetime.now()),
]
id_counter = 3

@app.get("/api/v1/other/", response_model=List[OtherItem])
async def get_other_items():
    return other_db

@app.get("/api/v1/other/{item_id}", response_model=OtherItem)
async def get_other_item(item_id: int):
    item = next((i for i in other_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    return item

@app.post("/api/v1/other/", response_model=OtherItem, status_code=201)
async def create_other_item(name: str, description: str):
    global id_counter
    new_item = OtherItem(
        id=id_counter,
        name=name,
        description=description,
        created_at=datetime.now()
    )
    other_db.append(new_item)
    id_counter += 1
    return new_item

@app.delete("/api/v1/other/{item_id}")
async def delete_other_item(item_id: int):
    global other_db
    item = next((i for i in other_db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Элемент не найден")
    other_db = [i for i in other_db if i.id != item_id]
    return {"message": "Элемент удален"}