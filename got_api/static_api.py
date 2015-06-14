from flask import Flask, jsonify
app = Flask(__name__)

SIMPLE_DICTIONARY = {
    "Lannisters": ["Cersei", "Jaime", "Tyrion"],
    "Baratheons": ["Robert", "Renly", "Stannis"]
}


@app.route('/')
def index():
    return jsonify(SIMPLE_DICTIONARY)

if __name__ == '__main__':
    app.run(debug=True)
