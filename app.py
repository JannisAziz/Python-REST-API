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


@app.route("/movie/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def single_movie(id):
    conn = db_connection()
    cursor = conn.cursor()
    movie = None

    if request.method == 'GET':
        cursor.execute("SELECT * FROM movie WHERE id=?", [id])
        rows = cursor.fetchall()
        for r in rows:
            movie = r
        if movie is not None:
            return jsonify(movie), 200
        else:
            return "Something wrong", 404

    if request.method == 'PUT':
        sql = """UPDATE movie 
        		SET title=? 
          		WHERE id=? """

        title = request.form["title"]

        updated_movie = {
            'id': id,
            'title': title
        }

        conn.execute(sql, [title, id])
        conn.commit()
        return jsonify(updated_movie)

    if request.method == 'DELETE':
        sql = """ DELETE FROM movie WHERE id=? """
        conn.execute(sql, [id])
        conn.commit()
        return "The book with id: {} has been deleted.".format(id), 200


if __name__ == '__main__':
    app.run()
