from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('index.html')  # Same page for simplicity

@app.route('/contact')
def contact():
    return render_template('index.html')  # Same page for simplicity

@app.route('/docs')
def docs():
    return render_template('docs.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
