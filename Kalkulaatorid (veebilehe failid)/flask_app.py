from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

# Liitintressi kalkulaator
@app.route('/liitintress', methods=['GET', 'POST'])
def liitintress():
    tulemus = None
    error = None
    if request.method == 'POST':
        try:
            algkapital = float(request.form['algkapital'])
            igakuine = float(request.form['igakuine'])
            tootlus = float(request.form['tootlus'])
            periood = int(request.form['periood'])

            n = periood
            r = tootlus / 100
            k = 12

            tulemus_valem = algkapital * (1 + r / k) ** (k * n) + igakuine * ((math.pow(1 + r / k, k * n) - 1) / (r / k))
            tulemus = f"{tulemus_valem:.2f} €"

        except ValueError:
            error = "Palun sisesta kehtivad numbrid."

    return render_template('liitintress.html', tulemus=tulemus, error=error)

# Laenukalkulaator
@app.route('/laen', methods=['GET', 'POST'])
def laen():
    tulemus = None
    error = None
    if request.method == 'POST':
        try:
            laenusumma = float(request.form["laenusumma"])
            sissemakse = float(request.form["sissemakse"])
            intress = float(request.form["intress"])
            periood = int(request.form["periood"])
            yksus = request.form["yksus"]

            laenusumma -= sissemakse
            periood_kuudes = periood * 12 if yksus == "aastates" else periood
            kuine_intress = intress / 100 / 12

            kuine_makse = (
                laenusumma
                * kuine_intress
                * math.pow(1 + kuine_intress, periood_kuudes)
                / (math.pow(1 + kuine_intress, periood_kuudes) - 1)
            )

            tulemus = f"{kuine_makse:.2f} €"

        except ValueError:
            error = "Palun sisesta kehtivad numbrid."

    return render_template('laen.html', tulemus=tulemus, error=error)

# Kütusekulu kalkulaator
@app.route('/kutus', methods=['GET', 'POST'])
def kutus():
    kulu_100km = ''
    kulu_maksumus = ''
    viga = None

    if request.method == 'POST':
        try:
            km = float(request.form['km'])
            liitrid = float(request.form['liitrid'])
            hind = float(request.form['hind'])

            kulu_100km = (liitrid / km) * 100
            kulu_maksumus = liitrid * hind

            kulu_100km = f"{kulu_100km:.2f}"
            kulu_maksumus = f"{kulu_maksumus:.2f}"
        except:
            viga = "Viga sisendis!"

    return render_template('kutus.html', kulu_100km=kulu_100km, kulu_maksumus=kulu_maksumus, viga=viga)

if __name__ == "__main__":
    app.run(debug=True)
