import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from metodos import (METODOS, MAX_IT, TOL, biseccion, falsa_posicion,
                     punto_fijo, secante, newton, newton_mejorado)

COLORES = {
    "Bisección": "#1b79bb", "Falsa posición": "#ff7f0e", "Punto fijo": "#2aab2a",
    "Secante": "#8539cc", "Newton-Raphson": "#d62728", "Newton mejorado": "#17becf",
}
MARCAS = {
    "Bisección": "o", "Falsa posición": "s", "Punto fijo": "^",
    "Secante": "D", "Newton-Raphson": "v", "Newton mejorado": "P",
}


# =================================================
# =============== Operaciones =====================
# =================================================

# Raiz verdadera
def raiz_referencia(fn):
    if fn["doble"]:
        return 2.0  # raíz exacta conocida de (x - 2)^2
    a, b, f = fn["a"], fn["b"], fn["f"]
    fa = f(a)
    for _ in range(200):
        c = (a + b) / 2
        fc = f(c)
        if fa * fc <= 0:
            b = c
        else:
            a, fa = c, fc
    return (a + b) / 2


def correr_metodos(fn, tol=TOL, max_it=MAX_IT):
    f, df, d2f, g = fn["f"], fn["df"], fn["d2f"], fn["g"]
    return {
        "Bisección": biseccion(f, fn["a"], fn["b"], tol, max_it),
        "Falsa posición": falsa_posicion(f, fn["a"], fn["b"], tol, max_it),
        "Punto fijo": punto_fijo(g, f, fn["x0"], tol, max_it),
        "Secante": secante(f, fn["sec"][0], fn["sec"][1], tol, max_it),
        "Newton-Raphson": newton(f, df, fn["x0"], tol, max_it),
        "Newton mejorado": newton_mejorado(f, df, d2f, fn["x0"], tol, max_it),
    }


def errores(res, raiz):
    return np.abs(np.array(res["xs"]) - raiz)


def orden_empirico(err):
    """p ≈ ln(e_{n+1}/e_n) / ln(e_n/e_{n-1}); mediana de las últimas estimaciones válidas."""
    vals = []
    for i in range(2, len(err)):
        e0, e1, e2 = err[i - 2], err[i - 1], err[i]
        if min(e0, e1, e2) > 1e-13 and e0 > e1 > e2:
            vals.append(np.log(e2 / e1) / np.log(e1 / e0))
    return float(np.median(vals[-3:])) if vals else float("nan")


def etiqueta(res):
    if not res["aplica"]:
        return "N/A"
    if not res["convergio"]:
        return "NC"
    return str(res["iteraciones"])

# =================================================
# =============== Graficos =====================
# =================================================

def grafico_funcion(fn, raiz, ruta):
    x = np.linspace(*fn["rango"], 600)
    with np.errstate(all="ignore"):
        y = fn["f"](x)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color="#1f77b4", lw=2, label=fn["texto"])
    ax.axhline(0, color="black", lw=0.8)
    a, b = fn["a"], fn["b"]
    ax.axvspan(a, b, color="#ffe9a8", alpha=0.45,
               label=f"Intervalo [{a:g}, {b:g}]")
    ax.plot([a, b], [fn["f"](a), fn["f"](b)], "gs", ms=8,
            label=f"f(a) = {fn['f'](a):.3f}, f(b) = {fn['f'](b):.3f}")
    ax.plot(raiz, 0, "r*", ms=18, zorder=5, label=f"Raíz ≈ {raiz:.6f}")
    if fn["doble"]:
        ax.annotate("Tangencia al eje x:\nf(2) = 0 y f'(2) = 0\n(sin cambio de signo)",
                    xy=(raiz, 0), xytext=(2.15, 0.55),
                    arrowprops=dict(arrowstyle="->"), fontsize=10)
        titulo = f"{fn['nombre']}: {fn['texto']} (raíz doble)"
    else:
        titulo = f"{fn['nombre']}: {fn['texto']}"
    ax.set_title(titulo)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(alpha=0.3)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def grafico_convergencia(fn, resultados, raiz, ruta):
    fig, ax = plt.subplots(figsize=(8, 5))
    omitidos = []
    for m in METODOS:
        r = resultados[m]
        if not r["aplica"]:
            omitidos.append(f"{m}: N/A")
            continue
        if r["iteraciones"] == 0:
            omitidos.append(f"{m}: NC ({r['estado']})")
            continue
        e = np.maximum(errores(r, raiz), 1e-17)  # piso para poder graficar en log
        estilo = "-" if r["convergio"] else "--"
        nombre = m if r["convergio"] else f"{m} (NC)"
        ax.semilogy(np.arange(1, len(e) + 1), e, estilo, marker=MARCAS[m],
                    color=COLORES[m], ms=5, label=nombre)
    ax.axhline(TOL, color="gray", ls=":", label="Tolerancia 1e-6")
    ax.set_title(f"Convergencia: {fn['texto']}")
    ax.set_xlabel("Iteración")
    ax.set_ylabel("|error| = |x − raíz| (escala log)")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="best")
    if omitidos:
        ax.text(0.01, 0.01, "No graficados: " + "; ".join(omitidos), transform=ax.transAxes,
                fontsize=7, va="bottom", color="dimgray")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def barras_iteraciones(ax, categorias, series, titulo, xlabel):
    """Barras agrupadas de iteraciones. 'series': {método: [resultados por categoría]}."""
    n = len(series)
    ancho = 0.8 / n
    x = np.arange(len(categorias))
    for i, (nombre, lista) in enumerate(series.items()):
        valores = [0 if not r["aplica"] else r["iteraciones"] for r in lista]
        barras = ax.bar(x + (i - (n - 1) / 2) * ancho, valores, ancho,
                        label=nombre, color=COLORES[nombre])
        for barra, r in zip(barras, lista):
            if r["aplica"] and not r["convergio"]:
                barra.set_hatch("///")
                barra.set_edgecolor("red")
            ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 1,
                    etiqueta(r), ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=8)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Iteraciones")
    ax.set_ylim(0, MAX_IT * 1.15)
    ax.grid(alpha=0.3, axis="y")


def grafico_resumen(funciones, todos, ruta):
    fig, ax = plt.subplots(figsize=(14, 6))
    cats = [fn["texto"] for fn in funciones]
    series = {m: [todos[fn["id"]][m] for fn in funciones] for m in METODOS}
    barras_iteraciones(ax, cats, series, "Iteraciones por método y función (tol = 1e-6, tope = 100)",
                       "Función")
    ax.legend(ncol=3, fontsize=8, loc="upper right")
    fig.text(0.01, 0.01, "N/A = no aplica (sin cambio de signo)   NC = no convergió (barra rayada)",
             fontsize=8, color="dimgray")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(ruta, dpi=150)
    plt.close(fig)