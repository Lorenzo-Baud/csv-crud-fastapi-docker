from fastapi import FastAPI, HTTPException
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