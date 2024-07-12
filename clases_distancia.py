import numpy as np
import heapq
import random

class Mapa:
    def __init__(self, filas_mapa, columnas_mapa, pos_inicio, pos_final):
        self.filas_mapa = filas_mapa
        self.columnas_mapa = columnas_mapa
        self.pos_inicio = pos_inicio
        self.pos_final = pos_final

    def gen_mapa(self):
        mapa_gen = np.zeros((self.filas_mapa, self.columnas_mapa), dtype=int)

        # Mostrar posición de inicio en el mapa
        filas_ini = self.pos_inicio // self.filas_mapa
        columnas_ini = self.pos_inicio % self.columnas_mapa
        mapa_gen[columnas_ini, filas_ini] = 5

        # Mostrar posición final en el mapa
        filas_fin = self.pos_final // self.filas_mapa
        columnas_fin = self.pos_final % self.columnas_mapa
        mapa_gen[columnas_fin, filas_fin] = 6

        print("Este es el mapa inicial:\n", mapa_gen)
        return mapa_gen

    def gen_obstaculos(self, mapa_gen):
        try:
            can_obstaculos = int(input("Escriba cuántos obstáculos desea (máximo 20): "))
            while True:
                if 0 < can_obstaculos <= 20:
                    obstaculos = [(random.randint(0, self.filas_mapa - 1), random.randint(0, self.columnas_mapa - 1)) for _ in range(can_obstaculos)]
                    for x, y in obstaculos:
                        mapa_gen[x, y] = 1
                    print("Mapa con obstáculos:\n", mapa_gen)
                    return mapa_gen
                else:
                    print("La cantidad supera el límite.")
                    break
        except:
            print("lo introducido no es valido")


    def obstaculos_usuaio(self, mapa_gen):
        while True:
            cas_obstaculo = int(input("en que casilla se encuentra el obstaculo"))
            cas_obstaculo -= 1
            if 0 <= cas_obstaculo < 64:
                ubicacion = (cas_obstaculo % self.columnas_mapa, cas_obstaculo // self.filas_mapa)
                mapa_gen[ubicacion] = 2
                print(mapa_gen)
                return mapa_gen
            else:
                print("la ubicacion no es valida")


    def ver_casillas(self, mapa_gen):
        casilla_obst = np.argwhere(mapa_gen == 1)
        for casilla in casilla_obst:
            print(f"\nLa casilla en la coordenada {casilla} está ocupada.")
    
    def quitar_obstaculos(self, mapa_gen):
        ubicacion_x = int(input("cual es la ubicacion en el eje X?(0 al 63): "))
        ubicacion_y = int(input("cual es la ubicacion en el eje y?(0 al 63): "))

        mapa_gen[ubicacion_x, ubicacion_y] = 0

        print(f"el mapa actualizado es:\n", mapa_gen)

class CalculadoraRutas:
    def __init__(self, mapa_gen, inicio, fin):
        self.mapa_gen = mapa_gen
        self.inicio = inicio
        self.fin = fin

    @staticmethod
    def distancia_man(entrada, salida):
        return abs(entrada[0] - salida[0]) + abs(entrada[1] - salida[1])

    def algoritmo_Astar(self, mapa_gen, inicio, fin):
        filas, columnas = mapa_gen.shape[0], mapa_gen.shape[1]
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        heap = []
        heapq.heappush(heap, (0, inicio[0], inicio[1]))

        costo_al_momento = {inicio: 0}
        viene_de = {inicio: None}

        while heap:
            current_cost, x, y = heapq.heappop(heap)

            if (x, y) == fin:
                camino = []
                nodo = fin
                while nodo is not None:
                    camino.append(nodo)
                    nodo = viene_de[nodo]
                camino.reverse()
                return camino

            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                new_cost = current_cost + 1

                if 0 <= nx < filas and 0 <= ny < columnas and mapa_gen[nx, ny] != 1:
                    if mapa_gen[nx, ny] != 2:
                        if (nx, ny) not in costo_al_momento or new_cost < costo_al_momento[(nx, ny)]:
                            costo_al_momento[(nx, ny)] = new_cost
                            priority = new_cost + CalculadoraRutas.distancia_man((nx, ny), fin)
                            heapq.heappush(heap, (priority, nx, ny))
                            viene_de[(nx, ny)] = (x, y)

        return None

def main():
    # Definir el mapa
    filas = 8
    columnas = 8
    inicio = int(input("ingrese la casilla de la cual va a comenzar: (1 al 64)"))
    inicio -= 1
    fin = int(input("Ingrese la casilla a la cual quiere llegar: (1 al 64)"))
    fin -= 1

    # Crear instancia de la clase Mapa y generar el mapa con obstáculos
    mapa_obj = Mapa(filas, columnas, inicio, fin)
    mapa_gen = mapa_obj.gen_mapa()
    mapa_gen_con_obstaculos = mapa_obj.gen_obstaculos(mapa_gen)


    #agregar obstaculos en la matriz
    des_usuario = str(input("agregar obstaculos?(si/no): ")).lower()
    if des_usuario == "si":
        try:
            mapa_obj.obstaculos_usuaio(mapa_gen)
        except:
            print("la ubicacion no es valida")
            

    # Verificar casillas ocupadas si se desea
    ver_casillas = input("¿Desea ver las casillas ocupadas? (si/no): ").lower()
    if ver_casillas == "si":
        mapa_obj.ver_casillas(mapa_gen_con_obstaculos)
    else:
        print("No se verificaron las casillas ocupadas.")

    #quitar obstaculos en la matriz
    descicion_usuario = str(input("quiere quitar un obstaculo?(si/no): ")).lower()    
    if descicion_usuario == "si":
        try:
            mapa_obj.quitar_obstaculos(mapa_gen)
        except:
            print("la ubicacion no es valida.")

    # Convertir coordenadas de inicio y fin
    ubicacion_inicio = (inicio % filas, inicio // filas)
    ubicacion_fin = (fin % filas, fin // filas)



    # Ejecutar algoritmo A*
    calculador_rutas = CalculadoraRutas(mapa_gen_con_obstaculos, ubicacion_inicio, ubicacion_fin)
    camino_encontrado = calculador_rutas.algoritmo_Astar(mapa_gen_con_obstaculos, ubicacion_inicio, ubicacion_fin)



    if camino_encontrado:
        for camino in camino_encontrado:
            mapa_gen[camino] = 7
        print("este es el camino encontrado:\n ", mapa_gen)
    else:
        print("No se encontró un camino válido.")

if __name__ == "__main__":
    main()




