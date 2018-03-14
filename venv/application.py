from flask import Flask, render_template, request, url_for
from flask_jsglue import JSGlue
from helpers import lookup

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


@app.route("/", methods=['GET', 'POST'])
def index():
    """Render home-page."""
    results = lookup(query="")
    results.pop()  # number of results - not important
    headlines = results  # list of headlines

    return render_template("index.html", headlines=headlines)


@app.route("/search", methods=['GET', 'POST'])
def search():
    """Search user query."""
    query = str(request.form['q']).strip()          # ensure query is some kind of string
    print(query)
    results = lookup(query=query)
    num_results = results.pop()                     # total matches on query string
    headlines = results                             # list of headlines

    return render_template("search.html", query=query, headlines=headlines, num_results=num_results)
