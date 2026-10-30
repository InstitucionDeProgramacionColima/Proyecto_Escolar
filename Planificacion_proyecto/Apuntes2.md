# Explicación del Proyecto: Simulador de Préstamos (versión para el alumno)

> Nota: este archivo resume y explica en palabras simples todo lo que está en `Apuntes.md`.
> Orden: por ideas grandes, no por fecha.

---

## 1. ¿Qué es el proyecto?

Es un programa de computadora (aplicación de escritorio en Windows) que **simula préstamos**.
El usuario mete:

- **Monto** (cuánto pide prestado)
- **Tasa de interés anual** (qué tanto le cobran)
- **Plazo en meses** (en cuánto tiempo lo paga)
- **Sistema de amortización** (francés, alemán o americano)

Y el programa le devuelve la **tabla de pagos** (mes a mes: cuota, interés, capital, saldo),
unas **gráficas**, la posibilidad de **comparar dos cálculos** y un **historial** guardado.

---

## 2. ¿Cómo está armado? (La idea central)

Usa dos lenguajes con roles distintos:

- **C++ = el trabajador que calcula.** Hace el cálculo financiero "puro": recibe números
  y devuelve la tabla sin guardar nada en memoria ni tocar la pantalla. Compilado a un
  archivo `.exe` (`amortizador.exe`).
- **Python = el orquestador que muestra.** Hace la ventana, los botones, las gráficas,
  llama al `.exe` de C++ con `subprocess` y recibe el resultado en **JSON**.

Esto se llama patrón **Orquestador-Trabajador** y también **Functional Core, Imperative Shell**:

```
Usuario → ventana (Python) → subprocess → amortizador.exe (C++) → JSON → ventana
```

En resumen: **C++ calcula, Python muestra.** Así el código de cálculo queda limpio y
reutilizable (funciones puras: mismas entradas → mismas salidas, sin efectos secundarios).

---

## 3. ¿Qué hace cada archivo?

| Archivo | Qué hace en palabras simples |
|---|---|
| `core_cpp/amortizacion.hpp` | Define la "fila" de la tabla y declara las funciones de cálculo. |
| `core_cpp/amortizacion.cpp` | El cálculo real: francés, alemán y americano. Todo puro. |
| `core_cpp/main.cpp` | Recibe los argumentos de la terminal, llama al cálculo, imprime JSON. |
| `core_cpp/amortizador.exe` | El binario compilado que Python ejecuta. |
| `gui/ventana.py` | La ventana: formulario, tabla, pestañas, botones, historial. |
| `gui/graficas.py` | Genera las figuras con `matplotlib` (saldo, interés-capital, A vs B). |
| `gui/ia.py` | Capa de IA (API) para explicar/comparar resultados (módulo aparte). |
| `main.py` | El punto de entrada: arranca la ventana. |
| `gui/Img/generar_recursos.py` | Genera los iconos y el logo `.ico`/`.png`. |
| `historial.json` | Guarda los cálculos hechos para que no se pierdan al cerrar. |

---

## 4. Evolución del proyecto (qué fue pasando)

**Etapa 1 — Estructura (18 sep):** Se crearon las carpetas y los archivos vacíos según
la arquitectura. Conceptos clave: **módulos**, **organización**, funciones puras.

**Etapa 2 — Cálculo en C++ (22 sep):** Se implementó el núcleo. Conceptos: **funciones
puras**, **inmutabilidad**, **transparencia referencial**, y la separación
**Functional Core / Imperative Shell** (cálculo puro adentro, entrada/salida imperativa
afuera). Se compiló con `g++` y se probó en terminal.

**Etapa 3 — Primera ventana (22 sep):** Python llamaba al `.exe` con `subprocess` y
mostraba la tabla. Concepto: **separación de responsabilidades** y **módulos**.

**Etapa 4 — Intento con Flet (22 sep):** Se probó otra librería de interfaz (Flet),
pero tuvo problemas de instalación. Concepto: interfaces declarativas.

