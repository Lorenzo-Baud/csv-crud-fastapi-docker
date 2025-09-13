from fastapi import FastAPI #Questa classe serve per creare la tua applicazione web

test = FastAPI()             #oggetto che gestirà tutte le rotte (endpoint) della tua API

@test.get("/")           #quando arriva una richiesta HTTP GET sull’URL /, esegui la funzione sotto
def read_root():        # / è la root del sito
    return {"status": "boom"}

# Nuovo endpoint con parametro 'name'
@test.get("/hello")
def say_hello(name: str = "ospite"):        #name è un query parameter (parametro che passi nell’URL)
    return {"message": f"Ciao, {name}!"}    # = "ospite" → se non passi nulla, userà “ospite” come valore di default
                                            #FastAPI la converte in JSON
#la f serve a sostituire il valore name e non considerare le {}

# Endpoint con parametro nel percorso
@test.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Ciao, {name}!"}

#Query parameter (/hello?name=Mario) → usato per opzioni, filtri, parametri opzionali.
#Path parameter (/hello/Mario) → usato per identificare una risorsa specifica.