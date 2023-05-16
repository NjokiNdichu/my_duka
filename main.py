
from flask import Flask, render_template, request, redirect
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
    cur.execute("select s.id, p.name, s.quantity, s.created_at from products as p join sales as s on s.pid=p.id")
    sales = cur.fetchall()
    cur.execute("SELECT * from products;")
    products = cur.fetchall()
    print(sales)
    
    return render_template('sales.html', sales=sales, products=products)

@app.route('/save-product', methods=['POST'])
def save_product():
        name=request.form['name']
        bp=request.form['bp']
        sp=request.form['sp']
        quantity=request.form['quantity']
        print(name, bp, sp, quantity)
        cur = conn.cursor()
        cur.execute("INSERT INTO products(name, buying_price, selling_price, quantity)values(%s, %s, %s, %s)",(name, bp, sp, quantity))
        conn.commit()

        return redirect("/products")

@app.route('/save-sales',methods=['POST'])
def save_sales():
    pid=request.form['pid']
    quantity=request.form['quantity']
    print(pid,quantity)
    cur=conn.cursor()
    
    cur.execute("INSERT INTO sales(pid,quantity,created_at)VALUES (%s, %s,%s)",(pid,quantity,"now()"))
    conn.commit()

    return redirect("/sales")

@app.route('/dashboard')
def dashboard():
 cur = conn.cursor()
 cur.execute("SELECT sum((p.selling_price*s.quantity)-(p.buying_price*s.quantity))as total,p.name FROM products as p join sales as s on s.pid=p.id group by p.name;")
 rows = cur.fetchall()
 a = []
 b = []
 for i in rows:
    a.append(i[1])
    b.append(float(i[0]))
 print(a,b)
 cur.execute("SELECT SUM(p.selling_price * s.Quantity) as salesperday,created_at FROM  products  as p JOIN sales as s ON s.pid = p.id GROUP BY created_at;")
 rows = cur.fetchall()
 c = []
 d = []
 for i in rows:
    c.append(i[1])
    d.append(float(i[0]))

 print(c,d)

 return render_template("dashboard.html",products=a,profit=b,days=c,sales=d)


app.run(debug=True)
