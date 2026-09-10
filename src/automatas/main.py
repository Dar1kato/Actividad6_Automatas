from typing import Dict, List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AFD:
    def __init__(self, cadena: str, transiciones: dict):
        self.cadena: list = list(cadena)
        self.nodo_actual: int = 0
        self.transiciones: dict = transiciones
        self.cadena_valida: bool = False

    def evaluar_cadena(self) -> bool:
        self.cadena.append("")

        for caracter in self.cadena:
            if caracter == "":
                for transicion in self.transiciones.get(str(self.nodo_actual), []):
                    if transicion[0] == caracter:
                        self.cadena_valida = True
                        break

                return self.cadena_valida

            for transicion in self.transiciones.get(str(self.nodo_actual), []):
                if transicion[0] == caracter:
                    self.nodo_actual = int(transicion[1])

        return self.cadena_valida

class AFND:
    def __init__(self, cadena: str, transiciones: dict):
        self.cadena: list = list(cadena)
        self.nodos_actuales: set = {0}
        self.transiciones: dict = transiciones
        self.cadena_valida: bool = False

    def evaluar_cadena(self) -> bool:
        self.cadena.append("")

        for caracter in self.cadena:
            if caracter == "":
                for nodo in self.nodos_actuales:
                    for transicion in self.transiciones.get(str(nodo), []):
                        if transicion[0] == "":
                            self.cadena_valida = True
                            break
                    if self.cadena_valida:
                        break

                return self.cadena_valida

            siguientes_nodos = set()
            
            for nodo in self.nodos_actuales:
                for transicion in self.transiciones.get(str(nodo), []):
                    if transicion[0] == caracter:
                        siguientes_nodos.add(int(transicion[1]))
            
            self.nodos_actuales = siguientes_nodos
            
            if not self.nodos_actuales:
                return False

        return self.cadena_valida

dictionary_afd = {
    "0": [["a", "0"], ["b", "1"], ["", "1"]],
    "1": [["a", "0"], ["b", "2"], ["", "2"]],
    "2": [["a", "0"], ["b", "3"], ["", "3"]],
    "3": [["a", "3"], ["b", "3"]]
}

dictionary_afnd = {
    "0": [["a", "0"], ["b", "0"], ["b", "1"]],
    "1": [["b", "2"]],
    "2": [["", "2"]]
}

class AFDRequest(BaseModel):
    cadena: str
    transiciones: Dict[str, List[List[str]]] = dictionary_afd

class AFNDRequest(BaseModel):
    cadena: str
    transiciones: Dict[str, List[List[str]]] = dictionary_afnd

@app.post("/automata/afd/evaluar")
def evaluar_afd(parametro: AFDRequest):
    automata = AFD(parametro.cadena, parametro.transiciones)
    es_valida = automata.evaluar_cadena()
    
    return {
        "Tipo": "AFD",
        "cadena": parametro.cadena,
        "nodo_final": automata.nodo_actual,
        "cadena_valida": es_valida,
        "resultado": "Cadena Valida" if es_valida else "Cadena Invalida"
    }

@app.post("/automata/afnd/evaluar")
def evaluar_afnd(parametro: AFNDRequest):
    automata = AFND(parametro.cadena, parametro.transiciones)
    es_valida = automata.evaluar_cadena()
    
    return {
        "Tipo": "AFND",
        "cadena": parametro.cadena,
        "nodos_finales": list(automata.nodos_actuales),
        "cadena_valida": es_valida,
        "resultado": "Cadena Valida" if es_valida else "Cadena Invalida"
    }