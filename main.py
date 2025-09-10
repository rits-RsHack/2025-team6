from flask import Flask, render_template, request
from RSA_tool import factordb, low_index, N_prime, yafu_factor, squared_index, Wiener, is_square, Fermat_factor, solve, other_attack
import requests

app = Flask(__name__)

#N = 13373801376856352919495636794117610920860037770702465464324474778341963699665011787021257
#e = 65537
#c = 39119617768257067256541748412833564043113729163757164299687579984124653789492591457335

@app.route("/", methods=["GET", "POST"])

def index():
    result = ""
    if request.method == "POST":
        try:

            N = int(request.form["N"])
            e = int(request.form["e"])
            ct = int(request.form["ct"])

            p,q = factordb(N)
            if not p or not q:
                result = other_attack(N, e, ct)
            else:
                result = solve(p, q, e, ct)

        except Exception as ex:
            result = f"Error: {ex}"

    return render_template("index.html", output=result)

if __name__ == "__main__":
    app.run(debug=True)