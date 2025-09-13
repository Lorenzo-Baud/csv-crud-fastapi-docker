from fastapi import FastAPI, HTTPException
from typing import List
from .schemas import Item  #importo la classe Item da schemas.py
from . import csv_store as db #importo csv_store e lo rinomino in db per chiarezza

app = FastAPI(title="CSV CRUD API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    db.ensure_csv_exists()

@app.get("/")
def ping():
    return {"status": "ok"}

@app.post("/items/", response_model=Item, status_code=201) #invia un JSON che rispetta lo schema Item e se valido status 201
def create_item(item: Item):
    try:
        return db.add(item.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    
@app.get("/items/", response_model=List[Item]) #ritorna una lista di Item
def list_items(): #Restituisce tutti i record dal CSV come lista.
    return db.read_all()

@app.get("/items/{id}", response_model=Item) #ritorna un singolo Item basato sull'id
def get_item(id: int):
    items = db.read_all()
    for i in items:
        if i["id"] == id:
            return i
    raise HTTPException(status_code=404, detail="Item non trovato")

@app.put("/items/{id}", response_model=Item)
def update_item(id: int, item: Item):
    if item.id != id: #controllo se l'ID nel body è diverso da quello nella URL
        raise HTTPException(status_code=400, detail="ID nel body diverso da quello nella URL.")

    items = db.read_all()
    for idx, r in enumerate(items):
        if r["id"] == id:
            #model_dump() converte l'oggetto Pydantic in un dict
            items[idx] = item.model_dump()
            db.write_all(items)
            return items[idx]

    raise HTTPException(status_code=404, detail=f"Item con id {id} non trovato.")