**Etapa 5 — Regreso a tkinter (22 sep):** Se volvió a `tkinter` (viene con Python, no
instala nada). Se rehizo la ventana con `ttk`.

**Etapa 6 — Gráficas (24 sep):** Se agregó `graficas.py` con `matplotlib`: curva de saldo
y barras de capital/interés. Se usó un `ttk.Notebook` (pestañas). Concepto: **modularidad**
(2.1.7).

**Etapa 7 — Comparativa entre los 3 sistemas (24 sep):** Las gráficas ahora superponen
francés, alemán y americano para compararlos. Concepto: funciones que reciben un diccionario
con las 3 tablas.

**Etapa 8 — Identidad visual (24 sep):** Icono de la barra de tareas (`ctypes` +
AppUserModelID), icono de ventana y logo de Intresta. Concepto: integración con el
sistema operativo.

**Etapa 9 — Encabezado (26 sep):** Título movido a la derecha, subtítulo eliminado.
Concepto: gestión geométrica (`pack`, `anchor`).

**Etapa 10 — Pestañas principales (26 sep):** Se creó la barra superior con
`Calcular Tabla` / `Comparar` / `Apartado 3` usando un `ttk.Notebook` principal.

**Etapa 11 — Comparar dos cálculos distintos (28 sep):** En `Comparar` se pueden fijar
dos resultados (A y B) y verlos en paralelo, con su diferencia. Solo en memoria,
**sin base de datos**. Conceptos: funciones de resumen con `sum()` (alto orden, Unidad III).

**Etapa 12 — Simplificar gráficas (28 sep):** Se quitaron "Comparativa Saldos" y
"Comparativa Cuotas". Ahora `Calcular Tabla` tiene `Tabla de Pagos` y
`Relación Interés-Capital` (2 barras: capital total vs interés total, con el % en el título).

**Etapa 13 — Micro barra en Comparar (28 sep):** Se quitó el botón "Intercambiar" y se
agregó una mini barra `Tablas` / `Grafica`. La pestaña `Grafica` muestra barras y curvas
comparando A contra B.

**Etapa 14 — Ajustes de diseño (28 sep):** Botones de "Fijar A/B" y "Limpiar" movidos a
la derecha y arriba; se ajustaron tamaños de figuras para que no se vean deformes.

**Etapa 15 — Historial (28 sep):** `Apartado 3` ahora se llama **Historial**. Cada cálculo
se guarda en `historial.json`. Cada fila tiene un botón con `monto | fecha | sistema` a la
izquierda y `Borrar` a la derecha. Al hacer click se recalcula con C++ y se muestra.
Sobrevive al cerrar la app (eso es lo que hace un **JSON**: persistencia ligera sin base
de datos).

**Etapa 15.1 — Renombrar pestaña:** `Apartado 3` → `Historial`.

**Etapa 15.2 — Centrar título:** El título se centró verticalmente a la derecha
(`anchor=E` en vez de `NE`).

**Etapa 15.3 y 15.4 — Intento de fuente global (y reversión):** Se intentó poner la fuente
Segoe UI en todos los widgets con `option_add("*Font", "Segoe UI 10")`, pero esto causó un
error (`_tkinter.TclError: expected integer but got "UI"`) y la ventana ya no abría. Se
revertió. **Lección aprendida:** en tkinter, los `option_add` de font necesitan un formato
con llaves correcto, y conviene no forzar fuentes globales a la ligera.

---

## 5. Conceptos de la materia (plan de materia) usados aquí

- **Unidad I:** fundamentos de programación funcional, tipos, estructuras, módulos.
- **Unidad II:** funciones, parámetros, funciones como objetos, módulos y organización
  (2.1.7), pruebas (2.1.8).
- **Unidad III:** funciones de alto orden (`map`, `filter`, `reduce`, `zip`, `sorted`),
  decoradores, generadores.

