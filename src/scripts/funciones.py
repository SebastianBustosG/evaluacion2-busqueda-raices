import numpy as np


def _fn(id, nombre, texto, f, df, d2f, g, g_texto, a, b, x0, sec, rango, doble=False):
    return dict(id=id, nombre=nombre, texto=texto, f=f, df=df, d2f=d2f, g=g,
                g_texto=g_texto, a=a, b=b, x0=x0, sec=sec, rango=rango, doble=doble)


FUNCIONES = [
    _fn("fun1_polinomica_simple", "Polinómica (raíz simple)", "f(x) = x³ − x − 2",
        lambda x: x**3 - x - 2,
        lambda x: 3 * x**2 - 1,
        lambda x: 6 * x,
        lambda x: np.cbrt(x + 2), "g(x) = ∛(x + 2)",
        1.0, 2.0, 1.5, (1.0, 2.0), (0.5, 2.5)),

    _fn("fun2_polinomica_doble", "Polinómica (raíz doble)", "f(x) = (x − 2)²",
        lambda x: (x - 2) ** 2,
        lambda x: 2 * (x - 2),
        lambda x: 2.0 + 0 * x,
        lambda x: x + (x - 2) ** 2, "g(x) = x + (x − 2)²",
        1.0, 3.0, 1.2, (1.2, 1.5), (1.0, 3.0), doble=True),

    _fn("fun3_logaritmica", "Logarítmica", "f(x) = ln(x) + x − 4",
        lambda x: np.log(x) + x - 4,
        lambda x: 1 / x + 1,
        lambda x: -1 / x**2,
        lambda x: 4 - np.log(x), "g(x) = 4 − ln(x)",
        2.0, 3.0, 2.5, (2.0, 3.0), (0.5, 4.5)),

    _fn("fun4_exponencial", "Exponencial", "f(x) = e^(−x) − x",
        lambda x: np.exp(-x) - x,
        lambda x: -np.exp(-x) - 1,
        lambda x: np.exp(-x),
        lambda x: np.exp(-x), "g(x) = e^(−x)",
        0.0, 1.0, 0.5, (0.0, 1.0), (-0.5, 1.5)),

    _fn("fun5_trigonometrica", "Trigonométrica", "f(x) = cos(x) − x",
        lambda x: np.cos(x) - x,
        lambda x: -np.sin(x) - 1,
        lambda x: -np.cos(x),
        lambda x: np.cos(x), "g(x) = cos(x)",
        0.0, 1.0, 0.5, (0.0, 1.0), (-0.5, 1.5)),

    _fn("fun6_mixta", "Mixta", "f(x) = √x − cos(x)",
        lambda x: np.sqrt(x) - np.cos(x),
        lambda x: 1 / (2 * np.sqrt(x)) + np.sin(x),
        lambda x: -1 / (4 * x**1.5) + np.cos(x),
        lambda x: x - 0.5 * (np.sqrt(x) - np.cos(x)), "g(x) = x − 0,5·f(x)",
        0.1, 1.0, 0.55, (0.1, 1.0), (0.0, 1.5)),
]

def por_id(id_):
    return next(fn for fn in FUNCIONES if fn["id"] == id_)