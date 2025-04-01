from flask import Blueprint, render_template, request
from .utils.calculator import add, subtract, multiply, divide
from .utils.derivada import calcular_derivada

calculator = Blueprint('calculator', __name__)
derivada = Blueprint('derivada', __name__)

@calculator.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        num1 = request.form.get("num1", type=float)
        num2 = request.form.get("num2", type=float)
        operation = request.form.get("operation")

        operations = {
            "sum": add,
            "subtract": subtract,
            "multiply": multiply,
            "divide": divide
        }

        result = operations.get(operation, lambda a, b: "Operación no válida")(num1, num2)

    return render_template("index.html", result=result)

@derivada.route("/derivatives", methods=["GET", "POST"])
def derivatives_page():
    result = None
    x_val = None  # Añadir esta línea
    if request.method == "POST":
        expr = request.form.get("expression")
        x_val = request.form.get("x_val")  # Coincide con el nombre del formulario

        x_val = float(x_val)
        result = calcular_derivada(expr, x_val)

    # Pasar x_val al template aunque sea None
    return render_template("derivadas.html", result=result, x_val=x_val)