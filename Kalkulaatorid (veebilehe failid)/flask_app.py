from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    kulu_100km = ''
    kulu_maksumus = ''
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
            kulu_100km = "Viga sisendis!"
            kulu_maksumus = "Viga sisendis!"
        
    return render_template('index.html', kulu_100km=kulu_100km, kulu_maksumus=kulu_maksumus)

if __name__ == '__main__':
    app.run(debug=True)
