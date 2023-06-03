import mysql.connector
from flask import Flask, render_template, request,redirect

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'herschel03'

app.config['MYSQL_DB'] = 'flaskdb'

def get_db():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html', users=data)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['nombre']
    email = request.form['correo']

    db = get_db()
    cursor = db.cursor()
    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    values = (name, email)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()

    return redirect('/')

@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    query = "DELETE FROM users WHERE id = %s"
    values = (user_id,)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()

    return redirect('/')

@app.route('/modify_user/<int:user_id>', methods=['POST'])
def modify_user(user_id):
    name = request.form['nombre']
    email = request.form['correo']
    db = get_db()
    cursor = db.cursor()
    query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
    values = (name,email,user_id)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()

    return redirect('/')

if __name__ == '__main__':
    app.run()
