from flask import Flask, render_template
# import connexion
import uvicorn

import config
from models import Person

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")


# app = Flask(__name__)

# app = connexion.App(__name__, specification_dir="./")
# app.add_api("swagger.yml")


@app.route("/")
def home():
    people = Person.query.all()

    return render_template("home.html", people=people)


if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8000, debug=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
