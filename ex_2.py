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

def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            query = f"""SELECT name 
                        FROM pokemon p join pokemon_types pt
                        ON p.id = pt.pokemon_id 
                        WHERE type = '{type}'"""
            cursor.execute(query)
            res = cursor.fetchall()
            return [dict["name"] for dict in res]

    except Exception as e:
        print("Error", str(e))

if __name__ == "__main__":
   print(find_by_type("grass"))