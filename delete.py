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

def delete_pokemon(owner, pokemon):
    with connection.cursor() as cursor:
    query = f"""DELETE FROM pokemon_owners 
                WHERE owner_name = '{owner}' AND pokemon_id = 
                                                    (SELECT id
                                                    FROM pokemon
                                                    WHERE name = '{pokemon}')"""
    cursor.execute(query)