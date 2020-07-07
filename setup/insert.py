import pymysql, json;
from db import pokemon;
from db import trainer;
from flask import Response;

def insert_data():
    insert_pokemon()
    insert_owners()
    insert_pokemon_owners()
    insert_pokemon_types()

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

def open_file():
    with open("setup/pokemon_data.json") as file:
        return json.load(file)

     
def insert_pokemon():
    data = open_file()
    for pokemon_data in data:
        if  not data.get("id") or not data.get("name") or not data.get("height") or not data.get("weight") or not data.get("type"):
            return Response("error in your data", 400)

        if pokemon.is_existent(pokemon_data):
            return Response("the pokemon you are trying to insert already exists!", 409)

        pokemon.add(pokemon_data)


def insert_owners():
    data = open_file()
    for owners in data:
        for owner in owners["ownedBy"]:
            if trainer.is_owner(owner):
                return Response("the owner you are trying to insert already exists!", 409)

            trainer.add(owner)
   

def insert_pokemon_owners():
    data = open_file()
    for pokemon_data in data:
        for owner in pokemon_data["ownedBy"]:
            if trainer.is_pair(owner['name'], pokemon['id']):
                return Response(f"{owner['name']} already ownes {pokemon_data['id']}")
            trainer.add_pokemon(owner['name'], pokemon_data['id'])


def insert_pokemon_types():
    data = open_file()
    for pokemon_data in data:
        pokemon.add_types(pokemon_data)




