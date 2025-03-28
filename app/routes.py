from flask import Blueprint, render_template, request
from .utils.calculator import add, subtract, multiply, divide

calculator = Blueprint('calculator', __name__)

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
