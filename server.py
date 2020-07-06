import pymysql, json;

from flask import Flask, Response, request 
import requests;
from insert import add_pokemon, add_types, is_existent, add_pokemon_owner;
from delete import delete_pokemon;
from ex_2 import find_by_type;
from ex_4 import find_roster;

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if not connection.open:
    print("error in your connection")

app = Flask(__name__)

@app.route('/')
def welcome():
    return Response("Welcome to the Pokemon Game!!!!!!!")


@app.route('/add_pokemon', methods=['Post'])
def add_new_pokemon():
    data = request.get_json()
    if  not data.get("id") or not data.get("name") or not data.get("height") or not data.get("weight") or not data.get("type"):
        return Response("error in your data", 400)

    if is_existent(data)
        return Response(f"the pokemon you are trying to add already exists")

    add_pokemon(data)
    add_types(data)
    return Response(f"added '{data['name']}' to pokemons")


@app.route('/get_pokemon_by_type/<type>')
def get_pokemon_by_type(type):
    res = find_by_type(type)
    return json.dumps(res)
   

@app.route('/delete_pokemon', methods=['Delete'])  
def delete_pokemon_owner():
    data = request.get_json()
    owner = data["owner"]
    pokemon = data["pokemon"]
    delete_pokemon(owner, pokemon)
        return Response(f"'{owner}'s ownership of '{pokemon}' delete successfuly")
    
@app.route('/get_pokemon_by_trainer/<name>')
def get_pokemon_by_trainer(name):
    res = find_roster(name)
    return json.dumps(res)

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

@app.route('/evolve/<trainer><pokemon>', methods=['Put'])
def evolve(trainer, pokemon):
    pokemon_to_evolve = get_evolve(pokemon)
    delete_pokemon(trainer, pokemon)
    if pokemon_to_evolve:
        if not is_existent(pokemon_to_evolve):
            pokemon_as_dict = get_pokemon_data(pokemon_to_evolve)
            add_pokemon(pokemon_as_dict)
        add_pokemon_owner(trainer, pokemon)

    return Response(f"evolved '{pokemon}' to '{pokemon_to_evolve}'")



if __name__ == '__main__':
    app.run(port = 3000)
