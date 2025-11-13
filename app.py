from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)