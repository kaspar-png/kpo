from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    tulemus = None
    error = None

    if request.method == "POST":
        try:
            laenusumma = float(request.form["laenusumma"])
            sissemakse = float(request.form["sissemakse"])
            intress = float(request.form["intress"])
            periood = int(request.form["periood"])
            yksus = request.form["yksus"]

            laenusumma -= sissemakse

            if yksus == "aastates":
                periood_kuudes = periood * 12
            else:
                periood_kuudes = periood

            kuine_intress = intress / 100 / 12

            kuine_makse = (
                laenusumma
                * kuine_intress
                * math.pow(1 + kuine_intress, periood_kuudes)
                / (math.pow(1 + kuine_intress, periood_kuudes) - 1)
            )

            tulemus = f"Igakuine makse: {kuine_makse:.2f} €"

        except ValueError:
            error = "Palun sisesta kehtivad numbrid."

    return render_template("index.html", tulemus=tulemus, error=error)

if __name__ == "__main__":
    app.run(debug=True)
