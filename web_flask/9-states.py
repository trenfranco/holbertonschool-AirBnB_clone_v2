#!/usr/bin/python3
"""Flask web application"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardon_appcontext(self):
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    states = storage.all("State").values()
    return render_template("7-states_list.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    states = storage.all("State").values()
    for state in states:
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html", state=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
