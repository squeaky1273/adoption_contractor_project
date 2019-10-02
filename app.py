from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('index.html', adoptions=adoptions.find())

if __name__ == '__main__':
    app.run(debug=True)