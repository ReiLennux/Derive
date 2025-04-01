from flask import Blueprint, render_template, request
from .utils.derivada import diferencias_finitas

derivada = Blueprint('derivada', __name__)

@derivada.route("/", methods=["GET", "POST"])
def derivatives_page():
    result = None
    x_val = None  
    h_val = None  # Nueva variable para recibir el valor de h

    if request.method == "POST":
        expr = request.form.get("expression")
        x_val = request.form.get("x_val")  
        h_val = request.form.get("h_val")  # Obtener el valor de h desde el formulario

        try:
            x_val = float(x_val)
            h_val = float(h_val)  # Convertir h a número decimal
            result = diferencias_finitas(expr, x_val, h_val)  # Pasar h a la función
        except ValueError:
            result = {"error": "Por favor, introduce valores numéricos válidos para x y h."}

    return render_template("derivadas.html", result=result, x_val=x_val)
