from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Flask!"

@app.route("/username/<name>")
def learn(name):
    return f"{name} is learning Flask!"

if __name__ == "__main__":
    app.run(debug=True, port=5002)  