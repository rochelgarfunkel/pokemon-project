import pymysql, json;
import requests;

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

def add(pokemon):
    with connection.cursor() as cursor:
        query = f"INSERT into pokemon values ({pokemon['id']}, '{pokemon['name']}', {pokemon['height']},  {pokemon['weight']})"
        cursor.execute(query)                   
        connection.commit()


def is_existent(pokemon):
    with connection.cursor() as cursor:
        query = f"""SELECT * 
                    FROM pokemon 
                    WHERE id = {pokemon['id']}"""
        cursor.execute(query) 
        return cursor.fetchall()  


def add_types(pokemon):
    for type in set(pokemon['type']):
        with connection.cursor() as cursor:
            query = f"INSERT into pokemon_types values ({pokemon['id']}, '{type}')"
            cursor.execute(query)
            connection.commit()

def find_owners(name):
    with connection.cursor() as cursor:
        query = f"""SELECT owner_name 
                    FROM pokemon_owners 
                    WHERE pokemon_id IN
                        (SELECT id 
                            FROM pokemon 
                            WHERE name = '{name}')"""
        cursor.execute(query)
        res = cursor.fetchall()
        print([dict["owner_name"] for dict in res])


def get_id(pokemon_name):
    _url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    pokemon_data = requests.get(url = _url, verify = False).json()
    return pokemon_data['id']

def find_by_type(type):
    with connection.cursor() as cursor:
        query = f"""SELECT name 
                    FROM pokemon p join pokemon_types pt
                    ON p.id = pt.pokemon_id 
                    WHERE type = '{type}'"""
        cursor.execute(query)
        res = cursor.fetchall()
        return [dict["name"] for dict in res]


