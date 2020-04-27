import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date
from flask_session import Session


idd=0


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello", methods=["POST"])
def hello():
    nombre = request.form.get("nombre")
    pas= request.form.get("pas")
    if db.execute("SELECT * FROM usuarios WHERE username = :username AND password = :password ", {"username": nombre, "password":pas}).rowcount == 0:
       return render_template("error.html", message="usuario no encontrado.")


    registro = db.execute("SELECT * FROM telefonica ORDER BY fecha_atendio DESC").fetchone()
    global idd
    idd = registro.id
    return render_template("hello.html", registro=registro, nombre=nombre, pas=pas)



@app.route("/atendio", methods=["POST"])
def atendio():
    today = date.today()
    global idd
  



    db.execute("UPDATE telefonica SET fecha_atendio = :today WHERE id = :idd", {"today": today, "idd": idd})
    db.commit()

    registro = db.execute("SELECT * FROM telefonica ORDER BY fecha_atendio DESC").fetchone()
    idd = registro.id
    nombre= idd

    return render_template("hello.html", registro=registro,nombre=nombre)

@app.route("/noencasa", methods=["POST"])
def noencasa():
    today = date.today()
    global idd
  



    db.execute("UPDATE telefonica SET fecha_tocado = :today WHERE id = :idd", {"today": today, "idd": idd})
    db.commit()

    registro = db.execute("SELECT * FROM telefonica ORDER BY fecha_atendio DESC").fetchone()
    idd = registro.id
    nombre= idd

    return render_template("hello.html", registro=registro,nombre=nombre)



@app.route("/register.html")
def register():
#INSERT INTO usuarios (nombre, apellido, username, password) VALUES ('Mario', 'Capeluto', 'marioc','cachirula')





    return render_template("registersucess.html")







#templates
#UPDATE flights SET duration = 430 WHERE origin = 'New York' AND destination = 'London'
#INSERT INTO telefonica (telefono, direccion) VALUES ('4778-4778', 'Segurola 2000')



