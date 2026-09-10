class AFD:
    def __init__(self, cadena: str, transiciones: dict):
        self.cadena: list = list(cadena)
        self.nodo_actual: int = 0
        self.transiciones: dict = transiciones
        self.cadena_valida: bool = False

    def evaluar_cadena(self):
        self.cadena.append("")

        for caracter in self.cadena:
            if caracter == "":
                for transicion in self.transiciones[str(self.nodo_actual)]:
                    if transicion[0] == caracter:
                        self.cadena_valida = True
                        break

                if self.cadena_valida:
                    print("Cadena Valida")
                else:
                    print("Cadena Invalida")
                return

            for transicion in self.transiciones[str(self.nodo_actual)]:
                if transicion[0] == caracter:
                    self.nodo_actual = int(transicion[1])    


class AFND:
    def __init__(self, cadena: str, transiciones: dict):
        self.cadena: list = list(cadena)
        self.nodos_actuales: set = {0} 
        self.transiciones: dict = transiciones
        self.cadena_valida: bool = False

    def evaluar_cadena(self):
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

                if self.cadena_valida:
                    print("Cadena Valida")
                else:
                    print("Cadena Invalida")
                return

            siguientes_nodos = set()
            
            for nodo in self.nodos_actuales:
                for transicion in self.transiciones.get(str(nodo), []):
                    if transicion[0] == caracter:
                        siguientes_nodos.add(int(transicion[1]))
            
            self.nodos_actuales = siguientes_nodos
            
            if not self.nodos_actuales:
                print("Cadena Invalida")
                return

dictionary_afnd = {
    "0": [["a", "0"], ["b", "0"], ["b", "1"]],  
    "1": [["b", "2"]],
    "2": [["", "2"]]                            
}

automata_afnd = AFND("bbb", dictionary_afnd)
automata_afnd.evaluar_cadena()


dictionary_afd = {
    "0": [["a", "0"], ["b", "1"], ["", "1"]],
    "1": [["a", "0"], ["b", "2"], ["", "2"]],
    "2": [["a", "0"], ["b", "3"], ["", "3"]],
    "3": [["a", "3"], ["b", "3"]]
}

automata_afd = AFD("bbb", dictionary_afd)
automata_afd.evaluar_cadena()
