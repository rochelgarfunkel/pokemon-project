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

def find_roster(name):
    try:
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
    except Exception as e:
        print("Error", str(e))

if __name__ == "__main__":
   find_roster("Loga")