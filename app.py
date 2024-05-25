from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['POST'])
def process_data():
    data = request.get_json()
    response_data = {
        "message": "Data received successfully",
        "received_data": data
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
