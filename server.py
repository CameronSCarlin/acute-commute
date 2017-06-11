from flask import Flask, request, send_file
from Commute import Commute
app = Flask(__name__)


@app.route('/trip', methods=['POST'])
def trip():
    form = request.form
    start = form['start']
    end = form['end']

    modes = [mode for mode in Commute.available_modes if mode in form]
    comm = Commute(start=start,
                    end=end,
                    acceptable_modes=modes)
    return comm.get_directions_json()


@app.route("/")
def main():
    return send_file('./static/index.html')


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True, port=80)
    app.run(host='localhost', port=5000)
