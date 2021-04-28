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

@app.route("/datapengguna",  methods=["POST","GET"])
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


@app.route("/datakriteria", methods=["POST","GET"])
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


@app.route("/datasekolah", methods=["POST","GET"])
def datasekolah():
    if request.method=="POST" and request.form["_method"]=="POST":
        return str(request.form["json"])
    elif request.method=="POST" and request.form["_method"]=="PUT":
        return "put"
    elif request.method=="POST" and request.form["_method"]=="DELETE":
        return 'delete'
    elif request.method=="GET":
        mydb.connect()
        cursor = mydb.cursor()
        
        cursor.execute("SELECT * FROM kriteria")
        kriteria = cursor.fetchall()

        cursor.execute("SELECT * FROM sekolah")
        sekolah = cursor.fetchall()

        cursor.close()
        mydb.close()


        columns = []
        for x in kriteria:
            columns.append({
                "field":x[1],
                "title":x[1]
            })

        school = []
        for j in sekolah:
            school.append(json.loads(j[1]))
    

        return render_template("datasekolah.html",kriteria=kriteria,columns=json.dumps(columns),data=json.dumps(school))

@app.route("/datarule", methods=["POST","GET"])
def datarule():
    if request.method=="POST" and request.form["_method"]=="POST":
        return 'post'
    elif request.method=="POST" and request.form["_method"]=="PUT":
        return "put"
    elif request.method=="POST" and request.form["_method"]=="DELETE":
        return 'delete'
    elif request.method=="GET":
        mydb.connect()
        cursor = mydb.cursor()
        
        cursor.execute("SELECT rule.*, kriteria.nama_kriteria FROM rule INNER JOIN kriteria ON rule.id_kriteria=kriteria.id_kriteria")
        row = cursor.fetchall()

        cursor.execute("SELECT * FROM kriteria")
        kriteria = cursor.fetchall()

        cursor.close()
        mydb.close()

        payload = [];

        for x in row:
            payload.append({
                "id_rule":x[0],
                "id_kriteria":x[1],
                "nama_kriteria":x[4],
                "rule":x[2],
                "nilai":x[3],
            })
        

        return render_template("datarule.html", data=json.dumps(payload), kriteria=kriteria)


if __name__=='__main__':
    app.run(debug=True)