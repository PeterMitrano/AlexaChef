from flask import Flask, render_template, request
import schema

app = Flask(__name__)

@app.route('/')
def get_root():
    return render_template('index.html', intents=schema.intents());

# run the app.
if __name__ == '__main__':
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.run(debug = True)

