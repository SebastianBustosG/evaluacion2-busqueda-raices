import csv
import os

import numpy as np

from analisis import (correr_metodos, errores, etiqueta, grafico_convergencia,
                      grafico_funcion, grafico_resumen, orden_empirico, raiz_referencia)
from funciones import FUNCIONES
from metodos import MAX_IT, METODOS, TOL

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(BASE, "data")
ASSETS = os.path.join(BASE, "assets")


def escribir_csv(ruta, encabezado, filas):
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(encabezado)
        w.writerows(filas)


def main():
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(ASSETS, exist_ok=True)

    ambiente, resumen, historial = [], [], []
    todos = {}

    for fn in FUNCIONES:
        f = fn["f"]
        raiz = raiz_referencia(fn)

        # CSV (x, f(x))
        x = np.linspace(*fn["rango"], 400)
        with np.errstate(all="ignore"):
            y = f(x)
        np.savetxt(os.path.join(DATA, fn["id"] + ".csv"), np.column_stack([x, y]),
                   delimiter=",", header="x,f(x)", comments="", fmt="%.10g")

        # Ambiente controlado: demostración de raíz en el rango
        fa, fb = float(f(fn["a"])), float(f(fn["b"]))
        if fn["doble"]:
            xs_fino = np.linspace(*fn["rango"], 20001)
            minimo = float(np.min(f(xs_fino)))
            demo = (f"Tangencia: f(2) = {float(f(2.0)):g}, f'(2) = {float(fn['df'](2.0)):g}, "
                    f"min f(x) en el rango = {minimo:g} >= 0 (sin cambio de signo)")
        else:
            demo = f"Bolzano: f(a)·f(b) = {fa * fb:.4g} < 0" if fa * fb < 0 else "SIN cambio de signo"
        ambiente.append([fn["id"], fn["texto"], fn["a"], fn["b"], f"{fa:.6g}", f"{fb:.6g}",
                         f"{fa * fb:.6g}", fn["x0"], fn["sec"][0], fn["sec"][1], fn["g_texto"],
                         TOL, MAX_IT, f"{raiz:.12f}", demo])

        # Ejecucion de los 6 métodos
        res = correr_metodos(fn)
        todos[fn["id"]] = res
        for m in METODOS:
            r = res[m]
            err = errores(r, raiz)
            ef = float(err[-1]) if len(err) else float("nan")
            orden = float("nan") if m == "Bisección" else orden_empirico(err)
            resumen.append([fn["id"], fn["texto"], m, etiqueta(r), r["iteraciones"],
                            f"{r['raiz']:.10f}", f"{ef:.3e}",
                            f"{abs(f(r['raiz'])):.3e}" if len(err) else "nan",
                            r["convergio"], r["estado"], f"{orden:.2f}"])
            for k, xk in enumerate(r["xs"], start=1):
                historial.append([fn["id"], m, k, f"{xk:.12f}", f"{float(f(xk)):.4e}",
                                  f"{abs(xk - raiz):.4e}"])

        # Gráficos por función
        grafico_funcion(fn, raiz, os.path.join(ASSETS, fn["id"] + "_funcion.png"))
        grafico_convergencia(fn, res, raiz, os.path.join(ASSETS, fn["id"] + "_convergencia.png"))

    grafico_resumen(FUNCIONES, todos, os.path.join(ASSETS, "resumen_iteraciones.png"))

    escribir_csv(os.path.join(DATA, "ambiente_controlado.csv"),
                 ["id", "funcion", "a", "b", "f(a)", "f(b)", "f(a)*f(b)", "x0_newton_pf",
                  "x0_secante", "x1_secante", "g(x)_punto_fijo", "tolerancia", "max_iter",
                  "raiz_referencia", "demostracion"], ambiente)
    escribir_csv(os.path.join(DATA, "resumen_convergencia.csv"),
                 ["id", "funcion", "metodo", "resultado", "iteraciones", "raiz", "error_final",
                  "|f(raiz)|", "convergio", "estado", "orden_empirico"], resumen)
    escribir_csv(os.path.join(DATA, "historial_iteraciones.csv"),
                 ["id", "metodo", "iteracion", "x", "f(x)", "error"], historial)

    # Resumen en consola
    print(f"Tolerancia = {TOL:g} | tope de iteraciones = {MAX_IT}\n")
    print(f"{'Función':<22}" + "".join(f"{m:>17}" for m in METODOS))
    for fn in FUNCIONES:
        print(f"{fn['texto']:<22}" + "".join(f"{etiqueta(todos[fn['id']][m]):>17}" for m in METODOS))
    print("\n(N/A = no aplica, NC = no convergió)\n")
    for fila in resumen:
        print(f"{fila[0]:<22}{fila[2]:<17}it={fila[4]:<4}raiz={fila[5]:<16}err={fila[6]:<11}"
              f"|f|={fila[7]:<11}p={fila[10]:<6}{fila[9]}")


if __name__ == "__main__":
    main()