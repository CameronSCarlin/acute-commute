from flask import Flask, request, send_file
app = Flask(__name__)


@app.route('/trip', methods=['POST'])
def trip():
    form = request.form
    start = form['start']
    end = form['end']
    walking = 'walking' in form
    bicycling = 'bicycling' in form
    driving = 'driving' in form
    transit = 'transit' in form


@app.route("/")
def main():
    return send_file('./static/index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
