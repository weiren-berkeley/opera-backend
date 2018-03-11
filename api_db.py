from flask import Flask, request, redirect
import json
import sqlite3
from flask_cors import CORS

def get_connection():
    return sqlite3.connect('links.db')


def create_links_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS links (long_url text, short_url text)")
    conn.commit()
    conn.close()


app = Flask(__name__)
CORS(app)

@app.route("/password", methods=["GET"])
def test_password():

    request_data = request.args
    password = request_data['password']
    response_text = dict()
    if (password == 'oparp'):
        response_text['message'] = "Right"
    else:
        response_text['message'] = "Wrong"
    return json.dumps(response_text)



@app.route("/links", methods=["POST"])
def create_link():
    """
    To test: curl -H "Content-Type: application/json" -X POST -d '{ "long_url" : "http://google.com", "short_url": "asefw" }' http://localhost:5000/links
    To test: curl -H "Content-Type: application/json" -X POST -d '{ "long_url" : "http://facebook.com", "short_url": "fb" }' http://localhost:5000/links

    """
    request_data = request.get_json()
    long_url = request_data["long_url"]
    short_url = request_data["short_url"]
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO links (long_url, short_url) VALUES (?, ?)", [long_url, short_url])
    conn.commit()
    conn.close()
    response_text = dict()
    response_text['message'] = "Success"
    return json.dumps(response_text)

@app.route("/links", methods=["GET"])
def get_all_links():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT long_url, short_url FROM links")
    links = c.fetchall()
    return_data = list()
    for link in links:
        link_dict = dict()
        link_dict["long_url"] = link[0]
        link_dict["short_url"] = link[1]
        return_data.append(link_dict)
    return json.dumps(return_data)

@app.route("/link", methods=["GET"])
def get_a_long_url():
    """
    To test: Input URL in browser "http://localhost:5000/link?short_url=asefw"
    Or test: curl http://localhost:5000/link?short_url=asefw
    Result: redirect to "http://google.com"

    To test: Input URL in browser "http://localhost:5000/link?short_url=fw"
    Or test: curl http://localhost:5000/link?short_url=fb
    Result: redirect to "http://facebook.com"

    """
    request_data = request.args
    short_url = request_data['short_url']
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT long_url, short_url FROM links WHERE short_url = '%s'" % short_url)
    link = c.fetchall()
    if (link != []):
        long_url = link[0][0]
        return redirect(long_url)
    else:
        return "No such record."


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)
create_links_table()