En este proyecto los viste así:

- **Funciones puras** = el cálculo de C++ y las funciones de `graficas.py`.
- **Funciones de alto orden** = uso de `sum()`, comprensiones de lista y generadores
  para resumir tablas.
- **Módulos y organización** = `ventana.py`, `graficas.py`, `ia.py`, `core_cpp/`.
- **Orquestador-Trabajador** = Python coordina, C++ trabaja.
- **Persistencia** = `historial.json` (no es base de datos, es un archivo).

---

## 6. Reglas de la rúpica (Roles_and_skills) que se cumplieron

- Registrar cada prompt en `bitacora.md`.
- Documentar en `Apuntes.md` qué hace el código.
- snake_case en variables/funciones/métodos, métodos privados con `_`.
- Constantes en MAYÚSCULAS con guiones bajos.
- Formato: headers/librerías → declaraciones → proceso principal → implementación.
- Describir el proceso y esperar un "Sí" antes de ejecutar.

---

## 7. ¿Dónde estamos ahora y qué sigue?

**Estado actual:**
- `Calcular Tabla`: formulario + tabla de pagos + gráfica de relación interés-capital.
- `Comparar`: dos tablas en paralelo (A/B) + micro barra `Tablas`/`Grafica`.
- `Historial`: guardado persistente en JSON con borrar individual y limpiar todo.
- La app abre correctamente (tras revertir el error de fuente).

**Posibles siguientes pasos:**
- Integrar la capa de IA (`ia.py`) para explicar resultados.
- Empaquetar a un solo `.exe` con PyInstaller (ya se explicó en la bitácora).
- Agregar pruebas unitarias (2.1.8).

---

## 8. ¿Cómo se relaciona con el plan de estudios?

La materia es **PROGRAMACIÓN FUNCIONAL** (3er semestre, Ingeniería en Computación Inteligente, Prof. Mata Lopez Walter Alexander). El plan divide la materia en **tres unidades** con evaluaciones parciales:

### 8.1 Estructura del plan

| Unidad | Período | Evaluación | Conceptos del plan |
|---|---|---|---|
| **Unidad I** | 17/08 - 14/09 | 1.ª Parcial (01/10/2026) | ¿Qué es la programación funcional?, POO vs PF, funciones matemáticas, cambios de estado, tipos de datos, estructuras de datos, control de flujo. |
| **Unidad II** | 15/09 - 01/10 | 1.ª Parcial (01/10/2026) | Funciones, retorno, parámetros, funciones como objetos, recursión, docstrings, **módulos y organización (2.1.7)**, pruebas y depuración (2.1.8). |
| **Unidad III** | 02/10 - 26/11 | 2.ª Parcial (26/11/2026) | Funciones de alto orden (`map`, `filter`, `reduce`, `zip`, `sorted`), decoradores, generadores (`yield`), módulo `operator`. |

### 8.2 Dónde aparece cada concepto en el proyecto

**Unidad I — ¿Qué es la programación funcional?**
- El programa entero aplica PF: el cálculo en C++ es **puro** (funciones sin efectos secundarios, dadas las mismas entradas → misma salida).
- `amortizacion.cpp` no muta variables globales: cada llamada devuelve una nueva tabla. Inmutabilidad de datos.
- Separación **POO vs PF**: C++ es el núcleo funcional puro; Python el orquestador imperativo con estado.

**Unidad I — Tipos de datos, estructuras de datos, control de flujo**
- El JSON que intercambia Python ↔ C++ usa listas (listas de diccionarios con `mes`, `cuota`, `interes`, `capital`, `saldo`).
- El formulario valida con `if` (monto ≤ 0, tasa < 0, plazo ≤ 0) y usa `try/except`.
- Las funciones de Python reciben listas e itera sobre ellas con comprensiones.

