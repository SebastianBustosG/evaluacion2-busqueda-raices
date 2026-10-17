import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analisis import barras_iteraciones, etiqueta, raiz_referencia
from funciones import por_id
from metodos import (MAX_IT, biseccion, falsa_posicion, newton, punto_fijo, secante)

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(BASE, "data")
ASSETS = os.path.join(BASE, "assets")

INTERVALOS = {
    "fun1_polinomica_simple": [(1, 2), (0, 3), (-5, 10), (1, 100), (-100, 100)],
    "fun3_logaritmica": [(2, 3), (1, 10), (0.5, 100)],
    "fun5_trigonometrica": [(0, 1), (-1, 2), (-10, 10)],
}
X0 = {
    "fun1_polinomica_simple": [-1, 0, 0.5, 0.6, 1.5, 3, 10],
    "fun3_logaritmica": [0.05, 0.5, 2.5, 10, 100],
    "fun4_exponencial": [-5, 0.5, 5, 20],
    "fun5_trigonometrica": [0.5, 1, 3, 10, -5],
}


def escribir_csv(ruta, encabezado, filas):
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(encabezado)
        w.writerows(filas)


def main():
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(ASSETS, exist_ok=True)

    # ---------------- A) intervalo inicial ----------------
    filas = []
    fig, axs = plt.subplots(1, len(INTERVALOS), figsize=(15, 4.8))
    for ax, (id_, ints) in zip(axs, INTERVALOS.items()):
        fn = por_id(id_)
        series = {"Bisección": [], "Falsa posición": []}
        for a, b in ints:
            rb = biseccion(fn["f"], a, b)
            rf = falsa_posicion(fn["f"], a, b)
            series["Bisección"].append(rb)
            series["Falsa posición"].append(rf)
            for nombre, r in (("Bisección", rb), ("Falsa posición", rf)):
                filas.append([id_, nombre, a, b, b - a, etiqueta(r), r["iteraciones"],
                              f"{r['raiz']:.8f}", r["estado"]])
        barras_iteraciones(ax, [f"[{a:g}, {b:g}]" for a, b in ints], series,
                           fn["texto"], "Intervalo inicial")
        ax.legend(fontsize=8)
    fig.suptitle("Efecto del intervalo inicial en los métodos cerrados")
    fig.tight_layout()
    fig.savefig(os.path.join(ASSETS, "sensibilidad_intervalo.png"), dpi=150)
    plt.close(fig)
    escribir_csv(os.path.join(DATA, "experimento_intervalo.csv"),
                 ["id", "metodo", "a", "b", "ancho", "resultado", "iteraciones", "raiz", "estado"], filas)
    print("A) Intervalo inicial")
    for f_ in filas:
        print("  ", f_)

    # ---------------- B) estimación inicial ----------------
    filas = []
    fig, axs = plt.subplots(2, 2, figsize=(14, 9))
    for ax, (id_, x0s) in zip(axs.ravel(), X0.items()):
        fn = por_id(id_)
        raiz = raiz_referencia(fn)
        series = {"Punto fijo": [], "Secante": [], "Newton-Raphson": []}
        for x0 in x0s:
            rs = {
                "Punto fijo": punto_fijo(fn["g"], fn["f"], x0),
                "Secante": secante(fn["f"], x0, x0 + 0.5),
                "Newton-Raphson": newton(fn["f"], fn["df"], x0),
            }
            for nombre, r in rs.items():
                series[nombre].append(r)
                a_raiz = abs(r["raiz"] - raiz) if r["iteraciones"] else float("nan")
                filas.append([id_, nombre, x0, etiqueta(r), r["iteraciones"],
                              f"{r['raiz']:.8f}", f"{a_raiz:.2e}", r["estado"]])
        barras_iteraciones(ax, [f"{x:g}" for x in x0s], series, fn["texto"], "Estimación inicial x0")
        ax.legend(fontsize=8, loc="upper left")
    fig.suptitle("Efecto de la estimación inicial en los métodos abiertos "
                 "(secante usa x0 y x0 + 0,5; NC = no convergió, barra rayada)")
    fig.tight_layout()
    fig.savefig(os.path.join(ASSETS, "sensibilidad_x0.png"), dpi=150)
    plt.close(fig)
    escribir_csv(os.path.join(DATA, "experimento_x0.csv"),
                 ["id", "metodo", "x0", "resultado", "iteraciones", "raiz", "|raiz - ref|", "estado"], filas)
    print("\nB) Estimación inicial")
    for f_ in filas:
        print("  ", f_)

    # ---------------- C) distintos despejes g(x) ----------------
    casos = [
        ("fun1_polinomica_simple", "g(x) = ∛(x + 2)", lambda x: np.cbrt(x + 2), 1.5),
        ("fun1_polinomica_simple", "g(x) = x³ − 2", lambda x: x**3 - 2, 1.5),
        ("fun6_mixta", "g(x) = cos²(x)", lambda x: np.cos(x) ** 2, 0.55),
        ("fun6_mixta", "g(x) = x − 0,5·f(x)", lambda x: x - 0.5 * (np.sqrt(x) - np.cos(x)), 0.55),
    ]
    filas = []
    for id_, txt, g, x0 in casos:
        fn = por_id(id_)
        r = punto_fijo(g, fn["f"], x0)
        filas.append([id_, txt, x0, etiqueta(r), r["iteraciones"], f"{r['raiz']:.8g}", r["estado"]])
    escribir_csv(os.path.join(DATA, "experimento_punto_fijo_g.csv"),
                 ["id", "g(x)", "x0", "resultado", "iteraciones", "ultimo_x", "estado"], filas)
    print("\nC) Punto fijo con distintos g(x)")
    for f_ in filas:
        print("  ", f_)


if __name__ == "__main__":
    main()