from flask import Flask, render_template, session, request, redirect, url_for, flash
import requests


USDA_SEARCH_API = "https://api.nal.usda.gov/fdc/v1"
API_KEY = "2SOZn8q2Z6rlJ7cfh1UP9zgc4QXUaYmACPKVjl6N"

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


def calcular_macros_por_ingrediente(info, gramos):
    """Calcula kcal y macros en gramos para una cantidad dada.

    info: dict con claves opcionales 'calorias', 'proteina', 'grasa', 'carbohidratos'
        (valores por 100 g).
    gramos: cantidad en gramos (float).
    Retorna un dict con 'calorias', 'proteina_g', 'grasa_g', 'carbohidratos_g'.
    """
    factor = (gramos / 100.0) if gramos else 0.0

    calorias = (info.get('calorias') or 0.0) * factor
    proteina_g = (info.get('proteina') or 0.0) * factor
    grasa_g = (info.get('grasa') or 0.0) * factor
    carbo_g = (info.get('carbohidratos') or 0.0) * factor

    return {
        'calorias': round(calorias, 2),
        'proteina_g': round(proteina_g, 2),
        'grasa_g': round(grasa_g, 2),
        'carbohidratos_g': round(carbo_g, 2)
    }


def calcular_porcentajes_macros(total_calorias, proteina_g, grasa_g, carbo_g):
    """Devuelve el % energético aportado por cada macronutriente respecto a `total_calorias`.

    Retorna dict con claves 'proteina_pct', 'grasa_pct', 'carbohidratos_pct'.
    """
    if not total_calorias or total_calorias <= 0:
        return {'proteina_pct': 0.0, 'grasa_pct': 0.0, 'carbohidratos_pct': 0.0}

    prot_cal = proteina_g * 4
    grasa_cal = grasa_g * 9
    carbo_cal = carbo_g * 4

    return {
        'proteina_pct': round((prot_cal / total_calorias) * 100, 1),
        'grasa_pct': round((grasa_cal / total_calorias) * 100, 1),
        'carbohidratos_pct': round((carbo_cal / total_calorias) * 100, 1)
    }

@app.route('/analizador', methods=['GET', 'POST'])
def analizador():
    resultado = None
    error_parse = None
    error_usda = None
    if request.method == 'POST':
        receta = request.form.get('receta', '')
        lineas = [l.strip() for l in receta.split('\n') if l.strip()]

        ingredientes_proc = []
        total = {'calorias': 0.0, 'proteina': 0.0, 'grasa': 0.0, 'carbohidratos': 0.0}

        for linea in lineas:
            partes = linea.split()
            if len(partes) < 2:
                ingredientes_proc.append({'linea': linea, 'error': 'Formato inválido'})
                error_parse = True
                continue

            
            try:
                cantidad = float(partes[0].replace(',', '.'))
            except Exception:
                ingredientes_proc.append({'linea': linea, 'error': 'Cantidad no numérica'})
                error_parse = True
                continue

            unidad = partes[1].lower()
            nombre = ' '.join(partes[2:]) if len(partes) > 2 else ' '.join(partes[1:])

        
            gramos = None
            if unidad in ('g', 'gr', 'gramo', 'gramos'):
                gramos = cantidad
            elif unidad in ('kg', 'kilogramo', 'kilogramos'):
                gramos = cantidad * 1000
            elif unidad in ('cucharada', 'cucharadas'):
                gramos = cantidad * 15
            elif unidad in ('cucharadita', 'cucharaditas'):
                gramos = cantidad * 5
            elif unidad in ('taza', 'tazas'):
                gramos = cantidad * 240
            elif unidad in ('huevo', 'huevos'):
                gramos = cantidad * 50
            else:
            
                gramos = None

            if gramos is None:
                ingredientes_proc.append({'linea': linea, 'error': 'Unidad no reconocida'})
                error_parse = True
                continue

        
            params = {'api_key': API_KEY, 'query': nombre or partes[-1], 'pageSize': 1}
            try:
                r = requests.get(f"{USDA_SEARCH_API}/foods/search", params=params, timeout=10)
                r.raise_for_status()
                data = r.json()
            except Exception:
                ingredientes_proc.append({'linea': linea, 'error': 'Error consultando USDA'})
                error_usda = True
                continue

            foods = data.get('foods') or []
            if not foods:
                ingredientes_proc.append({'linea': linea, 'error': 'No encontrado en la base USDA'})
                error_usda = True
                continue

            food = foods[0]
            fdcId = food.get('fdcId')

        
            nutri_data = food
            if fdcId:
                try:
                    r2 = requests.get(f"{USDA_SEARCH_API}/food/{fdcId}", params={'api_key': API_KEY}, timeout=10)
                    r2.raise_for_status()
                    nutri_data = r2.json()
                except Exception:
                    nutri_data = food

            
            info = {'calorias': 0.0, 'proteina': 0.0, 'grasa': 0.0, 'carbohidratos': 0.0}
            label = nutri_data.get('labelNutrients') or {}
            if label:
            
                def _get_label(k):
                    v = label.get(k)
                    if isinstance(v, dict):
                        return v.get('value')
                    return v

                info['calorias'] = _get_label('calories') or info['calorias']
                info['proteina'] = _get_label('protein') or info['proteina']
                info['grasa'] = _get_label('fat') or info['grasa']
                info['carbohidratos'] = _get_label('carbohydrates') or info['carbohidratos']
            else:
                for n in nutri_data.get('foodNutrients', []):
                    nutrient = n.get('nutrient') or {}
                    name = nutrient.get('name', '').lower() if nutrient else n.get('nutrientName', '').lower()
                    amount = n.get('amount') or n.get('value') or 0
                    if 'energy' in name or 'calor' in name:
                        info['calorias'] = info['calorias'] or amount
                    elif 'protein' in name or 'proteina' in name:
                        info['proteina'] = info['proteina'] or amount
                    elif 'lipid' in name or 'fat' in name or 'grasa' in name:
                        info['grasa'] = info['grasa'] or amount
                    elif 'carbohydrate' in name or 'carbohidr' in name:
                        info['carbohidratos'] = info['carbohidratos'] or amount

            macros = calcular_macros_por_ingrediente(info, gramos)

            ingredientes_proc.append({'linea': linea, 'nombre': nombre, 'gramos': gramos, 'macros': macros})

            total['calorias'] += macros['calorias']
            total['proteina'] += macros['proteina_g']
            total['grasa'] += macros['grasa_g']
            total['carbohidratos'] += macros['carbohidratos_g']

        total_porcentajes = calcular_porcentajes_macros(total['calorias'], total['proteina'], total['grasa'], total['carbohidratos'])
        resultado = {'ingredientes': ingredientes_proc, 'total': total, 'total_porcentajes': total_porcentajes}

    return render_template('analizador.html', resultado=resultado, error_parse=error_parse, error_usda=error_usda, receta_texto=(request.form.get('receta') if request.method == 'POST' else ''))

@app.route('/banco')
def banco():
    return render_template('banco.html')

if __name__ == '__main__':
    app.run(debug=True)