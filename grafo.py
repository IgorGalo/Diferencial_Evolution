class Grafo:

    def __init__(self, arquivo):
        self.matriz_distancias = self._carregar(arquivo)

    def _carregar(self, arquivo):
        with open(arquivo, "r") as dados:
            matriz = []
            for linha in dados:
                if linha.strip():
                    valores = []
                    for valor in linha.split():
                        valores.append(float(valor))
                    matriz.append(valores)

            return matriz


    def quantidade_vertices(self):
        return len(self.matriz_distancias)

    def distancia(self, origem, destino):
        return self.matriz_distancias[origem][destino]
