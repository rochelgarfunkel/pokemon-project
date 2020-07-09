from flask import Flask, Response, request, redirect, render_template
import json
import requests
from DB import trainer, pokemon
from external_api import pokeapi, poke_pics;


app = Flask(__name__, static_url_path='', static_folder='frontend', template_folder='frontend')


@app.route('/')
def welcome_display():
    return redirect('/home_page.html')


@app.route('/<file_path>')
def serve_static_file(file_path):
    return app.send_static_file(file_path)


@app.route('/pokemon/add', methods=['Post'])
def add_new_pokemon():
    data = request.get_json()
    if  not data.get("id") or not data.get("name") or not data.get("height") or not data.get("weight") or not data.get("type"):
        return Response("error in your data"), 400

    if pokemon.is_existent(data):
        return Response(f"the pokemon you are trying to add already exists"), 409

    pokemon.add(data)
    pokemon.add_types(data)
    return Response(f"added '{data['name']}' to pokemons"), 200


def filter_pokemon_type(the_type):
    pokemon_list = pokemon.find_by_type(the_type)
    return json.dumps({"Type": the_type, "Pokemons": pokemon_list})


def filter_pokemon_owner(the_owner):
    pokemon_list = trainer.get_pokemons(the_owner)
    return json.dumps({"Trainer": the_owner, "Pokemons": pokemon_list})


@app.route('/pokemon')
def get_pokemons():
    if request.args.get('type'):
        pokemons = filter_pokemon_type(request.args.get('type'))

    elif request.args.get('owner'):
        pokemons = filter_pokemon_owner(request.args.get('owner'))

    else: Response("Invalid request"), 400
    return Response(json.dumps({"Found": pokemons})), 200


@app.route('/pokemon', methods = ['DELETE'])
def delete_pokemon_by_trainer():
    data = request.get_json()
    trainer.delete_ownership(data['pokemon'], data['owner'])
    return Response(f"'{owner}'s ownership of '{pokemon}' delete successfuly")


@app.route('/evolve', methods = ['PUT'])
def evolve():
    if not trainer.is_pair(owner, pokemon_name):
        return Response(f"'{owner}' does not own '{pokemon_name}'"), 400
    
    pokemon_to_evolve = pokeapi.get_evolve(pokemon_name)
    trainer.delete_ownership(owner, pokemon_name)
    if pokemon_to_evolve:
        pokemon_as_dict = pokeapi.get_pokemon_data(pokemon_to_evolve)
        if not pokemon.is_existent(pokemon_as_dict):
            pokemon.add(pokemon_as_dict)
            pokemon.add_types(pokemon_as_dict)
        pokemon_id = pokemon.get_id(pokemon_name)
        trainer.add_pokemon(owner, pokemon_id)

        return Response(f"evolved {pokemon_name} to {pokemon_to_evolve}")

    return Response(f"{pokemon_name} cannot evolve")

   
@app.route('/pic', methods = ['GET'])
def get_picture():
    pokemon_name = request.args.get('pokemon')
    pokemon_id = pokemon.get_id(pokemon_name)
    return poke_pics.get_picture(pokemon_name)


@app.route('/evolve/pic')
def evolve_pic():
    pokemon_name = request.args.get('pokemon')
    new_name = pokeapi.get_evolve(pokemon_name)
    return poke_pics.evolve_pic(pokemon_name, new_name)
 

if __name__ == "__main__":
    app.run(port=3001)