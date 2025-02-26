import pandas as pd
import requests
from requests_oauthlib import OAuth1
import json

consumer_key = "0ccadad2b3f1a0827b095a329868d3d16b36fbfc5acdddbb04ef6dbb5b5b35fd"
consumer_secret = "d1364aa4a1def3701cb68dde4589c50c7edf46994a62b949e68ff9934a4cb93c"
token_key = "d98165c84440d6abd0f13a2837a9abefabdd8bbe15b0f1df7bb367854a6c7099"
token_secret = "412f22a603e41ac2be58b67f7551f0f9534179d42bc285a5a4afb409fa763663"
realm = "11012044"
# Definir las columnas esperadas
columnas_correctas = [
    "external id", "LIBRO CONTABLE", "TIPO DE CAMBIO", "MONEDA",
    "DEBITO", "CREDITO", "FECHA", "NOMBRE (EMPLEADO)", "ID","CUENTA CONTABLE", "SUBSIDIARIA"
]

# Ruta del archivo CSV
csv_file = "nomina lote1.csv"  # Cambia esto por la ruta de tu archivo


# Leer el CSV con separador ';'
try:
    df = pd.read_csv(csv_file, sep=";", dtype=str, encoding="ISO-8859-1")
  # Cargar todo como string

    # Validar columnas
    if list(df.columns) != columnas_correctas:
        raise ValueError(f"Las columnas del CSV no coinciden con las esperadas: {df.columns}")

    # Convertir valores numéricos
    df["DEBITO"] = df["DEBITO"].astype(float).fillna(0)
    df["CREDITO"] = df["CREDITO"].astype(float).fillna(0)

    # Agrupar por empleado
    empleados = df.groupby("NOMBRE (EMPLEADO)")

    # URL de la API
    API_URL = f"https://11012044.suitetalk.api.netsuite.com/services/rest/record/v1/journalEntry"
    auth = OAuth1(consumer_key, 
                        client_secret=consumer_secret, 
                        resource_owner_key=token_key, 
                        resource_owner_secret=token_secret,
                        signature_method='HMAC-SHA256',
                        realm=realm,)
    headers = {
                "Content-Type": "application/json",
                "prefer": "transient"
            }

    for empleado, data in empleados:
        line_items = []
        id = ''
        for _, row in data.iterrows():
            line_items.append({
                "account": {"id": row["CUENTA CONTABLE"]},
                "debit": row["DEBITO"],
                "credit": row["CREDITO"],
                "entity": {"id": row["ID"]}  # Se usa el ID del empleado
            })
            id = row["ID"]
        # Construcción del body del request
        body = {
            "customForm": {"id": 237},  # Fijo
            "subsidiary": {"id": 3},  # Fijo
            "currency": {"id": 5},  # Fijo
            "trandate": "2025-01-30 00:00:00.000",  # Fijo
            "line": {"items": line_items},  # Solo líneas del empleado
            "accountingBookDetail": {
                "items": [{"accountingBook": {"id": 2}, "exchangeRate": 4195.6}]  # Fijo
            }
        }

        # Hacer la solicitud POST
        print(body)
        response = requests.post(API_URL, headers=headers, data=json.dumps(body), auth=auth)

        # Verificar la respuesta
        print(response.status_code)
        if response.status_code in [200, 201, 204]:
            print(f"✅ Datos enviados correctamente para empleado {empleado} id: {id}")

        #    status = "OK"
        else:
            print(response.text)
            print(f"❌ Error en la solicitud para {empleado}: {response.status_code}, {response.text}")

except Exception as e:
    print(f"⚠️ Error: {e}")