**Unidad II — Funciones, parámetros, retorno**
- `calcular_amortizacion()` recibe parámetros y retorna `list[dict]`.
- `calcular_fila_frances(saldo, tasaMensual, cuota)` es función pura: recibe parámetros y retorna una fila.
- `serializar_tabla_json()` retorna JSON sin mutar las listas de entrada.

**Unidad II — Funciones como objetos, recursión**
- Aunque no se usó recursión, `sum(fila["cuota"] for fila in lista)` es una función como objeto aplicada a una colección.
- Los `lambda` en botones (`command=lambda: self._fijar_escenario_comparar("A")`) son funciones anónimas como objetos.

**Unidad II — Módulos y Organización (2.1.7)**
- **Módulos**: `core_cpp/`, `gui/ventana.py`, `gui/graficas.py`, `gui/ia.py`, `main.py` son módulos separados.
- Cada módulo tiene una responsabilidad única (principio de separación de responsabilidades).
- Importaciones: `from gui.graficas import generar_figura_relacion_interes_capital`.
- `__init__.py` permite importar con `import gui.ventana`.

**Unidad II — Pruebas y Depuración (2.1.8)**
- Se compiló y probó `amortizador.exe` en terminal con los 3 sistemas.
- `assert` y pruebas unitarias serían el siguiente paso (pendiente).

**Unidad III — Funciones de alto orden**
- `sum()` es una función de alto orden: recibe un iterable y retorna un acumulado.
- Comprensiones de lista (`[fila["cuota"] for fila in lista_filas]`) son funciones de alto orden implícitas.
- `max(valores)`, `min(valores)` en `graficas.py`.
- Las funciones de `graficas.py` reciben otras funciones implícitamente via `map`/comprensiones.

**Unidad III — Generadores (yap)**
- El proyecto no usa `yield` explícitamente, pero la lista de filas de C++ ya es una secuencia generada por el trabajador. Si se necesitara procesar meses sin cargar todo en memoria, se reemplazaría por un generador.

### 8.3 Competencias evaluadas

- **Competencia específica:** Modelado computacional — se modeló un problema real (amortización de préstamos) con el paradigma funcional y multi-lenguaje.
- **Competencias genéricas:**
  - *Comunicación:* `Apuntes.md`, `bitacora.md`, `Explicacion_*.md` documentan el proceso.
  - *Actualización:* se aprendió a migrar Flet → tkinter, usar `subprocess`, `matplotlib`, `ctypes`.
  - *Toma de decisiones:* Flet falló → cambio a tkinter; BD no → JSON; fuente global falló → reversión.
  - *Responsabilidad social:* el simulador ayuda a entender finanzas personales.
  - *Investigación:* se investigaron `matplotlib`, `tkinter`, `subprocess`, `ctypes`, PyInstaller.
  - *Creatividad:* diseño visual de Intresta, iconos, comparativas.

### 8.4 Niveles de dominio (autoevaluación)

- **Sobresaliente (9.5-10):** dominio de PF (funciones puras, inmutabilidad), patrón Orquestador-Trabajador, módulos, `subprocess`, JSON, `matplotlib`, `tkinter` con ttk, persistencia ligera.
- **Competente (8.0-9.4):** funciones como objetos, funciones de alto orden (`sum`, comprensiones), manejo de excepciones, pruebas en terminal.
- **Requiere práctica (6.0-7.9):** uso de decoradores, generadores con `yield`, pruebas unitarias con `assert`.

### 8.5 Evaluaciones

- **1.ª Parcial (01/10/2026 — Unidades I y II):** cubre estructura modular, funciones puras, módulos, organización, tipos y estructuras de datos, control de flujo. **El proyecto está listo para esta evaluación.**
- **2.ª Parcial (26/11/2026 — Unidad III):** cubre funciones de alto orden, decoradores, generadores. **El proyecto toca parcialmente alto orden (`sum`, comprensiones). Decoradores y generadores con `yield` quedarían como fase 2.**

---

*Explicación generada a partir de `Apuntes.md` y el plan de estudios `plan_materia (1).md`.*
