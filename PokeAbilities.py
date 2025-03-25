import requests
import json
import time

# URL base da PokéAPI para movimentos
base_url = "https://pokeapi.co/api/v2/move"

# Primeiro, descobrir quantos movimentos existem
response = requests.get(base_url)
data = response.json()
total_moves = data['count']

# Obter todos os movimentos com informações detalhadas
moves = []
for i in range(1, total_moves + 1):
    try:
        response = requests.get(f"{base_url}/{i}")
        if response.status_code == 200:
            move_data = response.json()
            
            # Extrair as informações necessárias
            move_info = {
                "name": move_data['name'],
                "type": move_data['type']['name'],
                "power": move_data.get('power', "N/A"),
                "accuracy": move_data.get('accuracy', "N/A"),
                "pp": move_data.get('pp', "N/A"),  # Adicionado o PP
                "description": next(
                    (entry['flavor_text'] for entry in move_data['flavor_text_entries']
                     if entry['language']['name'] == 'en'),
                    "No description available"
                )
            }
            moves.append(move_info)
            print(f"Obtido: {move_info['name']} - {move_info['type']} - PP: {move_info['pp']}")

        else:
            print(f"Erro ao obter movimento ID {i}: {response.status_code}")
        
        # Respeitar o limite de requisições (rate limiting)
        time.sleep(0.7)

    except Exception as e:
        print(f"Erro ao processar movimento ID {i}: {e}")

# Salvar todas as informações em um arquivo JSON
with open("moves_detailed.json", "w") as file:
    json.dump(moves, file, indent=4)


