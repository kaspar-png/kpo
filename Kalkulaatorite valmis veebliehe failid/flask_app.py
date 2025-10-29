from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

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

            if algkapital < 0 or igakuine < 0 or tootlus < 0 or periood <= 0:
                error = "Kõik väärtused peavad olema positiivsed."
            else:
                n = periood
                r = tootlus / 100
                k = 12

                if r == 0:
                    tulemus_valem = algkapital + igakuine * k * n
                else:
                    tulemus_valem = (
                        algkapital * (1 + r / k) ** (k * n)
                        + igakuine * ((math.pow(1 + r / k, k * n) - 1) / (r / k))
                    )

                if tulemus_valem < 0:
                    tulemus_valem = 0

                tulemus = f"{tulemus_valem:.2f} €"

        except ValueError:
            error = "Palun sisesta kehtivad numbrid."

    return render_template('liitintress.html', tulemus=tulemus, error=error)

@app.route('/laen', methods=['GET', 'POST'])
def laen():
    tulemus = None
    kogusumma = None
    error = None

    if request.method == 'POST':
        try:
            laenusumma = float(request.form["laenusumma"].replace(',', '.'))
            sissemakse = float(request.form["sissemakse"].replace(',', '.'))
            intress = float(request.form["intress"].replace(',', '.'))
            periood = int(request.form["periood"])
            yksus = request.form["yksus"]

            if laenusumma <= 0 or sissemakse < 0 or intress < 0 or periood <= 0:
                error = "Kõik väärtused peavad olema positiivsed."
            elif sissemakse > laenusumma:
                error = "Sissemakse ei saa olla suurem kui laenusumma."
            else:
                laenusumma -= sissemakse

                periood_kuudes = periood * 12 if yksus == "aastates" else periood

                kuine_intress = intress / 100 / 12

                if kuine_intress == 0:
                    kuine_makse = laenusumma / periood_kuudes
                else:
                    arvutus = (1 + kuine_intress) ** periood_kuudes
                    kuine_makse = laenusumma * kuine_intress * arvutus / (arvutus - 1)

                tulemus = f"{kuine_makse:.2f} €"

                kogusumma_valem = kuine_makse * periood_kuudes
                kogusumma = f"{kogusumma_valem:.2f} €"

        except ValueError:
            error = "Palun sisesta kehtivad numbrid."

    return render_template('laen.html', tulemus=tulemus, kogusumma=kogusumma, error=error)

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

            if km <= 0 or liitrid < 0 or hind < 0:
                viga = "Kõik väärtused peavad olema positiivsed."
            else:
                kulu_100km_valem = (liitrid / km) * 100
                kulu_maksumus_valem = liitrid * hind

                if kulu_100km_valem < 0:
                    kulu_100km_valem = 0
                if kulu_maksumus_valem < 0:
                    kulu_maksumus_valem = 0

                kulu_100km = f"{kulu_100km_valem:.2f}"
                kulu_maksumus = f"{kulu_maksumus_valem:.2f}"

        except ValueError:
            viga = "Palun sisesta kehtivad numbrid."

    return render_template('kutus.html', kulu_100km=kulu_100km, kulu_maksumus=kulu_maksumus, viga=viga)


if __name__ == "__main__":
    app.run(debug=True)
