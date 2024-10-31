import os
import requests
from dotenv import load_dotenv

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")

if not MAPBOX_TOKEN:
    raise ValueError("MAPBOX_TOKEN não encontrado. Verifique seu arquivo .env.")


def geolocation_function(enderecos):
    resultados = []

    for endereco in enderecos:
        endereco_completo = f"{endereco}, Fortaleza, Ceará"
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{endereco_completo}.json"

        params = {
            'access_token': MAPBOX_TOKEN,
            'bbox': '-38.6351,-3.8950,-38.3195,-3.6706',
            'limit': 1
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'features' in data and data['features']:
                coordinates = data['features'][0]['geometry']['coordinates']
                longitude, latitude = coordinates
                resultados.append({
                    "endereco": endereco_completo,
                    "latitude": latitude,
                    "longitude": longitude
                })
            else:
                resultados.append({
                    "endereco": endereco_completo,
                    "erro": "Nenhum resultado encontrado"
                })

        except requests.RequestException as e:
            resultados.append({
                "endereco": endereco_completo,
                "erro": f"Erro ao fazer a requisição: {e}"
            })

    return resultados
