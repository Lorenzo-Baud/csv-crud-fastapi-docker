import csv, os
from typing import List, Dict, Optional
from filelock import FileLock
#il csv_store si occupa del "database" che in questo caso è un file CSV
#senza csv_store Gli endpoint (tipo POST /items/) riceverebbero un JSON 
#e dovrebbero gestire direttamente apertura, lettura e scrittura del CSV

CSV_PATH = os.getenv("CSV_PATH", "data/items.csv")
FIELDNAMES = ["ID", "nome", "cognome", "codice_fiscale"] #definisce le colonne del CSV

def _lock():
    return FileLock(CSV_PATH + ".lock") #crea un lock per evitare accessi concorrenti

def ensure_csv_exists() -> None: #crea il file CSV se non esiste con l'header giusto
    os.makedirs(os.path.dirname(CSV_PATH) or ".", exist_ok=True) #crea la cartella se non esiste
    if not os.path.exists(CSV_PATH): #se il file non esiste lo crea
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()

def read_all() -> List[Dict]:
    ensure_csv_exists()
    with _lock(): #il with chiama automaticamente __enter__ per provare ad acquisire il lock appena è disponibile
        with open(CSV_PATH, newline="", encoding="utf-8") as f: #apre il file in lettura
            reader = csv.DictReader(f) #Crea un lettore che restituisce ogni riga come dict usando l’header come chiavi
            rows: List[Dict] = []
            for r in reader:
                rows.append({
                    "id": int(r["ID"]),
                    "nome": r["nome"],
                    "cognome": r["cognome"],
                    "codice_fiscale": r["codice_fiscale"],
                })
            return rows #ritorna la lista completa dei record(righe del CSV)
        #rilascia il lock appena il blocco finisce

def write_all(rows: List[Dict]) -> None: #sovrascrive tutto il CSV con i record passati
    with _lock():
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES) #Crea uno scrittore che usa l’header specificato
            writer.writeheader() #scrive la riga di header all'inizio del file
            for r in rows:
                writer.writerow({ #Scrive una riga nel CSV mappando le nostre chiavi interne ai nomi colonna del file
                    "ID": int(r["id"]),
                    "nome": r["nome"],
                    "cognome": r["cognome"],
                    "codice_fiscale": r["codice_fiscale"],
                })

def add(item: Dict) -> Dict:
    rows = read_all()
    if any(r["id"] == item["id"] for r in rows):
        # id deve essere univoco
        raise ValueError(f"Item con id {item['id']} esiste già.")
    rows.append(item)
    write_all(rows) #riscrive tutto il CSV con il nuovo record aggiunto
    return item
