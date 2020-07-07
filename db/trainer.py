import pymysql, json;

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

def add(trainer):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM owners WHERE name = '{trainer['name']}'"
        cursor.execute(query) 
        if not cursor.fetchall():  
            query = f"INSERT into owners values ('{trainer['name']}', '{trainer['town']}')"
            cursor.execute(query)
            connection.commit()

def add_pokemon(owner, pokemon):
    with connection.cursor() as cursor: 
        query = f"INSERT into pokemon_owners values ('{owner}', {pokemon})"
        cursor.execute(query)
        connection.commit()

def get_pokemons(name):
    with connection.cursor() as cursor:
        query = f"""SELECT name 
                    FROM pokemon
                    WHERE id IN
                        (SELECT pokemon_id
                        FROM pokemon_owners
                        WHERE owner_name = '{name}')"""
                        
        cursor.execute(query)
        res = cursor.fetchall()
        return([dict["name"] for dict in res])

def is_owner(owner):
    with connection.cursor() as cursor: 
        query = f"""SELECT * 
                    FROM owners 
                    WHERE name = '{owner}"""
        cursor.execute(query)
        return cursor.fetchall()

def is_pair(owner, pokemon):
    with connection.cursor() as cursor: 
        query = f"""SELECT * 
                    FROM pokemon_owners 
                    WHERE owner_name = '{owner}' AND pokemon_id =
                                        (SELECT id 
                                         FROM pokemon 
                                         WHERE name = '{pokemon}')"""
        cursor.execute(query)
        return cursor.fetchall()

def delete_ownership(owner, pokemon):
    with connection.cursor() as cursor:
        query = f"""DELETE FROM pokemon_owners 
                    WHERE owner_name = '{owner}' AND pokemon_id = 
                                                        (SELECT id
                                                        FROM pokemon
                                                        WHERE name = '{pokemon}')"""
        cursor.execute(query)
        connection.commit()