from flask import Flask, render_template
import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/prod')
def product():
    try:
        image = main.product()
        print(image)
    except Exception as e:
        return 'error: ' + str(e)
    return 'ok'

if __name__ == '__main__':
    app.run()
