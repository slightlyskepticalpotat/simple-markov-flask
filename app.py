import os
import secrets
from flask import Flask, flash, render_template, request

app = Flask(__name__)

secret = secrets.token_hex(32)
with open("/home/chenanthony365/chenanthony-markov/secret_key.txt", "w+") as file:
    file.write(secret)
app.config["SECRET_KEY"] = secret

@app.route("/", methods = ["GET", "POST"])
def markov():
    if request.method == "GET":
        return render_template("index.html")

    if not request.form.get("word-count") or not request.form.get("states-used") or not request.form.get("temperature") or not request.files.get("training-data"):
        flash("All fields must be filled in.", "danger")
        return render_template("index.html")

    try:
        word_count = int(request.form.get("word-count"))
        states_used = int(request.form.get("states-used"))
        temperature = int(request.form.get("temperature"))
    except:
        flash("Non-file fields must be numerical.", "danger")
        return render_template("index.html")

    if not 1 <= word_count <= 65536 or not 1 <= states_used <= 16 or not 0 <= temperature <= 100:
        flash("Non-file fields must stay within range.", "danger")
        return render_template("index.html")

    filename = str(secrets.token_hex(8))
    try:
        request.files.get("training-data").save(filename + ".in")
        training_data = open(filename + ".in", "r").read()
        os.remove(filename + ".in")
    except:  # top-quality error handling
        pass

    generated_text = open(filename + ".out", "r").read()
    os.remove(filename + ".out")
    return generated_text

if __name__ == "__main__":
    app.run()
