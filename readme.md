### Fecha: 
Martes 4 de Noviembre del 2025

### Integrantes: 
Diaz Martinez Angel Joel, De Luna Castruita Santiago 

### Escuela: 
CETis #61

### Especialidad:
Programacion

### Grupo: 
3 - D

### Nuestras fotos:
![Mi foto](f1.jpg)


pip install -r
requirements.txt

pip freeze >
requirements.txt

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
    return render_template('imc.html', resultado=resultado)



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
    return render_template('tmb.html', resultado=resultado)