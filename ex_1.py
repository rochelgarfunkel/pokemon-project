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

def getMax():
    try:
        with connection.cursor() as cursor:
            query = f"""SELECT name, weight
                        FROM pokemon 
                        WHERE weight IN 
                            (SELECT MAX(weight) 
                             FROM pokemon)"""
            cursor.execute(query)
            res = cursor.fetchone()
            print(res["name"], res["weight"])
    except Exception as e:
        print("Error", str(e))

if __name__ == "__main__":
   getMax()