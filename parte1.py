import csv
import requests
import time
import math

class Ciudad:
    def __init__(self, nombre_ciudad, nombre_pais):
        self.nombre_ciudad = nombre_ciudad
        self.nombre_pais = nombre_pais

class Coordenada:
    def __init__(self, latitud, longitud):
        self.latitud = latitud
        self.longitud = longitud

class CoordenadasStrategy:
    def obtener_coordenadas(self, ciudad):
        raise NotImplementedError("Este método debe ser implementado por subclases")

class CoordenadasDesdeCSV(CoordenadasStrategy):
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def obtener_coordenadas(self, ciudad):
        with open(self.csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["city"].lower() == ciudad.nombre_ciudad.lower() and row["country"].lower() == ciudad.nombre_pais.lower():
                    return Coordenada(float(row["lat"]), float(row["lng"]))
        return None

class CoordenadasDesdeAPI(CoordenadasStrategy):
    def obtener_coordenadas(self, ciudad):
        url = f"https://nominatim.openstreetmap.org/search?q={ciudad.nombre_ciudad},{ciudad.nombre_pais}&format=json"
        response = requests.get(url)
        data = response.json()
        if data:
            return Coordenada(float(data[0]["lat"]), float(data[0]["lon"]))
        return None
    
class CoordenadasMock(CoordenadasStrategy):
    def obtener_coordenadas(self, ciudad):
        mock_data = {
            "Lima": Coordenada(-12.1, -77.0),
            "Cusco": Coordenada(-13.5, -72)
        }
        return mock_data.get(ciudad.nombre_ciudad)

def calcular_distancia(coord1, coord2):
    R = 6371  # Radio de la Tierra en km
    lat1, lon1 = math.radians(coord1.latitud), math.radians(coord1.longitud)
    lat2, lon2 = math.radians(coord2.latitud), math.radians(coord2.longitud)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

class ObtenerCoordenadas:
    def __init__(self, strategy):
        self.strategy = strategy

    def obtener_coordenadas(self, ciudad):
        return self.strategy.obtener_coordenadas(ciudad)

def main():
    ciudad1 = Ciudad("Lima", "Peru")
    ciudad2 = Ciudad("Cusco", "Peru")

    strategies = {
        1: CoordenadasDesdeCSV('worldcities.csv'),
        2: CoordenadasDesdeAPI(),
        3: CoordenadasMock()
    }

    try:
        opc = int(input("Opción (1: CSV, 2: API, 3: Mock): "))
        coordenadas_strategy = strategies[opc]
    except (ValueError, KeyError):
        print("Opción no válida")
        return

    coordenadas = ObtenerCoordenadas(coordenadas_strategy)
    coord1 = coordenadas.obtener_coordenadas(ciudad1)
    coord2 = coordenadas.obtener_coordenadas(ciudad2)
    
    if coord1 and coord2:
        distancia = calcular_distancia(coord1, coord2)
        print(f"La distancia entre {ciudad1.nombre_ciudad} y {ciudad2.nombre_ciudad} es {distancia:.2f} km.")
    else:
        print("No se pudieron obtener las coordenadas de una o ambas ciudades.")

if __name__ == "__main__":
    main()
