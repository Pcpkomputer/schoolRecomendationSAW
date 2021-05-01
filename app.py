from flask import Flask, render_template, request, redirect, url_for, session
import json
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="rekomendasisekolahSAW"
)

app = Flask(__name__)

app.secret_key="ini rahasia"

@app.route("/logout")
def logout():
    session.pop("email")
    session.pop("nama")
    session.pop("role")
    return redirect(url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    if 'role' in session:
        return redirect(url_for("index"))
    if request.method=="POST":
        email = request.form["email"]
        password = request.form["password"]

        mydb.connect()
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM pengguna WHERE email=%s",(email,))
        user = cursor.fetchone()

        mydb.commit()
        cursor.close()
        mydb.close()

        if user==None:
            return render_template("login.html",error="Tidak ditemukan user tersebut...")
        
        if user[2]==email and user[3]==password:
            session["email"]=user[2]
            session["nama"]=user[1]
            session["role"]=user[4]
            return redirect(url_for("index"))
        else:
            return render_template("login.html",error="Password yang dimasukkan salah...")

    return render_template("login.html")

@app.route("/")
def index():

    if 'role' in session and session["role"]=="admin" or 'role' in session and session["role"]=="user":
        mydb.connect()
        cursor = mydb.cursor()

        cursor.execute("SELECT COUNT(*) FROM pengguna")
        totalpengguna = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM sekolah")
        totalsekolah = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM kriteria")
        totalkriteria = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM rule")
        totalrule = cursor.fetchone()

        mydb.commit()
        cursor.close()
        mydb.close()

        return render_template("index.html",nama=session["nama"], role=session["role"], totalpengguna=totalpengguna, totalsekolah=totalsekolah, totalkriteria=totalkriteria, totalrule=totalrule)

    else:
        return redirect(url_for("login"))

   
@app.route("/datapengguna",  methods=["POST","GET"])
def datapengguna():
    if 'role' in session:
        if session["role"]=="user":
            return "cih user"
        if request.method=="POST" and request.form["_method"]=="POST":
            nama = request.form["nama"]
            email = request.form["email"]
            password = request.form["password"]
            role = request.form["role"]

            mydb.connect()
            cursor = mydb.cursor()

            cursor.execute("SELECT * FROM pengguna WHERE email=%s",(email,));
            emailExist = cursor.fetchall()

            print(emailExist)
            if emailExist != None:
                return "Email sudah dipakai..."
            cursor.execute("INSERT INTO pengguna VALUES (NULL,%s,%s,%s,%s)",(nama,email,password,role))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datapengguna"))

        elif request.method=="POST" and request.form["_method"]=="PUT":
            id = request.form["id"]
            nama = request.form["nama"]
            email = request.form["email"]
            password = request.form["password"]
            role = request.form["role"]

            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("UPDATE pengguna SET nama=%s,email=%s,password=%s,role=%s WHERE id_pengguna=%s",(nama,email,password,role,id))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datapengguna"))
        elif request.method=="POST" and request.form["_method"]=="DELETE":
            id = request.form["id"]
        
            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM pengguna WHERE id_pengguna=%s",(id,))
            mydb.commit()
            cursor.close()
            mydb.close()


            return redirect(url_for("datapengguna"))
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

            return render_template("datapengguna.html",nama=session["nama"], data=json.dumps(payload))
    else:
        return redirect(url_for("login"))


@app.route("/datakriteria", methods=["POST","GET"])
def datakriteria():
    if 'role' in session:
        if session["role"]=="user":
            return "cih user"
        if request.method=="POST" and request.form["_method"]=="POST":
            name = request.form["nama"]
            tipe = request.form["tipe"]
            bobot = request.form["bobot"]

            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO kriteria VALUES (NULL,%s,%s,%s)",(name,tipe,bobot))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datakriteria"))
        elif request.method=="POST" and request.form["_method"]=="PUT":
            id = request.form["id"]
            name = request.form["nama"]
            tipe = request.form["tipe"]
            bobot = request.form["bobot"]

            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("UPDATE kriteria SET nama_kriteria=%s,tipe=%s,bobot=%s WHERE id_kriteria=%s",(name,tipe,bobot,id))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datakriteria"))
        elif request.method=="POST" and request.form["_method"]=="DELETE":

            id = request.form["id"]

            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM kriteria WHERE id_kriteria=%s",(id,))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datakriteria"))
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

            return render_template("datakriteria.html",nama=session["nama"], data=json.dumps(payload))
    else:
        return redirect(url_for("login"))

