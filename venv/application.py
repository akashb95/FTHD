from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_jsglue import JSGlue
from helpers import lookup, MAX_RESULTS
from pagination import Pagination

# configure application
app = Flask(__name__)
JSGlue(app)


@app.route("/", methods=['GET'])
def index():
    """Render home-page."""
    results = lookup(query="")
    num_results = results.pop()  # number of results - not important
    headlines = results  # list of headlines

    return render_template("index.html", headlines=headlines, num_results=num_results,
                           results_per_page=MAX_RESULTS, current_page=1)


@app.route("/search/<int:page_num>", methods=['GET', 'POST'])
def search(page_num=1):
    """Search user query."""
    offset = (page_num - 1) * MAX_RESULTS

    query = request.args.get('q').strip()  # ensure query is some kind of string

    results = lookup(query=query, offset=offset, max_results=MAX_RESULTS)

    num_results = results.pop()  # total matches on query string
    headlines = results  # list of headlines

    if not headlines[0]:
        headlines = None

    pages = Pagination(page_num, (num_results // MAX_RESULTS) + 1, 4, 4)

    return render_template("search.html", query=query, headlines=headlines,
                           num_results=num_results, pages=pages.paginate(), current_page=page_num,
                           results_per_page=MAX_RESULTS)


@app.route("/extend/<int:page_num>", methods=["POST"])
def extend(page_num):
    offset = (page_num - 1) * MAX_RESULTS
    query = request.form['q'].strip()  # ensure query is some kind of string

    results = lookup(query=query, offset=offset, max_results=MAX_RESULTS)

    num_results = results.pop()     # total matches on query string
    headlines = results             # list of headlines
    show_more = True

    if not headlines[0]:
        headlines = None

    if num_results < page_num * MAX_RESULTS:
        show_more = False

    return jsonify({'data': render_template("extend.html", headlines=headlines,
                                            num_results=num_results),
                    'extend': show_more})


if __name__ == '__main__':
    app.run()
