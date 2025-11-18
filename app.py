from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'random_value'

@app.route('/')
def index():
    return render_template('Base.html')

@app.route('/calculadora')
def calculadora():
    return render_template('calculadoraTMB.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/sesion')
def sesion():
    return render_template('sesion.html')

@app.route('/politicas')
def politicas():
    return render_template('politicas de seguridad.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/imc', methods=['GET', 'POST'])
def imc():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form.get('peso', 0))
            altura = float(request.form.get('altura', 0)) / 100
            if peso <= 0 or altura <= 0:
                raise ValueError("Valores inválidos.")

            imc_valor = peso / (altura ** 2)
            if imc_valor < 18.5:
                estado = "Bajo peso"
            elif imc_valor < 25:
                estado = "Normal"
            elif imc_valor < 30:
                estado = "Sobrepeso"
            else:
                estado = "Obesidad"

            resultado = f"Tu IMC es {imc_valor:.2f} ({estado})"
        except Exception:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('calculadoraIMC.html', resultado=resultado)

@app.route('/tmb', methods=['GET', 'POST'])
def tmb():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form.get('peso', 0))
            altura = float(request.form.get('altura', 0))
            edad = int(request.form.get('edad', 0))
            sexo = request.form.get('sexo')

            if sexo not in ["Masculino", "Femenino"] or peso <= 0 or altura <= 0 or edad <= 0:
                raise ValueError("Datos inválidos.")

            if sexo == "Masculino":
                tmb_valor = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
            else:
                tmb_valor = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)

            resultado = f"Tu TMB es {tmb_valor:.2f} kcal/día"
        except Exception:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('calculadoraTMB.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)