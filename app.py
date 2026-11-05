from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "lab.db"


def search_users(username):
    """INTENTIONALLY VULNERABLE: untrusted input is concatenated into SQL."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Vulnerability: SQL injection through string concatenation.
    query = "SELECT id, username, email FROM users WHERE username LIKE '%" + username + "%'"
    cursor.execute(query)

    results = cursor.fetchall()
    connection.close()
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    searched = False
    error = None

    if request.method == "POST":
        searched = True
        username = request.form.get("username", "")
        try:
            results = search_users(username)
        except sqlite3.Error as exc:
            # Lab-only: display database errors to make the behaviour observable.
            error = str(exc)

    return render_template("index.html", results=results, searched=searched, error=error)


if __name__ == "__main__":
    # Local-only binding. Do not change to 0.0.0.0 for this exercise.
    app.run(host="127.0.0.1", port=5000, debug=True)
