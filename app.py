import requests
import urllib.parse
import os
from flask import Flask, request, render_template, jsonify
from json2html import *

app = Flask(__name__)


# Return books matching URL parameters in json format
def process_query(query):
    url = os.environ["API_URL"]  # from environment variable
    params = ""
    for key, value in query.items():
        if not value:
            continue
        if not params:
            params += "?" + key + "=" + value
        else:
            params += "&" + key + "=" + value
    # print (params)
    response = requests.get(f"http://{url}{params}")

    if response.status_code == 404:
        # return("No books matching search critera", 404)
        return render_template("404.html", code=response.status_code)
    elif response.status_code == 200:
        books = response.json()
        table_html = json2html.convert(json=books)
        replacements = {
            "<th>author": "<th>Author",
            "<th>genre": "<th>Genre",
            "<th>id": "<th>ID",
            "<th>publication_year": "<th>Publication year",
            "<th>title": "<th>Title",
            "<table": "<table style='margin-left:auto;margin-right:auto;'",
        }

        for x, y in replacements.items():
            table_html = table_html.replace(x, y)

        # print(table_html)
        return render_template("results.html", results_table=table_html)
    else:
        # return("the books API is probably down")
        return render_template("error.html", code=response.status_code)


@app.route("/search")
def search():
    query = request.args.to_dict()
    if query:  # directly access api
        return process_query(query)
    else:  # show page with form
        return render_template("search.html")


@app.route("/search_results", methods=["POST"])
def search_results():
    params_dict = {
        "id": urllib.parse.quote(request.form.get("id")),
        "title": urllib.parse.quote(request.form.get("title")),
        "author": urllib.parse.quote(request.form.get("author")),
        "publication_year": urllib.parse.quote(
            request.form.get("publication_year")
        ),
        "genre": urllib.parse.quote(request.form.get("genre")),
    }
    # print (params_dict)
    return process_query(params_dict)


if __name__ == "__main__":
    app.run(debug == True)
