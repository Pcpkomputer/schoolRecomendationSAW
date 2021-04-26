from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/datapengguna",  methods=["POST","GET","PUT","DELETE"])
def datapengguna():
    return render_template("datapengguna.html")


@app.route("/datakriteria", methods=["POST","GET","PUT","DELETE"])
def datakriteria():
    return render_template("datakriteria.html")

@app.route("/datarule", methods=["POST","GET","PUT","DELETE"])
def datarule():
    return render_template("datarule.html")

if __name__=='__main__':
    app.run(debug=True)