from pydantic import BaseModel, field_validator, StringConstraints
from typing_extensions import Annotated #per esprimere i vincoli in Pydantic

class Item(BaseModel):
    id: int #campo obbligatorio di tipo intero, Pydantic provea a convertire "1" -> 1 altrimenti da errore
    nome: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    #stringa di lunghezza minima 1 e leva gli spazi iniziali/finali prima di validare la lunghezza
    cognome: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] 
    codice_fiscale: Annotated[str, StringConstraints(pattern=r'^[A-Z0-9]{16}$')] #regex 
    #stringa di 16 caratteri solo maiuscoli alfanumerici senza spazi o minuscole

    @field_validator("codice_fiscale", mode="before")
    #Definisce un validatore per il campo codice_fiscale, eseguito prima degli altri controlli Pydantic (quindi prima della regex). 
    #Questo ci permette di trasformare l’input e poi validarlo.
    @classmethod
    def to_upper(cls, v): #cls rappresenta la classe stessa
        return v.upper() if isinstance(v, str) else v
