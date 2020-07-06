import pymysql, json;

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
    with open("pokemon_data.json") as file:
        return json.load(file)

def is_existent(pokemon):
    query = f"""SELECT * 
                FROM pokemon 
                WHERE id = {pokemon['id']}"""
    cursor.execute(query) 
    return cursor.fetchall()       

def add_pokemon(pokemon):
    with connection.cursor() as cursor:
        query = f"INSERT into pokemon values ({pokemon['id']}, '{pokemon['name']}', {pokemon['height']},  {pokemon['weight']})"
        cursor.execute(query)                   
        connection.commit()

def insert_pokemon():
    data = open_file()
    for pokemon in data:
        if not is_existent(pokemon):
            add_pokemon(pokemon)

def add_owner(owner):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM owners WHERE name = '{owner['name']}'"
        cursor.execute(query) 
        if not cursor.fetchall():  
            query = f"INSERT into owners values ('{owner['name']}', '{owner['town']}')"
            cursor.execute(query)
            connection.commit()


def insert_owners():
    data = open_file()

    for owners in data:
        for owner in owners["ownedBy"]:
            add_owner(owner)

def add_pokemon_owner(owner, pokemon):
    with connection.cursor() as cursor: 
        query = f"INSERT into pokemon_owners values ('{owner}', {pokemon})"
        cursor.execute(query)
        connection.commit()   

def insert_pokemon_owners():
    with open("pokemon_data.json") as file:
        data = json.load(file)

    for pokemon in data:
        for owner in pokemon["ownedBy"]:
            add_pokemon_owner(owner['name'], pokemon['id'])

def add_types(pokemon):
    for type in set(pokemon['type']):
        with connection.cursor() as cursor:
            query = f"INSERT into pokemon_types values ({pokemon['id']}, '{type}')"
            cursor.execute(query)
            connection.commit()

def insert_pokemon_types():
    with open("pokemon_data.json") as file:
        data = json.load(file)

    for pokemon in data:
        add_types(pokemon)


if __name__ == "__main__":
    insert_pokemon()
    insert_owners()
    insert_pokemon_owners()
    insert_pokemon_types()


