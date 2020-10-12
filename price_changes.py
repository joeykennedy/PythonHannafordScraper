import mysql.connector
from hannaford_product import HannafordProduct

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
query = ("SELECT * FROM products")
cursor.execute(query)

biggestIncrease = 0
biggestIncreaseString = ""
products = []

for (id, name, last_update, price, brand, category, variant, list) in cursor:
    product = HannafordProduct(id, name, last_update, price, brand, category, variant, list)
    products.append(product)

for(product) in products:
    #print("{}, {} (${}), {:%d %b %Y}. Old prices: ".format(id, name, price, last_update), end = '')
    query = ("SELECT * FROM prices where id = '{}'".format(product.id))
    cursor.execute(query)
    for(id, start_date, end_date, new_price) in cursor:
        increase = new_price - product.price
        if (increase > biggestIncrease):
            biggestIncrease = increase
            biggestIncreaseString = ("The largest price increase was for {} ({} -> {})".format(product.name, product.price, new_price))

print(biggestIncreaseString)

cursor.close()