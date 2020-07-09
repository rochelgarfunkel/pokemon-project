import json, requests

def get_evolve(pokemon):
    _url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    pokemon_data = requests.get(url = _url, verify = False).json() 
    species_url = pokemon_data["species"]["url"]
    species_data = requests.get(url = species_url, verify = False).json()
    resource_url = species_data["evolution_chain"]["url"]
    resource_data = requests.get(url = resource_url, verify = False).json()["chain"]

    while len(resource_data["evolves_to"]):
        if resource_data["species"]["name"] == pokemon:
            return resource_data["evolves_to"][0]["species"]["name"]
        resource_data = resource_data["evolves_to"][0]
    return None

def get_pokemon_data(pokemon):

    _url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    pokemon_data = requests.get(url = _url, verify = False).json()
    pokemon_dict = {}
    pokemon_dict['id'] = pokemon_data['id']
    pokemon_dict['name'] = pokemon
    pokemon_dict['height'] = pokemon_data['height']
    pokemon_dict['weight'] = pokemon_data['weight']
    pokemon_dict['type'] = pokemon_data['types']
    return pokemon_dict