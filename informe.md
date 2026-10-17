# Informe Laboratorio: La raíz que se esconde

* Asignatura: Computación Numérica S2 [INF321].
* Integrantes: Cristobal Aguilera - Sebastián Bustos.
* Fecha: 16 de octubre 2026.

## 1. Preguntas de Convergencia

### 1.1. ¿Qué método convergió en menos iteraciones en cada función?¿Por qué?

El método que convergió en menos iteraciones fue el Newton-Raphson en sus dos versiones, como se ve a continuación:

- **$x^3 - x - 2$, $e^{-x} - x$, $\sqrt{x} - \cos(x)$:** Newton-Raphson y Newton mejorado (2 iteraciones).
- **$\cos(x) - x$:** Newton y Newton mejorado (3).
- **$\ln(x) + x - 4$:** empate entre secante, Newton y Newton mejorado (3).
- **$(x - 2)^2$:** Newton mejorado, con **1** iteración.

Esto de debe a que Newton-Raphson usa la pendiente exacta de la curva, y debido a eso en una raíz simple el número de digitos correctos se duplicar al aumentar los paso, o en otras palabras tiene convergencia cuadrática.

### 1.2. ¿Qué orden de convergencia tiene cada método y cómo se refleja en el gráfico $\vert error \vert$ vs iteración?

- **Convergencia Lineal (Bisección, Falsa Posición, Punto Fijo):** En los gráficos logarítmicos, esto se ve como una línea recta en bajada constante y pareja.
- **Convergencia Superlineal (Secante):** Se refleja en una curva que cae un poco más rápido y en picada que los métodos lineales.
- **Convergencia Cuadrática (Newton-Raphson y Mejorado):** En el gráfico, el error se desploma drásticamente, viéndose como una caída casi vertical en muy pocos pasos.

### 1.3. ¿Qué métodos requieren un intervalo con cambio de signo y cuáles no?

Los métodos que requiren un intervalo con cambio de signo son los denominados **métodos cerrados**, los cuáles son:
* Método de bisección.
* Método de falsa posición.

Lo comprueban al inicio y, si no se cumple, no se pueden ejecutar.

Los métodos que **NO** requieren un intervalo con cambio de signo son los denominados **métodos abiertos**, los cuáles son:
* Método punto fijo.
* Método de la secante.
* Método Newton-Raphson y Newton-Raphson mejorado.

Parten de una estimación (o dos) y no necesitan encerrar la raíz, pero estos no garantizan una convergencia. 

### 1.4. En la función que toca el eje x (raíz doble): ¿qué métodos fallan o no aplican y cuál se comporta mejor?

En la función $(x-2)^2$, la curva rebota en el eje y nunca cambia de signo. Por lo tanto:

- **Falla o no aplica:** La Bisección y la Falsa Posición marcan "N/A" (no aplican) y el Punto Fijo simplemente no converge.
- **Se comporta mejor:** El método de **Newton Mejorado**, el cual encuentra la raíz en exactamente 1 iteración. Esto pasa porque su fórmula está matemáticamente diseñada para evitar problemas cuando la derivada se acerca a cero en la raíz.

### 1.5. ¿Cómo influyen el intervalo inicial y la estimación inicial en las iteraciones y en la convergencia?

- **Intervalo inicial (métodos cerrados):** Agrandar el intervalo hace que la Bisección se demore más pasos (por ejemplo, pasar de $[1, 2]$ a $[-100, 100]$ sube de 20 a 28 iteraciones). En la Falsa Posición es más grave: un intervalo muy amplio o mal elegido hace que el método se estanque y no converja en absoluto.
- **Estimación inicial (métodos abiertos):** Es vital para que funcionen. Si el punto de partida $x_0$ está muy lejos de la raíz, el método puede irse hacia el infinito o fallar totalmente. Por ejemplo, en $\cos(x)-x$, empezar en $x_0 = 10$ hizo que Newton fallara, pero al empezar cerca ($x_0 = 0.5$), lo resolvió en solo 3 pasos.

### 1.6. ¿Qué método recomiendan según el tipo de función (velocidad vs robustez)?

* Si se conoce un **intervalo con cambio de signo** y se quiere **seguridad** de convergencia, el método más adecuado sería **Bisección** dado a su característica de que siempre converge.
* Si tenemos una función **logarítmica**, **exponencial**, **trigonométrica** o **mixta** y se tiene una buena estimación inicial, el método más adecuado sería **Newton-Raphson** (o secante si no se tiene la derivada).
* Si tenemos una función **logarítmica**, **exponencial**, **trigonométrica** o **mixta** y se tiene una buena estimación inicial, pero no se cuenta con la derivada de la función el método más adecuado sería el de la **secante**.
* Si tenemos un **Polinomio de raíz simple**, el método más adecuado sería **Newton-Raphson** (o tambíen se podría combinar bisección y Newton-Raphson).
* Si tenemos una **Raíz doble** sin cambio de signo, el método más adecuado sería **Newton-Raphson mejorado**.

## 2. Conclusión

La elección del método ideal es siempre un compromiso entre qué tan seguro es y qué tan rápido llega. Los métodos abiertos demostraron ser extremadamente rápidos, llegando a la tolerancia en un par de pasos gracias a su convergencia cuadrática, pero los experimentos de sensibilidad comprobaron que fallan si se les da una mala aproximación inicial. Por otro lado, los métodos cerrados son robustos, pero quedan completamente inútiles frente a raíces dobles porque exigen un cambio de signo que no existe. En la práctica, la mejor estrategia suele ser combinar ambos mundos: usar un método robusto como la Bisección para acercarse a la zona de la raíz, y luego cambiar a Newton-Raphson para rematar el cálculo a la máxima velocidad posible.