@app.route("/datasekolah", methods=["POST","GET"])
def datasekolah():
    if 'role' in session:
        if session["role"]=="user":
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
                p = json.loads(j[1])
                p["ID Sekolah"]=j[0]
                school.append(p)
        

            return render_template("datasekolah.html",nama=session["nama"],role=session["role"],kriteria=kriteria,columns=json.dumps(columns),data=json.dumps(school))
        if request.method=="POST" and request.form["_method"]=="POST":

            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO sekolah VALUES (UUID(),%s)",(request.form["json"],))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datasekolah"))
        elif request.method=="POST" and request.form["_method"]=="PUT":
            id = request.form["id"]
            json_ = request.form["json"]

            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("UPDATE sekolah SET json=%s WHERE id_sekolah=%s",(json_,id))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datasekolah"))
        elif request.method=="POST" and request.form["_method"]=="DELETE":
            id = request.form["id"]

            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM sekolah WHERE id_sekolah=%s",(id,))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datasekolah"))
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
                p = json.loads(j[1])
                p["ID Sekolah"]=j[0]
                school.append(p)
        

            return render_template("datasekolah.html",nama=session["nama"],role=session["role"],kriteria=kriteria,columns=json.dumps(columns),data=json.dumps(school))
    else:
        return redirect(url_for("login"))
@app.route("/datarule", methods=["POST","GET"])
def datarule():
    if 'role' in session:
        if session["role"]=="user":
            return "cih user"
        if request.method=="POST" and request.form["_method"]=="POST":
            id = request.form["id"]
            rule = request.form["rule"]
            nilai = request.form["nilai"]
            
            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO rule VALUES (UUID(),%s,%s,%s)",(id,rule,nilai))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datarule"))
        elif request.method=="POST" and request.form["_method"]=="PUT":

            id = request.form["id"]
            rule = request.form["rule"]
            nilai = request.form["nilai"]
            
            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("UPDATE rule SET rule=%s,nilai=%s WHERE id_rule=%s",(rule,nilai,id))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datarule"))
        elif request.method=="POST" and request.form["_method"]=="DELETE":

            id = request.form["id"]
    
            mydb.connect()
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM rule WHERe id_rule=%s",(id,))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for("datarule"))
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
            

            return render_template("datarule.html",nama=session["nama"], data=json.dumps(payload), kriteria=kriteria)
    else:
        return redirect(url_for("login"))

@app.route("/perangkingan", methods=["POST","GET"])
def perangkingan():
    if 'role' in session:
        if request.method=="POST":

            mydb.connect()
            cursor = mydb.cursor()

            cursor.execute("SELECT * FROM sekolah")
            sekolah = cursor.fetchall()

            cursor.execute("SELECT rule.*, kriteria.nama_kriteria FROM rule INNER JOIN kriteria ON rule.id_kriteria=kriteria.id_kriteria")
            rule = cursor.fetchall()

            cursor.execute("SELECT * FROM kriteria")
            kriteria = cursor.fetchall()

            cursor.close()
            mydb.close()

            school = []
            for j in sekolah:
                p = json.loads(j[1])
                p["ID Sekolah"]=j[0]
                school.append(p)


            return render_template("perangkingan.html",role=session["role"],nama=session["nama"],sekolah=json.dumps(school),kriteria=json.dumps(kriteria),rule=json.dumps(rule))
        return render_template("perangkingan.html", role=session["role"], nama=session["nama"])
    else:
        return redirect(url_for("login"))

if __name__=='__main__':
    app.run(debug=True)