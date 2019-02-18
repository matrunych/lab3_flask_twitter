from flask import Flask, render_template, request
from web_map import data, create_map

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/map", methods=["POST"])
def info():
    user = str(request.form.get("name"))
    if len(user.split()) > 1:
        return render_template("failure.html")
    else:
        lst_data = data(user)
        create_map(lst_data)
        return render_template("map.html")


if __name__ == "__main__":
    app.run(debug=True)
