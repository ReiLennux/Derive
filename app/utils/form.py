
import json


#  Kury XD
def f(x):
    return x**3 - x

# Brandon XD
def derivative(x):
    return 3 * x**2 - 1

def x_plus_h(x, h):
    return x + h

def x_minus_h(x, h):
    return x - h

def derivative_progressive(x, h):
    return (f(x_plus_h(x,h)) - f(x)) / h

def derivative_regressive(x, h):
    return (f(x) - f(x_minus_h(x,h))) / h

def derivative_central(x, h):
    return (f(x_plus_h(x,h)) - f(x_minus_h(x,h)) ) / (2 * h)

def check(dp, dr, dc, dreal):
    valores = {
        'derivada progresiva': dp, 
        'derivada regresiva': dr, 
        'derivada central': dc
        }
    mas_cercano = min(valores, key=lambda k: abs(valores[k] - dreal))
    return mas_cercano


def error(dp, dr, dc, dreal):
    return json.dumps({
        'e_progresiva': (dp - dreal),
        'e_regresiva': (dr - dreal),
        'e_central': (dc - dreal)
    })
    

def main():
    x = 1
    h = 0.1
    dreal = derivative(x)
    dp, dr, dc = derivative_progressive(x, h), derivative_regressive(x, h), derivative_central(x, h)
    mas_cercano = check(dp, dr, dc, dreal)

    print(f'Derivada Progressiva: {dp}')
    print(f'Derivada Regressiva: {dr}')
    print(f'Derivada Central: {dc}')
    print(f'Derivada Más Cercana a {dreal} es: {mas_cercano}')
    print(error(dp, dr, dc, dreal))

main()