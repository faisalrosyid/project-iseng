from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    nama = request.form["nama"]
    return f"Halo {nama}, data kamu sudah diterima!"

if __name__ == "__main__":
    app.run(debug=True)