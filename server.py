import pymysql, json;

from flask import Flask, Response, request 
import requests;

from db import pokemon, trainer;
import external_api;

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if connection.open:
    print("the connection is opened")

app = Flask(__name__, static_url_path = '', static_folder = 'frontend')

@app.route('/')
def welcome():
    return Response("Welcome to the Pokemon Game!!!!!!!")


@app.route('/pokemon/add', methods=['Post'])
def add_new_pokemon():
    data = request.get_json()
    if  not data.get("id") or not data.get("name") or not data.get("height") or not data.get("weight") or not data.get("type"):
        return Response("error in your data", 400)

    if pokemon.is_existent(data):
        return Response(f"the pokemon you are trying to add already exists")

    pokemon.add(data)
    pokemon.add_types(data)
    return Response(f"added '{data['name']}' to pokemons")


@app.route('/pokemon/find_by_type/<type>')
def get_pokemon_by_type(type):
    res = pokemon.find_by_type(type)
    return json.dumps(res)
   

@app.route('/pokemon', methods=['Delete'])  
def delete_pokemon_owner():
    data = request.get_json()
    owner = data["owner"]
    pokemon = data["pokemon"]
    pokemon.delete_ownership(owner, pokemon)
    return Response(f"'{owner}'s ownership of '{pokemon}' delete successfuly")
 
    
@app.route('/pokemon/get_pokemons/<name>')
def get_pokemon_by_trainer(name):
    res = trainer.get_pokemons(name)
    return json.dumps(res)


@app.route('/evolve/<owner>/<pokemon_name>', methods=['Put'])
def evolve(owner, pokemon_name):
    if not trainer.is_pair(owner, pokemon_name):
        return Response(f"'{owner}' does not own '{pokemon_name}'")

    pokemon_to_evolve = external_api.get_evolve(pokemon_name)
    trainer.delete_ownership(owner, pokemon_name)
    if pokemon_to_evolve:
        pokemon_as_dict = external_api.get_pokemon_data(pokemon_to_evolve)
        if not pokemon.is_existent(pokemon_as_dict):
            pokemon_as_dict = external_api.get_pokemon_data(pokemon_to_evolve)
            pokemon.add(pokemon_as_dict)
            pokemon.add_types(pokemon_as_dict)
        pokemon_id = pokemon.get_id(pokemon_name)
        trainer.add_pokemon(owner, pokemon_id)

        return Response(f"evolved {pokemon_name} to {pokemon_to_evolve}")

    return Response(f"{pokemon_name} cannot evolve")


if __name__ == '__main__':
    app.run(port = 3000)
