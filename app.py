from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    result = None
    if request.method == "POST":
        try:
            km = float(request.form['km'])
            huella = km * 0.192
            result = f"Tu huella semanal estimada es de {huella:.2f} kg de Co2"
        except ValueError:
            result = "Por favor, ingresa un número válido."

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run()