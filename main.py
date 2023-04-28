
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

try:
    conn = psycopg2.connect("dbname='myduka' user='postgres' host='localhost' port='5433' password='njokin2023#'")
    print('connected successfuly')
except Exception as e:
    print ("I am unable to connect to the database", e)

@app.route('/')
def home():
    
    return render_template('index.html')


@app.route('/products')
def products():
    

    cur = conn.cursor()
    cur.execute("SELECT * from products;")
    rows = cur.fetchall()
    print (rows)
    return render_template('products.html', rows=rows)

@app.route('/sales')
def sales():
    

    cur = conn.cursor()
    cur.execute("SELECT * from sales;")
    row = cur.fetchall()
    print (row)
    return render_template('sales.html', row=row)

@app.route('/save-product')
def save_product():
    pass
 


app.run()
