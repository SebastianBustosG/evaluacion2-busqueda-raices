# Búsqueda de Raíces y Análisis de Convergencia

Este repositorio contiene la Evaluación 2 de la asignatura Computación Numérica (INF321): "La raíz que se esconde". El objetivo principal del proyecto es implementar, probar y comparar la eficiencia de seis métodos numéricos de búsqueda de raíces en un entorno controlado.

A través de este laboratorio, analizamos el costo computacional (cantidad de iteraciones) y el orden de convergencia de métodos cerrados y abiertos frente a distintas naturalezas matemáticas (funciones polinómicas, logarítmicas, exponenciales, trigonométricas, mixtas y el caso crítico de una raíz doble sin cambio de signo).

## Integrantes
- Cristóbal Aguilera
- Sebastián Bustos

## Métodos Implementados
El proyecto incluye el desarrollo manual mediante `numpy` de los siguientes algoritmos, todos con un criterio de parada basado en una tolerancia estricta de `1e-6`:
1. Método de Bisección
2. Método de Falsa Posición
3. Método de Punto Fijo
4. Método de la Secante
5. Método de Newton-Raphson
6. Método de Newton-Raphson Mejorado

## Cómo montar el entorno de ejecución

Este proyecto utiliza un entorno virtual de Python (`venv`) para aislar las dependencias (principalmente `numpy` y `matplotlib`). Sigue estos pasos para configurarlo y ejecutar el código:

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/SebastianBustosG/evaluacion2-busqueda-raices.git
   cd evaluacion2-busqueda-raices
   ```

2. **Crea el entorno virtual:**
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual:**
   - En **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - En **Linux / macOS**:
     ```bash
     source venv/bin/activate
     ```

4. **Instala las dependencias necesarias:**
   ```bash
   pip install -r requirements.txt
   ```

## Estructura del proyecto

El repositorio sigue una arquitectura modular estricta para separar la lógica matemática de la extracción de datos y la generación de recursos visuales:

```text
evaluacion2-busqueda-raices/
├── README.md                  <- Documentación e instrucciones del proyecto.
├── requirements.txt           <- Lista de librerías requeridas (numpy, matplotlib).
├── informe.md                 <- Respuestas formales al análisis de convergencia y conclusiones.
└── src/
    ├── assets/                <- Contiene los gráficos PNG (funciones con su raíz y curvas de convergencia logarítmica).
    ├── data/                  <- Archivos CSV con los datos crudos extraídos de las iteraciones.
    └── scripts/               <- Código fuente en Python.
```

## Descripción de los Scripts (`src/scripts/`)

Para mantener el código ordenado y escalable, la lógica se dividió en los siguientes módulos:

*   `funciones.py`: Define matemáticamente las 6 funciones a evaluar (y sus derivadas cuando es necesario) garantizando el ambiente controlado.
*   `metodos.py`: Contiene la implementación algorítmica pura de los seis métodos numéricos de búsqueda de raíces.
*   `experimentos.py`: Script encargado de ejecutar los métodos sobre las funciones, recolectar el número de iteraciones y errores, y automatizar la exportación de resultados hacia los archivos `.csv` en la carpeta `data/`.
*   `analisis.py`: Utiliza `matplotlib` para leer los datos y generar de forma automatizada las gráficas comparativas de $|error|$ vs iteración, guardándolas en la carpeta `assets/`.
*   `main.py`: Archivo orquestador principal que coordina la ejecución de todos los módulos anteriores.