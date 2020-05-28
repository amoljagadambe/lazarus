from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
import os

BASE_DIR = os.getcwd()

app = Flask(__name__)
db = yaml.load(open('E:/Projects/flask-application/application/resources/db-connect/db.yml.yaml'),
               Loader=yaml.BaseLoader)
print(db)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,email)VALUES(%s,%s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM product")

    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)


if __name__ == "__main__":
    app.run()
