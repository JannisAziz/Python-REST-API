from flask import Flask, request, jsonify
app = Flask(__name__)


movies_list = [
    {"id": 0,
     "title": "Spiderman"},
    {"id": 1,
     "title": "Batman"},
    {"id": 2,
     "title": "Superman"},
    {"id": 3,
     "title": "Aquaman"}
]


@app.route("/")
def home():
    return "Hello World from Flask App!"


@app.route("/movies", methods=['GET', 'POST'])
def movies():
    if request.method == 'GET':
        if len(movies_list) > 0:
            return jsonify(movies_list)
        else:
            "Nothing found", 404

    if request.method == 'POST':
        new_title = request.form['title']
        iD = movies_list[-1]['id'] + 1

        new_movie = {
            'id': iD,
            'title': new_title
        }

        movies_list.append(new_movie)
        return jsonify(movies_list), 201


if __name__ == '__main__':
    app.run()
