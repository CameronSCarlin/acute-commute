from flask import Flask, request, render_template
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


@app.route("/v1")
def v1():
    return render_template('index.html', bg_color='red')

@app.route("/v2")
def v2():
    return render_template('index.html', bg_color='blue')

@app.route("/v3")
def v3():
    return render_template('index.html', bg_color='green')


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True, port=80)
    app.run(host='localhost', port=5000)
