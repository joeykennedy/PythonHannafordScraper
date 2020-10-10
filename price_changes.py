import mysql.connector

def createInstance():
    mydb = mysql.connector.connect(
    host="localhost",
    user="hannafordApp",
    password="groceryListTestPassword",
    database="hannaford_products"
    )

    #print(mydb)
    return mydb


mydb = createInstance()
cursor = mydb.cursor()
query = ("SELECT * FROM products where id = '690683'")
cursor.execute(query)

for (id, name, last_update, price, brand, category, variant, list) in cursor:
    print("{}, {} (${}), {:%d %b %Y}. Old prices: ".format(id, name, price, last_update), end = '')
    query = ("SELECT * FROM prices where id = '{}'".format(id))
    cursor.execute(query)
    for(id, start_date, end_date, price) in cursor:
        print("{},".format(price), end = '')
    print("")

cursor.close()