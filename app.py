from flask import Flask, render_template, session, request, redirect, url_for, flash
import requests

USDA_SEARCH_API = "https://api.nal.usda.gov/fdc/v1/foods/search"
API_KEY = "O9NiAqcunULNoE5rLUG09X6xtMDAymcUQozGCJLS"

app = Flask(__name__)
app.secret_key = 'random_value'

@app.route('/')
def index():
    return render_template('Base.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        user = {
            'nombre': request.form.get('nombre'),
            'email': request.form.get('email'),
            'edad': request.form.get('edad'),
            'sexo': request.form.get('sexo'),
            'peso': request.form.get('peso'),
            'altura': request.form.get('altura')
        }
        session['user'] = user
        flash('Registro guardado correctamente.', 'success')
        return redirect(url_for('perfil'))
    return render_template('registro.html')

@app.route('/sesion')
def sesion():
    return render_template('sesion.html')

@app.route('/politicas')
def politicas():
    return render_template('politicas de seguridad.html')

@app.route('/perfil')
def perfil():
    user = session.get('user')
    return render_template('perfil.html', user=user)

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
        except:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('calculadoraTMB.html', resultado=resultado)

@app.route('/gct', methods=['GET', 'POST'])
def gct():
    resultado = None
    if request.method == 'POST':
        try:
            tmb = float(request.form.get('tmb', 0))
            actividad = request.form.get('actividad')

            factores_actividad = {
                "Sedentario": 1.2,
                "Ligera": 1.375,
                "Moderada": 1.55,
                "Intensa": 1.725,
                "Muy Intensa": 1.9
            }

            if actividad not in factores_actividad or tmb <= 0:
                raise ValueError("Datos inválidos.")

            gct_valor = tmb * factores_actividad[actividad]
            resultado = f"Tu GCT es {gct_valor:.2f} kcal/día"
        except:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('calculadoraGCT.html', resultado=resultado)

@app.route('/pci', methods=['GET', 'POST'])
def peso_ideal():
    resultado = None
    if request.method == 'POST':
        try:
            altura = float(request.form.get('altura', 0))
            sexo = request.form.get('sexo')

            if sexo not in ["Masculino", "Femenino"] or altura <= 0:
                raise ValueError("Datos inválidos.")

            if sexo == 'Masculino':
                peso_ideal_valor = 50 + 2.3 * ((altura / 2.54) - 60)
            else:
                peso_ideal_valor = 45.5 + 2.3 * ((altura / 2.54) - 60)

            resultado = f"Tu peso ideal es {peso_ideal_valor:.2f} kg"
        except:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('CalculadoraPCI.html', resultado=resultado)

@app.route('/m', methods=['GET', 'POST'])
def macronutrientes():
    resultado = None
    if request.method == 'POST':
        try:
            calorias = float(request.form.get('calorias', 0))
            if calorias <= 0:
                raise ValueError("Valor inválido.")
            proteinas = calorias * 0.3 / 4
            grasas = calorias * 0.25 / 9
            carbohidratos = calorias * 0.45 / 4
            resultado = {
                "proteinas": round(proteinas, 1),
                "grasas": round(grasas, 1),
                "carbohidratos": round(carbohidratos, 1)
            }
        except:
            flash("Error: revisa los datos ingresados.", "danger")
    return render_template('calculadoraM.html', resultado=resultado)

@app.route('/articulos')
def articulos():
    return render_template('articulos.html')

@app.route('/ejercicios')
def ejercicios():
    return render_template('ejercicios.html')

def parse_food(item):
    nombre = item.get("description", "Sin nombre")

    categoria = (
        item.get("brandedFoodCategory")
        or item.get("foodCategory", {}).get("description")
    )

    label = item.get("labelNutrients", {})

    calorias = label.get("calories", {}).get("value")
    proteina = label.get("protein", {}).get("value")
    grasa = label.get("fat", {}).get("value")
    carbohidratos = label.get("carbohydrates", {}).get("value")

    if calorias is None:
        for n in item.get("foodNutrients", []):
            nutrient = n.get("nutrient", {})
            nombre_nutriente = nutrient.get("name")

            if nombre_nutriente == "Energy":
                calorias = n.get("amount")
            elif nombre_nutriente == "Protein":
                proteina = n.get("amount")
            elif nombre_nutriente == "Total lipid (fat)":
                grasa = n.get("amount")
            elif nombre_nutriente == "Carbohydrate, by difference":
                carbohidratos = n.get("amount")

    return {
        "nombre": nombre,
        "categoria": categoria,
        "calorias": calorias,
        "proteina": proteina,
        "grasa": grasa,
        "carbohidratos": carbohidratos
    }

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    resultados = None

    if request.method == 'POST':
        query = request.form.get("query", "").strip()

        if query:
            url = f"{USDA_SEARCH_API}/v1/foods/search"
            params = {
                "api_key": API_KEY,
                "query": query,
                "pageSize": 10
            }
            r = requests.get(url, params=params)
            data = r.json()

            foods = data.get("foods", [])
            resultados = [parse_food(f) for f in foods]

    return render_template("buscar.html", resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)