from sympy import symbols, sympify, diff, latex
import re

def calcular_derivada(expr_str, x_val):
    try:
        # Reemplaza el operador de potencia '^' por '**' para que Sympy lo reconozca
        expr_str = expr_str.replace('^', '**')
        
        # Inserta el operador de multiplicación implícita en casos como "2x" o "3(x+1)"
        expr_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr_str)
        
        # Define la variable simbólica 'x'
        x = symbols('x')
        
        # Convierte la cadena de la expresión en una expresión simbólica
        expr = sympify(expr_str)
        
        # Calcula la derivada de la expresión respecto a x
        derivada = diff(expr, x)
        
        # Evalúa la derivada en el punto x_val y obtiene un valor numérico
        valor_derivada = derivada.subs(x, x_val).evalf()
        
        # Retorna los resultados en un diccionario
        return {
            "expresion_original": latex(expr),
            "derivada": latex(derivada),
            "valor_evaluado": valor_derivada,
            "x_val": x_val
        }
    except Exception as e:
        return {"error": "Lo sentimos, ocurrió un error al calcular la derivada. Por favor, verifica la expresión ingresada e intenta de nuevo."}