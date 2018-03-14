from flask import Flask, render_template, request, url_for, redirect
from flask_jsglue import JSGlue
from helpers import lookup
from pagination import Pagination

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


@app.route("/search/<int:page_num>", methods=['GET', 'POST'])
def search(page_num=1):
    """Search user query."""
    max_results = 100
    offset = (page_num - 1) * max_results
    query = str(request.args.get('q')).strip()  # ensure query is some kind of string

    results = lookup(query=query, offset=offset, max_results=max_results)

    num_results = results.pop()  # total matches on query string
    headlines = results  # list of headlines

    pages = Pagination(page_num, (num_results // max_results) + 1)

    return render_template("search.html", query=query, headlines=headlines,
                           num_results=num_results, pages=pages.paginate())
