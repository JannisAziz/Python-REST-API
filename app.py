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


@app.route("/movie/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def single_movie(id):
    if request.method == 'GET':
        for movie in movies_list:
            if movie['id'] == id:
                return jsonify(movie)
    if request.method == 'PUT':
        for movie in movies_list:
            if movie['id'] == id:
                movie['title'] = request.form['title']
                updated_movie = {
                    'id': id,
                    'title': movie['title']
                }
                return jsonify(updated_movie)
    if request.method == 'DELETE':
        for index, movie in enumerate(movies_list):
            if movie['id'] == id:
                movies_list.pop(index)
                return jsonify(movies_list)


if __name__ == '__main__':
    app.run()
