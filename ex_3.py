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

def findOwners(name):
    try:
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
    except Exception as e:
        print("Error", str(e))

if __name__ == "__main__":
   findOwners("gengar")
