from flask import Flask, render_template, request
import json
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="rekomendasisekolahSAW"
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/datapengguna",  methods=["POST","GET","PUT","DELETE"])
def datapengguna():
    if request.method=="POST" and request.form["_method"]=="POST":
        nama = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        return 'post'
    elif request.method=="POST" and request.form["_method"]=="PUT":
        id = request.form["id"]
        nama = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        return "put"
    elif request.method=="POST" and request.form["_method"]=="DELETE":
        id = request.form["id"]
        return 'delete'
    elif request.method=="GET":
        mydb.connect()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM pengguna")
        row = cursor.fetchall()
        cursor.close()
        mydb.close()

        payload = [];

        for x in row:
            payload.append({
                "id":x[0],
                "nama":x[1],
                "email":x[2],
                "password":x[3],
                "role":x[4]
            })

        return render_template("datapengguna.html", data=json.dumps(payload))


@app.route("/datakriteria", methods=["POST","GET","PUT","DELETE"])
def datakriteria():
    if request.method=="POST" and request.form["_method"]=="POST":
        return 'post'
    elif request.method=="POST" and request.form["_method"]=="PUT":
        return "put"
    elif request.method=="POST" and request.form["_method"]=="DELETE":
        return 'delete'
    elif request.method=="GET":
        mydb.connect()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM kriteria")
        row = cursor.fetchall()
        cursor.close()
        mydb.close()

        payload = [];

        for x in row:
            payload.append({
                "id":x[0],
                "nama":x[1],
                "tipe":x[2],
                "bobot":x[3],
            })

        return render_template("datakriteria.html", data=json.dumps(payload))
    return render_template("datakriteria.html")

@app.route("/datarule", methods=["POST","GET","PUT","DELETE"])
def datarule():
    return render_template("datarule.html")

if __name__=='__main__':
    app.run(debug=True)