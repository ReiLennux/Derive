from sympy import symbols, sympify, diff, latex, lambdify
import re
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def diferencias_finitas(expr_str, x0, h):
    try:
        # Reemplaza el operador de potencia '^' por '**' para que Sympy lo reconozca
        expr_str = expr_str.replace('^', '**')
        
        # Inserta el operador de multiplicación implícita en casos como "2x" o "3(x+1)"
        expr_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr_str)
        
        x = symbols('x')
        expr = sympify(expr_str)
        
        # Métodos de diferencias finitas
        derivada_adelante = (expr.subs(x, x0 + h) - expr.subs(x, x0)) / h
        derivada_atras = (expr.subs(x, x0) - expr.subs(x, x0 - h)) / h
        derivada_centrada = (expr.subs(x, x0 + h) - expr.subs(x, x0 - h)) / (2 * h)
        
        # Derivada exacta
        derivada_exacta = diff(expr, x).subs(x, x0)
        
        # Calcular los errores relativos
        error_adelante = abs((derivada_adelante.evalf() - derivada_exacta.evalf()) / derivada_exacta.evalf())
        error_atras = abs((derivada_atras.evalf() - derivada_exacta.evalf()) / derivada_exacta.evalf())
        error_centrada = abs((derivada_centrada.evalf() - derivada_exacta.evalf()) / derivada_exacta.evalf())
        
        # Determinar el método con menor error
        min_error_method = min(
            ("Adelante", error_adelante),
            ("Atras", error_atras),
            ("Centrada", error_centrada),
            key=lambda x: x[1]
        )[0]
        
        # Generar la gráfica
        x_vals = np.linspace(x0 - 2, x0 + 2, 100)  # Rango alrededor de x0
        f_lambdified = lambdify(x, expr, "numpy")  # Convertir la función a una forma evaluable
        f_vals = f_lambdified(x_vals)  # Evaluar la función original
        
        deriv_exacta = diff(expr, x)  # Derivada exacta como expresión
        deriv_lambdified = lambdify(x, deriv_exacta, "numpy")  # Convertir la derivada a una forma evaluable
        deriv_vals = deriv_lambdified(x_vals)  # Evaluar la derivada
        
        # Crear la figura
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, f_vals, label=f"f(x) = {expr_str}", color="blue")
        plt.plot(x_vals, deriv_vals, label=f"f'(x) = {latex(deriv_exacta)}", color="red", linestyle="--")
        plt.axvline(x=x0, color="green", linestyle=":", label=f"x = {x0}")
        plt.legend()
        plt.grid(True)
        plt.title(f"Función y su derivada en x = {x0}")
        plt.xlabel("x")
        plt.ylabel("y")
        
        # Guardar la gráfica en un buffer y codificarla en base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        graph_data = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close()  # Cerrar la figura para liberar memoria
        
        # Retornar los resultados con la gráfica
        return {
            "expresion_original": latex(expr),
            "derivada_exacta": latex(diff(expr, x)),
            "valor_derivada_exacta": derivada_exacta.evalf(),
            "derivada_adelante": derivada_adelante.evalf(),
            "derivada_atras": derivada_atras.evalf(),
            "derivada_centrada": derivada_centrada.evalf(),
            "error_adelante": error_adelante,
            "error_atras": error_atras,
            "error_centrada": error_centrada,
            "metodo_menor_error": min_error_method,
            "x_val": x0,
            "graph_html": f'<img src="data:image/png;base64,{graph_data}" alt="Gráfica de la función y su derivada"/>'
        }
    except Exception as e:
        return {"error": f"Lo sentimos, ocurrió un error: {str(e)}. Por favor, verifica la expresión ingresada e intenta de nuevo."}