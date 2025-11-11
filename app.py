from flask import Flask, render_template

app = Flask(__name__)
#Ian é muito viado
@app.route("/")
def home():
    return render_template("index.html")

app.run()
