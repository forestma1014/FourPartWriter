from flask import Flask, render_template, request, url_for
from main import *

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        key = request.form['key'].split(' ')
        melody = request.form['melody'].split(' ')
        
        print('KEY:',key)
        if key[0].upper() not in ['A','B','C','D','E','F','G']:
            return render_template('invalid.html')
        
        if key[-1].lower() not in ['major','minor']:
            return render_template('invalid.html')
            
        if len(key) == 3 and key[1].lower() not in ['sharp','flat','natural']:
            return render_template('invalid.html')
        
        if len(key) == 2 or key[1].lower() == 'natural':
            accidental = 0
        elif key[1].lower() == 'sharp':
            accidental = 1
        else:
            accidental = -1
        
        tonic = [key[0].upper(), accidental]
        mode = key[-1]
        print(tonic, mode, melody,'asdf')
        parts = run(tonic, mode, melody)

        return render_template('result.html',parts)
    else:
        return render_template('index.html')

#results page after successful input
@app.route('/result')
def result():
    return render_template('result.html')

#invalid input
@app.route('/invalid', methods=['POST','GET'])
def invalid():

    return render_template('invalid.html')


if __name__ == "__main__":
    app.run(debug=True)