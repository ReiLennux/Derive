from sympy import symbols, sympify, diff, latex

def calcular_derivada(expr_str, x_val):
    try:
        x = symbols('x')
        expr = sympify(expr_str)
        derivada = diff(expr, x)
        valor_derivada = derivada.subs(x, x_val).evalf()
        
        return {
            "expresion_original": latex(expr),
            "derivada": latex(derivada),
            "valor_evaluado": valor_derivada,
            "x_val": x_val
        }
    except Exception as e:
        return {"error": f"Error al calcular: {str(e)}"}