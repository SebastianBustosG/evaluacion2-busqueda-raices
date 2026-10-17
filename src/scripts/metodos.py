import numpy as np

TOL = 1e-6 # Tolerancia
MAX_IT = 100 # Maximo de iteraciones

METODOS = ["Bisección", "Falsa posición", "Punto fijo", "Secante", "Newton-Raphson", "Newton mejorado"]

# Empaqueta y estandariza la salida del método (historial, iteraciones, raíz hallada, éxito y estado) en un diccionario.
def _res(xs, convergio, estado, aplica=True):
    return {
        "xs": [float(x) for x in xs],
        "iteraciones": len(xs),
        "raiz": float(xs[-1]) if len(xs) else float("nan"),
        "convergio": convergio,
        "aplica": aplica,
        "estado": estado,
    }

# Evalúa si se alcanzó la raíz por residuo o convergencia entre pasos.
def _parar(f, xs, tol):
    x = xs[-1]
    if abs(f(x)) < tol:
        return True
    return len(xs) > 1 and abs(x - xs[-2]) < tol



# Metodo de biseccion (cerrado)
def biseccion(f, a, b, tol=TOL, max_it=MAX_IT):
    with np.errstate(all = "ignore"):
        fa, fb = f(a), f(b)
        if fa * fb > 0:
            return _res([], False, "no aplica: f(a)·f(b) > 0 (sin cambio de signo)", False)
        xs = []
        for _ in range(max_it):
            c = (a + b) / 2
            fc = f(c)
            xs.append(c)
            if _parar(f, xs, tol):
                return _res(xs, True, "converge")
            if fa * fc < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc
    return _res(xs, False, "tope de iteraciones")

# Metodo de falsa posicion (cerrado)
def falsa_posicion(f, a, b, tol=TOL, max_it=MAX_IT):
    with np.errstate(all="ignore"):
        fa, fb = f(a), f(b)
        if fa * fb > 0:
            return _res([], False, "no aplica: f(a)·f(b) > 0 (sin cambio de signo)", False)
        xs = []
        for _ in range(max_it):
            if fb - fa == 0:
                return _res(xs, False, "división por cero (f(a) = f(b))")
            c = (a * fb - b * fa) / (fb - fa)
            fc = f(c)
            xs.append(c)
            if _parar(f, xs, tol):
                return _res(xs, True, "converge")
            if fa * fc < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc
    return _res(xs, False, "tope de iteraciones")

# Metodo del punto fijo (abierto)
def punto_fijo(g, f, x0, tol=TOL, max_it=MAX_IT):
    """x_{n+1} = g(x_n).  f solo se usa para el criterio |f(x)| < tol."""
    xs = []
    x = x0
    with np.errstate(all = "ignore"):
        for _ in range(max_it):
            x = g(x)
            if not np.isfinite(x) or abs(x) > 1e12:
                return _res(xs, False, "diverge (valor no finito o enorme)")
            xs.append(x)
            if _parar(f, xs, tol):
                return _res(xs, True, "converge")
            if len(xs) == 1 and abs(x - x0) < tol:
                return _res(xs, True, "converge")
    return _res(xs, False, "tope de iteraciones")

# Metodo de la secante (abierto)
def secante(f, x0, x1, tol=TOL, max_it=MAX_IT):
    xs = []
    xp, x = x0, x1
    with np.errstate(all ="ignore"):
        for _ in range(max_it):
            fp, fx = f(xp), f(x)
            if fx - fp == 0 or not np.isfinite(fx - fp):
                return _res(xs, False, "división por cero (f(x_{n-1}) = f(x_n))")
            xn = x - fx * (x - xp) / (fx - fp)
            if not np.isfinite(xn) or abs(xn) > 1e12:
                return _res(xs, False, "diverge (valor no finito o enorme)")
            xs.append(xn)
            if _parar(f, xs, tol):
                return _res(xs, True, "converge")
            xp, x = x, xn
    return _res(xs, False, "tope de iteraciones")

# Metodo de Newton-Raphson (abierto)
def newton(f, df, x0, tol=TOL, max_it=MAX_IT):
    xs = []
    x = x0
    with np.errstate(all="ignore"):
        for _ in range(max_it):
            d = df(x)
            if d == 0 or not np.isfinite(d):
                return _res(xs, False,"derivada nula o no finita (f'(x) = 0)")
            xn = x - f(x) / d
            if not np.isfinite(xn) or abs(xn) > 1e12:
                return _res(xs, False, "diverge (valor no finito o enorme)")
            xs.append(xn)
            if _parar(f, xs, tol):
                return _res(xs, True,"converge")
            x = xn
    return _res(xs, False, "tope de iteraciones")

# Metodo Newton-Raphson mejorado (abierto)
def newton_mejorado(f, df, d2f, x0, tol=TOL, max_it=MAX_IT):
    xs = []
    x = x0
    with np.errstate(all = "ignore"):
        for _ in range(max_it):
            fx, d, d2 = f(x), df(x), d2f(x)
            den = d * d - fx * d2
            if den == 0 or not np.isfinite(den):
                return _res(xs,False,"denominador nulo (f'^2 - f·f'' = 0)")
            xn = x - fx * d / den
            if not np.isfinite(xn) or abs(xn) > 1e12:
                return _res(xs,False, "diverge (valor no finito o enorme)")
            xs.append(xn)
            if _parar(f, xs, tol):
                return _res( xs, True, "converge")
            x = xn
    return _res(xs,False,"tope de iteraciones")