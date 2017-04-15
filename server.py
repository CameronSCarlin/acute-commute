from flask import Flask, request
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
