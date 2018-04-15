from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_jsglue import JSGlue
from helpers import lookup, MAX_RESULTS, lookup
from pagination import Pagination

# configure application
app = Flask(__name__)
JSGlue(app)


@app.route("/", methods=['GET'])
def index():
    """Render home-page."""
    results = lookup(query="", offset=0)
    num_results = results.pop()  # number of results - not important
    headlines = results  # list of headlines

    return render_template("index.html", headlines=headlines, num_results=num_results,
                           results_per_page=MAX_RESULTS, current_page=1)


@app.route("/search/<int:page_num>", methods=['GET', 'POST'])
def search(page_num=1):
    """Search user query."""

    if request.method == "GET":
        query = request.args.get('q').strip()
        results_per_page = request.args.get('select-results-per-page')

    else:
        query = request.form['q'].strip()
        results_per_page = request.form['select-results-per-page']

    if not query:
        query = ''

    if not results_per_page:
        results_per_page = MAX_RESULTS

    else:
        results_per_page = int(results_per_page)

    offset = (page_num - 1) * results_per_page

    results = lookup(query=query, offset=offset, max_results=results_per_page)

    num_results = results.pop()  # total matches on query string
    headlines = results  # list of headlines

    if not headlines[0]:
        headlines = None

    pages = Pagination(page_num, (num_results // MAX_RESULTS) + 1, 4, 4)

    if request.method == "GET":
        return render_template("search.html", query=query, headlines=headlines,
                               num_results=num_results, pages=pages.paginate(), current_page=page_num,
                               results_per_page=results_per_page)

    else:
        show_more = True
        if num_results < page_num * MAX_RESULTS:
            show_more = False

        return jsonify({'data': render_template("extend.html", headlines=headlines, num_results=num_results),
                        'extend': show_more})


if __name__ == '__main__':
    app.run()
