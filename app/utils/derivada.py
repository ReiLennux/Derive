import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from sympy import symbols, sympify, diff, latex, lambdify, E, log
import re

def diferencias_finitas(expr_str, x0, h, decimales=None):  # Añadido parámetro decimales
    try:
        # Reemplaza el operador de potencia '^' por '**'
        expr_str = expr_str.replace('^', '**')
        
        # Inserta el operador de multiplicación implícita (ej: 2x -> 2*x)
        expr_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr_str)
        
        # Reemplaza la "e" aislada por "E" (constante de Euler)
        expr_str = re.sub(r'\be\b', 'E', expr_str)
        
        # Reemplaza "ln" por "log" para el logaritmo natural
        expr_str = re.sub(r'\bln\b', 'log', expr_str)
        
        # Definir la variable simbólica y convertir la cadena a expresión
        x = symbols('x')
        expr = sympify(expr_str)
        
        # Verificar que la expresión solo contiene la variable 'x'
        if len(expr.free_symbols) > 1:
            return {"error": "Por favor, ingrese una expresión que dependa solo de 'x'."}
        
        # Métodos de diferencias finitas
        derivada_adelante = (expr.subs(x, x0 + h) - expr.subs(x, x0)) / h
        derivada_atras = (expr.subs(x, x0) - expr.subs(x, x0 - h)) / h
        derivada_centrada = (expr.subs(x, x0 + h) - expr.subs(x, x0 - h)) / (2 * h)
        
        # Derivada exacta evaluada en x0
        derivada_exacta = diff(expr, x).subs(x, x0)
        exact_val = derivada_exacta.evalf()
        
        # Se define una tolerancia para decidir si el valor exacto es prácticamente cero
        tol = 1e-12
        
        # Calcular errores: si exact_val es muy pequeño, usamos error absoluto
        if abs(exact_val) < tol:
            error_adelante = abs(derivada_adelante.evalf() - exact_val)
            error_atras = abs(derivada_atras.evalf() - exact_val)
            error_centrada = abs(derivada_centrada.evalf() - exact_val)
        else:
            error_adelante = abs((derivada_adelante.evalf() - exact_val) / exact_val)
            error_atras = abs((derivada_atras.evalf() - exact_val) / exact_val)
            error_centrada = abs((derivada_centrada.evalf() - exact_val) / exact_val)
        
        # Función para aplicar redondeo si decimales tiene valor
        def redondear(valor):
            if decimales is not None:
                return round(float(valor), decimales)
            return valor
        
        # Determinar el método con menor error
        errors = {"Progresiva": error_adelante, "Regresiva": error_atras, "Central": error_centrada}
        min_error_method = min(errors, key=errors.get)
        
        # Generar la gráfica
        x_vals = np.linspace(x0 - 2, x0 + 2, 100)  # Rango alrededor de x0
        f_lambdified = lambdify(x, expr, "numpy")
        f_vals = f_lambdified(x_vals)
        
        deriv_exacta_expr = diff(expr, x)
        deriv_lambdified = lambdify(x, deriv_exacta_expr, "numpy")
        deriv_vals = deriv_lambdified(x_vals)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, f_vals, label=f"f(x) = {expr_str}", color="blue")
        plt.plot(x_vals, deriv_vals, label=f"f'(x) = {latex(deriv_exacta_expr)}", color="red", linestyle="--")
        plt.axhline(y=0, color="black", linewidth=0.5, linestyle="--")
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
        plt.close()
        
        # Retornar los resultados con la gráfica (aplicando redondeo si es necesario)
        return {
            "expresion_original": latex(expr),
            "derivada_exacta": latex(deriv_exacta_expr),
            "valor_derivada_exacta": redondear(exact_val),
            "derivada_adelante": redondear(derivada_adelante.evalf()),
            "derivada_atras": redondear(derivada_atras.evalf()),
            "derivada_centrada": redondear(derivada_centrada.evalf()),
            "error_adelante": redondear(error_adelante),
            "error_atras": redondear(error_atras),
            "error_centrada": redondear(error_centrada),
            "metodo_menor_error": min_error_method,
            "x_val": x0,
            "graph_html": f'<img src="data:image/png;base64,{graph_data}" alt="Gráfica de la función y su derivada"/>'
        }
    except Exception as e:
        return {
            "error": "Lo sentimos, ocurrió un error al procesar la expresión. "
                     "Verifica que la sintaxis sea correcta y vuelve a intentarlo."
        }