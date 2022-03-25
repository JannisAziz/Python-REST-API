from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("movies.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/")
def home():
    return "Hello World from Flask App!"


@app.route("/movies", methods=['GET', 'POST'])
def movies():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM movie")
        movies = [
            dict(id=row[0], title=row[1])
            for row in cursor.fetchall()
        ]
        if movies is not None:
            return jsonify(movies)

    if request.method == 'POST':
        new_title = request.form['title']
        sql = """INSERT INTO movie (title) VALUES (?)"""
        cursor = cursor.execute(sql, [new_title])
        conn.commit()
        return f"Movie with the id: {cursor.lastrowid} created successfully", 201


if __name__ == '__main__':
    app.run()
