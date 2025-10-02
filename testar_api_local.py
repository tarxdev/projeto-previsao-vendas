import requests
import json

URL_API = "http://127.0.0.1:5000/predict"

dados_para_prever = {
    "data": [
        {
            "data_da_previsao": "2025-10-02",
            "id_produto": "PROD001" 
        },
        {
            "data_da_previsao": "2025-10-02",
            "id_produto": "PROD002"
        }
    ]
}

headers = {"Content-Type": "application/json"}

response = requests.post(URL_API, data=json.dumps(dados_para_prever), headers=headers)

if response.status_code == 200:
    previsoes = response.json()
    print("--- Requisição enviada com sucesso! ---")
    print(f"Previsão de vendas para Notebook Gamer: {previsoes[0]:.0f} unidades")
    print(f"Previsão de vendas para Mouse Sem Fio: {previsoes[1]:.0f} unidades")
else:
    print(f"Erro ao fazer a requisição. Status: {response.status_code}")
    print(f"Resposta: {response.text}")