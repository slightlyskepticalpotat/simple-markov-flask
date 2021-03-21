import os
import secrets
from flask import Flask, flash, render_template, request

app = Flask(__name__)

secret = secrets.token_hex(32)
with open("/home/chenanthony365/chenanthony-markov/" + "secret_key.txt", "w+") as file:
    file.write(secret + "\n")
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

    if not 1 <= word_count <= 262144 or not 1 <= states_used <= 16 or not 0 <= temperature <= 100:
        flash("Non-file fields must stay within range.", "danger")
        return render_template("index.html")

    generated_text = "Sorry, something went wrong. Please try again."
    filename = str(secrets.token_hex(8))
    try:
        request.files.get("training-data").save("/home/chenanthony365/chenanthony-markov/" + filename + ".in")
        os.system(f"./markov_mod {word_count} {states_used} {temperature} {'/home/chenanthony365/chenanthony-markov/' + filename + '.in'} {'/home/chenanthony365/chenanthony-markov/' + filename + '.out'}")  # actually generate the text
        generated_text = open("/home/chenanthony365/chenanthony-markov/" + filename + ".out", "r").read()
        os.remove("/home/chenanthony365/chenanthony-markov/" + filename + ".in")
        os.remove("/home/chenanthony365/chenanthony-markov/" + filename + ".out")
    except:  # top-quality error handling
        try:
            os.remove("/home/chenanthony365/chenanthony-markov/" + filename + ".in")
        except:
            pass
        try:
            os.remove("/home/chenanthony365/chenanthony-markov/" + filename + ".out")
        except:
            pass

    return render_template("generated.html", data = generated_text)

if __name__ == "__main__":
    app.run()
