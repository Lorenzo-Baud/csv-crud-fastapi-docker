from fastapi import FastAPI #Questa classe serve per creare la tua applicazione web

app = FastAPI()             #oggetto che gestirà tutte le rotte (endpoint) della tua API

@app.get("/")           #quando arriva una richiesta HTTP GET sull’URL /, esegui la funzione sotto
def read_root():        # / è la root del sito
    return {"status": "ok"}

# Nuovo endpoint con parametro 'name'
@app.get("/hello")
def say_hello(name: str = "ospite"):        #name è un query parameter (parametro che passi nell’URL)
    return {"message": f"Ciao, {name}!"}    # = "ospite" → se non passi nulla, userà “ospite” come valore di default
                                            #FastAPI la converte in JSON