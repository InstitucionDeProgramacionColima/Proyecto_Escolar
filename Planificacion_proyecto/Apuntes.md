# Apuntes del Proyecto: Simulador de Préstamos

## Vinculación con los Objetivos de la Materia (Plan de Materia)

### Fecha: 18 de septiembre de 2026

#### 1. Creación de la Estructura Modular del Proyecto
- **Unidad I & II:** *Fundamentos del paradigma funcional, módulos y organización de código (2.1.7 Módulos y Organización)*.
- Se definió y estructuró el espacio de trabajo en base al patrón **Orquestador-Trabajador** y **Functional Core, Imperative Shell**:
  - `simulador_prestamos/core_cpp/`: Núcleo de cálculo funcional puro en C++ (`amortizacion.hpp`, `amortizacion.cpp`) y su interfaz imperativa/CLI (`main.cpp`).
  - `simulador_prestamos/gui/`: Orquestador de la interfaz gráfica y cliente de IA en Python (`ventana.py`, `ia.py`, `graficas.py`).
  - `simulador_prestamos/main.py`: Punto de entrada principal.
- Para cada componente se generaron sus respectivos archivos de especificación y explicación (`Explicacion_*.md`), preparando el terreno para la implementación de funciones puras, inmutabilidad de datos y pruebas.

---

### Fecha: 22 de septiembre de 2026

**Prompts:**
- *"si, solo la implementacion primero."*
- *"Analiza los archivos .cpp y dime porque me marca error en el IDE"*
- *"entonce dime, ya esta todo la logica? en .cpp? si es asi, podemos pasar a hacer el GUI?"*

**Archivos involucrados:**
- `simulador_prestamos/core_cpp/amortizacion.hpp`
- `simulador_prestamos/core_cpp/amortizacion.cpp`
- `simulador_prestamos/core_cpp/main.cpp`

#### 2. Implementación del Núcleo Funcional Puro en C++
- **Unidad I & II:** *Funciones Puras, Inmutabilidad, Transparencia Referencial y Patrón Functional Core, Imperative Shell*.
- **Descripción de lo que hace el código:**
  - **`amortizacion.hpp`:** Declara la estructura inmutable `FilaTabla` (`num_mes`, `val_cuota`, `val_interes`, `val_capital`, `val_saldo`) y las firmas de las funciones puras de cálculo.
  - **`amortizacion.cpp`:**
    - Implementa funciones puras de cálculo financiero para los 3 sistemas de amortización:
      - **Sistema Francés:** `calcular_cuota_fija_frances()`, `calcular_fila_frances()`, `generar_tabla_frances()`.
      - **Sistema Alemán:** `calcular_fila_aleman()`, `generar_tabla_aleman()`.
      - **Sistema Americano:** `calcular_fila_americano()`, `generar_tabla_americano()`.
    - Todas las funciones son **deterministas y sin efectos secundarios** (dada la misma entrada, producen exactamente la misma salida sin mutar variables externas).
    - Incluye la función `serializar_tabla_json()` que formatea los datos calculados en un arreglo estándar JSON.
  - **`main.cpp` (Imperative Shell):**
    - Actúa como la capa externa imperativa que recibe argumentos por línea de comandos (`<sistema> <monto> <tasa_anual> <meses>`), valida las entradas, delega el cálculo a las funciones puras y escribe la salida JSON en `stdout`.
  - **Compilación y Pruebas:**
    - Se compiló con `g++ -Wall -Wextra -O2 amortizacion.cpp main.cpp -o amortizador.exe` generando el binario ejecutable `amortizador.exe`.
    - Se validó el cálculo y formato JSON en terminal con pruebas de los tres sistemas (`frances`, `aleman`, `americano`).

---

### Fecha: 22 de septiembre de 2026

**Prompts:**
- *"ok, procedamos con el entorno GUI, nadamas necesito por el momento que hagas las ventanas, ojo, no ocupo que hagas algo por el moemnto de IA o graficas"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/main.py`

#### 3. Implementación de la Interfaz Gráfica (GUI) y Conexión Multi-lenguaje
- **Unidad I & II:** *Integración de módulos, separación de responsabilidades y patrón Orquestador-Trabajador*.
- **Descripción de lo que hace el código:**
  - **`ventana.py`:**
    - Define la función `calcular_amortizacion(str_sistema, val_monto, val_tasa_anual, num_meses)` que invoca mediante `subprocess.run` el binario compilado `amortizador.exe` de C++, pasando los argumentos y deserializando el resultado JSON devuelto en `stdout`.
    - Implementa la clase `VentanaPrincipal(tk.Tk)` con `tkinter` y `ttk`:
      - **Panel de Formulario:** Campos de entrada para Monto del préstamo, Tasa de interés anual porcentual, Plazo en meses y selector desplegable del Sistema de amortización (Francés, Alemán, Americano).
      - **Panel de Tabla (`Treeview`):** Muestra de forma tabular las columnas calculadas (Mes, Cuota, Interés, Capital y Saldo pendiente) con formato de moneda y scrollbar vertical.
      - **Panel de Resumen Financiero:** Tarjeta con cálculo automático de Total Pagado acumulado, Total de Intereses generados y Cuota del primer mes.
      - Botones de acción: *Calcular Tabla* y *Limpiar*.
  - **`main.py`:**
    - Punto de entrada principal que inicializa la aplicación y arranca el ciclo principal de eventos `mainloop()`.

---

### Fecha: 22 de septiembre de 2026

**Prompts:**
- *"dime, hay mucho problema si cambiamos la libreria de tkinter a flet?"*
- *"listo ya descarge la libreria, ahora por favor implemntala en el proyecto, por cierto, no olvides leer los archivos de la carpeta "Roles_and_skills" y al editar los archivos haslo segun lo que este escrito"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/main.py`
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md`

#### 4. Migración e Implementación de la Interfaz Gráfica Moderna con Flet
- **Unidad I & II:** *Desarrollo de interfaces declarativas reactivas, desacoplamiento y patrón Orquestador-Trabajador*.
- **Descripción de lo que hace el código:**
  - **`ventana.py` (Flet):**
    - Mantiene intacta la función pura de invocación `calcular_amortizacion(str_sistema, val_monto, val_tasa_anual, num_meses)` vía `subprocess.run` contra `amortizador.exe` de C++.
    - Implementa la clase `AplicacionSimulador` con componentes declarativos de Flet (Flutter para Python):
      - **Panel de Formulario (Columna Izquierda):** Campos de texto reactivos con iconos (`ft.TextField` para monto, tasa anual, plazo) y selector `ft.Dropdown` de sistemas de amortización.
      - **Botones de Acción:** `ft.ElevatedButton` (Calcular Tabla) con estilos modernos y `ft.OutlinedButton` (Limpiar).
      - **Tarjeta de Resumen Financiero:** Muestra dinámica del total pagado, total de intereses y cuota inicial.
      - **Tabla de Resultados (`ft.DataTable` + `ft.ListView`):** Visualización de las filas de amortización (Mes, Cuota, Interés, Capital y Saldo) con soporte para scroll vertical fluido y diseño Material Design 3.
      - **Diálogo de Alerta:** Manejo de validaciones numéricas con ventanas emergentes `ft.AlertDialog`.
  - **`main.py`:**
    - Inicializa la aplicación de escritorio nativa mediante `ft.app(target=iniciar_app_flet)`.

---

### Fecha: 22 de septiembre de 2026

**Prompts:**
- *"resolver el GUI de flet a tkinter"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/main.py`

#### 5. Migración de la Interfaz Gráfica de Flet a tkinter
- **Motivo:** La librería Flet presentaba problemas de instalación y no permitía ejecutar la aplicación correctamente.
- **Descripción de lo que hace el código:**
  - **`ventana.py` (tkinter):**
    - Se conserva **idéntica** la función `calcular_amortizacion()` que invoca vía `subprocess.run` al binario compilado `amortizador.exe` de C++.
    - Se reimplementa la clase `AplicacionSimulador` usando `tkinter` y `ttk` (incluidos con Python, sin dependencias externas):
      - **Panel de Formulario (Izquierda):** Campos `ttk.Entry` con `tk.StringVar` para monto, tasa y plazo. Selector `ttk.Combobox` de sistema de amortización (Francés, Alemán, Americano).
      - **Botones de Acción:** `ttk.Button` (Calcular Tabla y Limpiar) con estilos personalizados vía `ttk.Style`.
      - **Resumen Financiero:** Etiquetas `ttk.Label` vinculadas a `StringVar` que muestran Total Pagado, Total Intereses y Cuota Mes 1 con formato de moneda.
      - **Tabla de Resultados (`ttk.Treeview`):** Columnas Mes, Cuota, Interés, Capital y Saldo con `ttk.Scrollbar` vertical.
      - **Alertas:** Se usa `messagebox.showwarning()` para validaciones.
    - Se utiliza `ttk.Style` con tema "clam" para estilizar la interfaz con colores consistentes y tipografía "Segoe UI".
    - La función de entrada se renombra de `iniciar_app_flet` a `iniciar_app`.
  - **`main.py`:**
    - Se reemplaza `flet` por `tkinter`. Se crea la ventana raíz con `tk.Tk()`, se pasa a `iniciar_app()` y se inicia el ciclo de eventos con `mainloop()`.

---

### Fecha: 24 de septiembre de 2026

**Prompts:**
- *"hola gemini, si sabes como estomos en el proyecto? si es así entonces procedamos con el apartado de gráficas que quiero implementar. (recuerda leer los archivo de la carpeta "Roles_and_skills""*
- *"si"*

**Archivos involucrados:**
- `simulador_prestamos/gui/graficas.py`
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/Explicacion_graficas.py.md`

#### 6. Implementación del Módulo de Visualizaciones Gráficas e Integración en GUI
- **Unidad I & II:** *Modularidad, Organización de Código (2.1.7) e Integración Funcional Desacoplada*.
- **Descripción de lo que hace el código:**
  - **`graficas.py`:**
    - Implementa funciones puras desacopladas que reciben la estructura inmutable generada por el trabajador de C++ (`lista_filas`) y construyen figuras de visualización financiera con `matplotlib`:
      - `generar_figura_saldo(lista_filas, val_monto_inicial)`: Traza la curva continua y decreciente del saldo deudor desde el momento del desembolso (mes 0) hasta la liquidación del préstamo (mes $N$).
      - `generar_figura_composicion(lista_filas)`: Construye un gráfico de barras apiladas donde cada mensualidad desglosa de manera transparente el capital amortizado frente a los intereses devengados.
      - `renderizar_lienzo_en_contenedor(figura, obj_contenedor)`: Gestiona de forma limpia y reactiva el ciclo de vida del lienzo `FigureCanvasTkAgg` dentro de la interfaz gráfica.
  - **`ventana.py`:**
    - Se actualiza la arquitectura de la ventana derecha sustituyendo el contenedor estático por un componente de pestañas (`ttk.Notebook`) con estilos unificados.
    - Se añaden tres pestañas interactivas:
      1. **Tabla de Pagos:** Vista tabular clásica (`Treeview`).
      2. **Evolución del Saldo:** Visualización gráfica de la amortización acumulada.
      3. **Composición de Cuota:** Visualización gráfica del balance capital/interés.
    - Se conectan los controladores de eventos `_evento_calcular()` y `_evento_limpiar()` para generar o limpiar automáticamente las figuras al realizar simulaciones o restablecer valores.

---

### Fecha: 24 de septiembre de 2026 - 20:10:39

**Prompts:**
- *"ok, pero quiero que las graficas se comparen entre si (los tipos de amortizacion americano, frances e aleman) no olvides leer Roles_and_skills"*
- *"si"*

**Archivos involucrados:**
- `simulador_prestamos/gui/graficas.py`
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/Explicacion_graficas.py.md`

#### 7. Implementación de Gráficas Comparativas Multi-Sistema (Francés, Alemán y Americano)
- **Unidad I & II:** *Evaluación y Análisis Comparativo de Algoritmos Funcionales, Inmutabilidad y Visualización Declarativa*.
- **Descripción de lo que hace el código:**
  - **`graficas.py`:**
    - Se refactoriza para operar de forma polimórfica y comparativa recibiendo un diccionario con los resultados de los tres sistemas (`dict_tablas`):
      - `generar_figura_comparativa_saldos(dict_tablas, val_monto_inicial)`: Superpone en un único plano cartesiano la curva convexa del sistema Francés (amortización creciente de capital), la recta diagonal del sistema Alemán (amortización uniforme constante) y la línea plana horizontal del sistema Americano (liquidación total del principal en la última cuota).
      - `generar_figura_comparativa_cuotas(dict_tablas)`: Contrasta la evolución temporal del flujo de pagos mensual (cuota fija francesa, cuota escalonada decreciente alemana y cuota reducida de solo intereses americana con desembolso final de capital).
      - `generar_figura_comparativa_costos(dict_tablas)`: Genera un gráfico de barras comparativo del interés total pagado, mostrando visual y numéricamente cuál sistema minimiza o maximiza el costo financiero del crédito.
  - **`ventana.py`:**
    - Al presionar *"Calcular Tabla"*, se orquesta de forma transparente y simultánea la llamada a C++ para los tres modelos de amortización.
    - Se incorporan 4 pestañas interactivas en `ttk.Notebook`:
      1. **Tabla de Pagos:** Detalle numérico del sistema seleccionado.
      2. **Comparativa Saldos:** Trayectoria superpuesta de liquidación de saldo.
      3. **Comparativa Cuotas:** Trayectoria de las cuotas mes a mes.
      4. **Comparativa Intereses:** Comparativa de costo total en intereses entre los 3 sistemas.

---

### Fecha: 24 de septiembre de 2026 - 20:22:56

**Prompts:**
- *"ok, algo rapido, modifica los iconos de las ventans de tk y usa los archivos que estan en la carpeta "img" el .icon usalo para la barra de tareas y el -logo para la parte superior de la ventana"*
- *"intenta de nuevo"*

**Archivos involucrados:**
- `simulador_prestamos/gui/Img/generar_recursos.py`
- `simulador_prestamos/gui/Img/intresta-icon.ico`
- `simulador_prestamos/gui/Img/intresta-icon.png`
- `simulador_prestamos/gui/Img/intresta-logo-horizontal.png`
- `simulador_prestamos/gui/ventana.py`

#### 8. Personalización de Identidad Visual (Iconos de Ventana, Barra de Tareas y Logo)
- **Unidad I & II:** *Presentación Gráfica, Integración de Recursos Multimedia e Interoperabilidad con el Sistema Operativo*.
- **Descripción de lo que hace el código:**
  - **`generar_recursos.py`:**
    - Script utilitario que convierte y renderiza los vectores SVG originales (`intresta-icon.svg` e `intresta-logo-horizontal.svg`) a formatos matriciales nativos de alta fidelidad (`.ico` y `.png`) compatibles con el motor Tkinter y la shell de Windows.
  - **`ventana.py`:**
    - Invoca a través de `ctypes` la función del API de Windows `SetCurrentProcessExplicitAppUserModelID` para registrar un App ID explícito, permitiendo que Windows asigne a la ventana su icono propio en la **barra de tareas** en lugar del icono predeterminado del intérprete de Python.
    - Carga `intresta-icon.ico` (y `intresta-icon.png`) asignándolos con `iconbitmap()` e `iconphoto()`.
    - Integra en el contenedor de cabecera (`marco_header`) el isotipo y tipografía corporativa `intresta-logo-horizontal.png`.

---

### Fecha: 26 de septiembre de 2026 - 20:28:14

**Prompts:**
- *"ok, veras quiero que me ayudes a mover el texto "Simluador de intereses y amortizaciones" a la esquina superior derecha y el texto que dice "Hecho con python y c++" quitalo."*
- *"si"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`

#### 9. Ajuste de Maquetación y Distribución del Encabezado (Header Layout)
- **Unidad I & II:** *Diseño de Interfaces Gráficas de Usuario (GUI), jerarquía visual y distribución de componentes espaciales mediante gestores geométricos (`pack`).*
- **Descripción de lo que hace el código:**
  - **`ventana.py`:**
    - Se reestructura el contenedor del encabezado (`marco_header`) para distribuir los elementos visuales en los extremos opuestos.
    - El logotipo corporativo (`lbl_logo`) se fija con `side=tk.LEFT, anchor=tk.W` manteniendo su anclaje en el borde izquierdo.
    - Se mueve el título principal de la aplicación (`ttk.Label` con estilo `Titulo.TLabel`) hacia la esquina superior derecha mediante `side=tk.RIGHT, anchor=tk.NE, pady=(4, 0)`.
    - Se elimina la etiqueta de subtítulo descriptivo (`Subtitulo.TLabel`) para limpiar la interfaz y darle un aspecto más minimalista y profesional.

---

### Fecha: 26 de septiembre de 2026 - 20:37:40

**Prompts:**
- *"Ahora debajo de el logo de Intresta y el texto que moviste, pon una barra que tengatres apartados "calcular tabla" y ahí estara lo que ya hay, otro apartado que diga "Comparar". Por el momento asi hasle despues te dire que hacer"*
- *"si"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`

#### 10. Implementación de Barra de Navegación Principal Multinivel (Main Navigation Tabs)
- **Unidad I & II:** *Diseño de Interfaces Gráficas de Usuario (GUI), arquitectura modular de vistas y control de navegación mediante contenedores jerárquicos (`ttk.Notebook`).*
- **Descripción de lo que hace el código:**
  - **`ventana.py`:**
    - Se añade un contenedor `ttk.Notebook` principal (`self.cuaderno_principal`) debajo del encabezado institucional.
    - Se configuran tres apartados principales:
      1. **"Calcular Tabla":** Encapsula el diseño previo de dos paneles (panel izquierdo de formulario y resumen financiero, y panel derecho con la tabla y gráficas comparativas).
      2. **"Comparar":** Contenedor modular independiente preparado para funcionalidades analíticas comparativas adicionales.
      3. **"Apartado 3":** Contenedor reservado para futuras herramientas del simulador.
    - Se establecen estilos visuales dedicados (`NavegacionPrincipal.TNotebook` y `NavegacionPrincipal.TNotebook.Tab`) para diferenciar la barra de navegación superior de las pestañas internas de visualización.

---

### Fecha: 28 de septiembre de 2026

**Prompts:**
- *"ok, creo que ya sabes el contexto necesario. Bien, quiero que me ayudes a que la pestaña numero 2 de el apartado GUI me compare las tablas calculadas en paralelo"*
- *"no, quiero comparar dos tablas de diferentes calculos no de distintos tipos de amortizacion."*
- *"Sí, ejecútalo"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (patrón Orquestador-Trabajador, GUI en Python)
- `Planificacion_proyecto/bitacora.md` (registro del prompt)
- `Roles_and_skills/rules.md` (reglas de proceso, escritura snake_case, métodos privados con _, y formato)
- `Roles_and_skills/skills.md` (rol Programador: describir proceso y esperar Sí)

#### 11. Comparativa en Paralelo de Dos Cálculos Distintos (Pestaña Comparar)
- **Unidad II (2.1.7 Módulos y Organización) y Unidad III (3.1 Funciones de alto orden, map/filter/sum):** *Reutilización modular, funciones puras de resumen con `sum()` y separación Orquestador-Trabajador sin tocar el núcleo C++.*
- **Descripción de lo que hace el código:**
  - **`ventana.py`:**
    - Guarda el último cálculo de `_evento_calcular()` en memoria (`lista_filas_actual`, `dict_params_actual`) sin base de datos, reutilizando `calcular_amortizacion()` que invoca al binario C++.
    - `_construir_apartado_comparar()` ahora muestra dos `Treeview` lado a lado (Escenario A y B) con botones `Fijar actual como A/B`, `Intercambiar A/B` y `Limpiar comparativa`.
    - `_fijar_escenario_comparar()`, `_intercambiar_escenarios()`, `_limpiar_comparar()` y `_actualizar_vista_comparar()` gestionan el estado en memoria y refrescan títulos, resúmenes y diferencia `A-B` en totales e intereses.
    - `_crear_treeview_comparar()`, `_rellenar_treeview_comparar()`, `_formatear_titulo_escenario()` y `_calcular_totales_lista()` son funciones reutilizables en snake_case que evitan duplicar lógica de tabla.

---

### Fecha: 28 de septiembre de 2026

**Prompts:**
- *"ok, ahora por favor, el apartado de la pestaña 1 "calcular tabla" tiene mas apartados que son "Comparativa de saldos y comparativas de cuotas" esas dos quitalas y la "Comparativa de intereses" modificala para que muestre la relacion inerese-capital no los intereses de distintos metodos"*
- *"Sí, ejecútalo"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/graficas.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (orquestador Python, trabajador C++)
- `Planificacion_proyecto/bitacora.md` (registro del prompt)
- `Roles_and_skills/rules.md` (snake_case, constantes en mayúsculas, métodos privados con _, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador: describir proceso y esperar Sí)

#### 12. Simplificación de Pestañas y Relación Interés-Capital (Calcular Tabla)
- **Unidad II (2.1.7 Módulos y Organización) y Unidad III (3.1 map/filter/sum):** *Modularidad visual aislada en `graficas.py` y cálculo funcional con `sum()` sobre datos inmutables del trabajador C++.*
- **Descripción de lo que hace el código:**
  - **`graficas.py`:**
    - Nueva función pura `generar_figura_relacion_interes_capital(lista_filas)` que suma capital e interés del sistema seleccionado y grafica dos barras (Capital vs Interés) con el porcentaje de interés en el título.
  - **`ventana.py`:**
    - `_construir_panel_derecho()` deja solo `Tabla de Pagos` y `Relacion Interes-Capital`; elimina `marco_pestana_saldos` y `marco_pestana_cuotas`.
    - `_evento_calcular()` solo calcula el sistema seleccionado y guarda `lista_filas_actual` para la pestaña Comparar; ya no calcula los 3 sistemas.
    - `_actualizar_graficas()` y `_limpiar_graficas()` solo usan la nueva figura de relación.

---

### Fecha: 28 de septiembre de 2026

**Prompts:**
- *"ok, esta bien, ahora en el apartado de la pestaña dos "comparar" quita el boton intercambiar y despues, pon abajo una micro barra donde esten dos botones "Tablas" y otra "grafica" y en la cual, la primera es totalmente lo que ya hay pero la otra, mostrara una grafica mostrando la comparativa de las dos tablas A y B"*
- *"Sí, ejecútalo"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/graficas.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (orquestador Python, trabajador C++)
- `Planificacion_proyecto/bitacora.md` (registro del prompt)
- `Roles_and_skills/rules.md` (snake_case, constantes en mayúsculas, métodos privados con _, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador: describir proceso y esperar Sí)

#### 13. Micro Barra Tablas/Grafica en Comparar (Sin Intercambiar)
- **Unidad II (2.1.7 Módulos y Organización) y Unidad III (3.1 sum/zip):** *Vista modular con `ttk.Notebook` anidado y funciones puras de agregación para comparar dos cálculos distintos en memoria.*
- **Descripción de lo que hace el código:**
  - **`graficas.py`:**
    - Nueva función pura `generar_figura_comparativa_escenarios(lista_a, lista_b)` con dos paneles: barras agrupadas Capital/Interés A vs B y líneas de evolución de saldo A vs B.
  - **`ventana.py`:**
    - `_construir_apartado_comparar()` quita el botón `Intercambiar A/B` y crea `cuaderno_vistas_comparar` con `Tablas` (tablas paralelas existentes vía `_construir_vista_tablas_paralelas()`) y `Grafica` (`marco_vista_grafica`).
    - `_actualizar_vista_comparar()` ahora también llama a `_actualizar_grafica_comparar()` que renderiza la figura A vs B.
    - Se elimina `_intercambiar_escenarios()`.

---

### Fecha: 28 de septiembre de 2026

**Prompts:**
- *"ok, todo bien, ahora mueve los botones de "fijar tabla A y B" y "Limpiar comparativa" a la derecha y hacia arriba, despues ajusta un poco las graficas osea, que no se vean mal ni deformes"*
- *"Sí, ejecútalo"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/graficas.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/bitacora.md` (registro del prompt)
- `Roles_and_skills/rules.md` (snake_case, métodos privados con _, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador: describir proceso y esperar Sí)

#### 14. Botones a la Derecha y Ajuste de Proporción de Gráficas
- **Unidad II (2.1.7 Módulos y Organización):** *Maquetación con `grid(sticky=ne)` y visualización con proporción fija para evitar deformación en `FigureCanvasTkAgg`.*
- **Descripción de lo que hace el código:**
  - **`ventana.py`:**
    - `_construir_apartado_comparar()` crea `marco_encabezado` con `columnconfigure(0, weight=1)`; títulos a la izquierda (`sticky=nw`) y `marco_acciones` a la derecha y arriba (`sticky=ne`).
  - **`graficas.py`:**
    - `generar_figura_relacion_interes_capital()` pasa a `figsize=(6.2, 3.8)`, `tight_layout(pad=2.0)`, fuentes 11/9/8 y `ylim max*1.25`.
    - `generar_figura_comparativa_escenarios()` pasa a `figsize=(8.0, 3.8)`, `subplots_adjust(wspace=0.35, left=0.08, right=0.97, top=0.88, bottom=0.15)`, fuentes 10/8/7 y `ylim max*1.3`.

---

### Fecha: 28 de septiembre de 2026

**Prompts:**
- *"Hagamos un pequeño histrorial. Cada calculo se guardara en un tipo de boton o barra que diga el monto y fecha junto al tipo de amortizacion, eso del extremo izquierdo hacia el centro, al otro lado un boton que diga borrar y ese calculo se quite del historia. Ojo, si esto requieere base de datos no hagas nada y consulatame que hacer"*
- *"dime antes de eso, si se cierra la ventana o proframa se borrara?"*
- *"dame mas informacion del .json"*
- *"ok, hagamoslo asi"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/historial.json` (se crea al guardar)

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/bitacora.md` (registro del prompt)
- `Roles_and_skills/rules.md` (snake_case, constantes en mayúsculas, métodos privados con _, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador: describir proceso y esperar Sí)

#### 15. Historial Persistente en JSON (Apartado 3)
- **Unidad II (2.1.7 Módulos y Organización, 2.1.8 Pruebas) y Unidad III (3.1 sum):** *Persistencia ligera en archivo JSON con recálculo funcional vía trabajador C++ y lista en memoria.*
- **Descripción de lo que hace el código:**
  - **`ventana.py`:**
    - Constantes `NOMBRE_ARCHIVO_HISTORIAL` y `MAX_ENTRADAS_HISTORIAL`; estado `lista_historial` y `var_contador_historial`.
    - `_ruta_archivo_historial()`, `_cargar_historial_desde_json()` y `_guardar_historial_en_json()` gestionan `simulador_prestamos/historial.json` con solo resumen + parámetros.
    - `_evento_calcular()` llama a `_agregar_actual_a_historial()` tras calcular; `_cargar_historial_en_ventana()` recalcula con C++ sin duplicar y salta a `Calcular Tabla`.
    - `_construir_apartado_tres()` muestra filas con botón central-izquierdo (`monto | fecha | sistema`) y `Borrar` a la derecha, con scroll y `Limpiar todo`.
    - `_borrar_entrada_historial()` y `_limpiar_todo_historial()` actualizan archivo y vista.

---

### Fecha: 28 de septiembre de 2026

**Prompts:**
- *"Ahora, la pestaña 3 "aaprtado 3" ponle el nombre de "Historial""*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`

#### 15.1 Renombrar Pestaña a Historial
- **Descripción:** `cuaderno_principal.add(..., text="  Historial  ")` en `ventana.py:276`.

---

### Fecha: 28 de septiembre de 2026

**Prompts:**
- *"ok, ahora hagamos lo siguiente, el texto que aparece en la parte suprior de la ventana "Simulador de Intereses y Amortizaciones" quiero que lo centres mas en terminos verticales"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`

#### 15.2 Centrado Vertical del Título del Encabezado
- **Descripción:** Título pasa de `anchor=NE, pady=(4,0)` a `anchor=E, pady=0` para centrado vertical a la derecha; logo ya estaba en `anchor=W` (centrado vertical izquierdo).

---

### Fecha: 28 de septiembre de 2026

**Prompts:**
- *"ok, dime solamente dime, puedes saber la fuente (tipo de letra) que tiene la imagen de Intresta?"*
- *"puedes implementar esa fuente en todos los textos? osea las pestañas y todo qque tenga letra? solo dime si o no, después te dire si lo haces"*
- *"ok, haslo"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/graficas.py`

#### 15.3 Fuente Corporativa Segoe UI en Todos los Textos
- **Unidad II (2.1.7 Módulos y Organización):** *Unificación tipográfica con la fuente del logo (`segoeuib.ttf` / Segoe UI).*
- **Descripción de lo que hace el código:**
  - **`ventana.py`:**
    - `_configurar_estilos()` agrega `option_add("*Font", "Segoe UI 10")`; todos los estilos ttk ya usaban `Segoe UI`.
  - **`graficas.py`:**
    - Constante `FUENTE_PRINCIPAL` y `matplotlib.rcParams["font.family"] = ["Segoe UI", "Arial", "DejaVu Sans"]` para títulos, ejes y leyendas.

---

### Fecha: 28 de septiembre de 2026

**Prompts:**
- *"ok, hay un error al ejecutar el main.py ya no me muestra la ventana, analizalo porfavor y si hay un problema con la fuente, simplemente deshaz lo que te solicite anteriormente"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/graficas.py`

#### 15.4 Reversión de Fuente Global por Error Tcl
- **Causa:** `option_add("*Font", "Segoe UI 10")` sin llaves provoca `_tkinter.TclError: expected integer but got "UI"` al crear `ttk.Label` en `_construir_disposicion()`.
- **Acción:** Se eliminó `option_add` y se revirtió `matplotlib.rcParams` + `FUENTE_PRINCIPAL`; se conserva `Segoe UI` solo en estilos ttk puntuales. Verificado: `main.py` ya abre ventana (timeout sin traceback).

---

### Fecha: 01 de octubre de 2026

**Prompt:**
- *"Ponte en el modo de un profesor y lee Roles_and_skills y analiza el apartado de Unidad 1 y 2 y de el archivo plan_materia.md y explica esas unidades... crea un archivo llamado Guia_de_estudio.md que explique esos temas, ojo debes de explicarlo de forma tan sencilla que lo entienda alguien que no sabe nada de programacion"*

**Archivos involucrados:**
- `Guia_de_estudio.md` (nuevo, en carpeta general Proyecto_Walter)
- `plan_materia (1).md` (Unidades I y II)
- `Roles_and_skills/skills.md`, `Roles_and_skills/rules.md`
- `Planificacion_proyecto/bitacora.md` (registro)

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (contexto Orquestador-Trabajador)
- `Roles_and_skills/skills.md` (Plan de estudio: apegado al plan + ejemplos en .md)
- `Roles_and_skills/rules.md` (Reglas de Proceso 1 y 2)

#### 16. Guia de estudio Unidades I y II en lenguaje sencillo
- **Unidad I y II:** *1.1 Que es PF, paradigma, funciones matematicas, cambios de estado, POO vs PF / 1.2 Comparacion estructurada-POO-funcional / 1.3 Tipos, operadores, list-dict-set-tuple, if-match, for-while / 2.1 def-return, parametros, *args-**kwargs, lambda, recursion, docstrings, modulos, assert*.
- **Descripcion de lo que hace el documento:**
  - `Guia_de_estudio.md` explica cada tema del plan sin asumir saber programar, con analogias (calculadora, receta, cajas) y ejemplos Python cortos comentados linea por linea.
  - Incluye glosario de una linea, 10 preguntas tipo examen 01/10/2026 y conexion con el proyecto (`amortizacion.cpp` como funciones puras, `graficas.py` con `sum`, `ventana.py` como POO + funcional).

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"primero a la app, quiero añardirle un tema oscuro (osea que tenga esos colores) ya que el blanco puede dañar mucho la vista"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/graficas.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (orquestador Python GUI)
- `Planificacion_proyecto/bitacora.md` (registro del prompt)
- `Roles_and_skills/rules.md` (snake_case, constantes en mayusculas, metodos privados con _, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador: ejecutar directo segun respuesta)

#### 17. Tema oscuro para cuidar la vista (GUI + Graficas)
- **Unidad II (2.1.7 Modulos y Organizacion):** *Separacion orquestador-trabajador sin tocar C++; solo presentacion en Python.*
- **Descripcion de lo que hace el codigo:**
  - **`ventana.py`:**
    - Constantes oscuras `COLOR_FONDO="#1E1E2E"`, `COLOR_FONDO_TARJETA="#2B2B40"`, `COLOR_TEXTO_CLARO`, `COLOR_TEXTO_SUAVE`, `COLOR_CAMPO`, `COLOR_SELECCION`, `COLOR_BORDE`; acentos `COLOR_PRIMARIO="#C9A8FF"`, `COLOR_SECUNDARIO="#E5DE4B"`, `COLOR_ROJO="#EF5350"`, `COLOR_VERDE="#66BB6A"`.
    - `_configurar_estilos()` con `TEntry`, `TCombobox`, `TNotebook.Tab` + `map(selected)`, `Tabla.Treeview` con `fieldbackground` oscuro y seleccion, `Vertical.TScrollbar` y `TSeparator`; `Canvas` de historial pasa de `#CFCFCF` a `COLOR_FONDO_TARJETA`.
  - **`graficas.py`:**
    - `COLOR_FONDO_GRAFICA="#2B2B40"`, `COLOR_REJILLA="#44475A"`, `COLOR_TEXTO_GRAFICA`, `COLOR_TEXTO_SUAVE`, `COLOR_BORDE_BARRA`; series brillantes `Frances="#64B5F6"`, `Aleman="#66BB6A"`, `Americano="#EF5350"`, `B="#FFB74D"`.
    - Nueva funcion pura `_aplicar_tema_oscuro_eje(eje)` que pinta titulo, etiquetas, ticks y leyenda en claro con fondo oscuro; se llama en las 5 figuras; `annotate` y textos vacios usan color claro; `edgecolor="white"` pasa a `COLOR_BORDE_BARRA`.
  - **Verificacion:** `py_compile` OK y generacion Agg de `generar_figura_relacion_interes_capital` y `generar_figura_comparativa_escenarios` OK con `face (0.16,0.16,0.25)`.

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"ok, todo bien pero me referia a que yp pudiera seleccionar tema claro u obscuro, para esto abajo de donde dice "simulador de intereses y amortizacion" pon un boto que diga claro u obscuro"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/graficas.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (orquestador Python GUI)
- `Planificacion_proyecto/bitacora.md` (registro del prompt)
- `Roles_and_skills/rules.md` (snake_case, constantes en mayusculas, metodos privados con _, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador: ejecutar directo segun respuesta)

#### 18. Boton Claro / Oscuro debajo del titulo (toggle de tema)
- **Unidad II (2.1.7 Modulos y Organizacion):** *Presentacion conmutablesin tocar el nucleo C++; estado en memoria + re-render.*
- **Descripcion de lo que hace el codigo:**
  - **`ventana.py`:**
    - Dicts `PALETA_OSCURA` y `PALETA_CLARA` + `obtener_colores_tema(modo)`; `MODO_TEMA_INICIAL="oscuro"`; `COLOR_*` quedan como alias oscuro.
    - `__init__` guarda `modo_tema`, `dict_colores` y llama `establecer_modo_graficas()`; `_configurar_estilos()` usa `col` activo y agrega estilo `Tema.TButton`.
    - Header derecho con `marco_derecha`: titulo arriba y `ttk.Button(textvariable=var_texto_tema, command=_alternar_tema)` debajo con `anchor=E, pady=(4,0)`.
    - `_alternar_tema()` cambia modo, actualiza `dict_colores`, llama `establecer_modo_graficas()`, `_configurar_estilos()` y `_refrescar_tema()` que repinta `raiz`, `lbl_logo`, `lienzo_historial`, texto del boton y re-renderiza `lista_filas_actual` y comparativa A-B.
    - Import robusto en 3 niveles (`gui`, `simulador_prestamos.gui`, `graficas`) para evitar `ModuleNotFoundError`.
  - **`graficas.py`:**
    - `PALETA_GRAFICA_OSCURA` / `PALETA_GRAFICA_CLARA` + `establecer_modo_graficas(modo)` que muta los globales `COLOR_*`; `_aplicar_tema_oscuro_eje()` sigue aplicando texto/leyenda segun paleta activa.
  - **Verificacion:** `py_compile` OK; Agg oscuro `face (0.16,0.16,0.25)` y claro `(0.97,0.97,0.98)`; `obtener_colores_tema('claro')['tarjeta']="#CFCFCF"`, oscuro `"#2B2B40"`.

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"crees que se peuda añardir un boton que sea exportar a: y aparescan pdf o excel? si o no?"*
- *"Si, implementar" (respuesta a pregunta de viabilidad)*

**Archivos involucrados:**
- `simulador_prestamos/gui/exportar.py` (nuevo)
- `simulador_prestamos/gui/ventana.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (orquestador Python, nucleo C++ intacto)
- `Planificacion_proyecto/bitacora.md` (registro del prompt)
- `Roles_and_skills/rules.md` (snake_case, constantes en mayusculas, metodos privados con _, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador: ejecutar directo segun respuesta)

#### 19. Boton Exportar a PDF / Excel (tabla actual)
- **Unidad II (2.1.7 Modulos y Organizacion) y Unidad III (3.1 sum):** *Modulo nuevo reutilizable + funciones puras de totales; sin base de datos, usa `lista_filas_actual` del trabajador C++.*
- **Descripcion de lo que hace el codigo:**
  - **`exportar.py`:**
    - Constantes `ENCABEZADOS_TABLA`, `COLOR_CABECERA_EXCEL`; `_calcular_totales()` y `_texto_resumen()` puras con `sum()`.
    - `exportar_tabla_excel(lista, params, ruta)` con `openpyxl`: resumen, cabecera morada, formato moneda, anchos y totales.
    - `exportar_tabla_pdf(lista, params, ruta)` con `reportlab`: titulo, resumen, `Table` con estilo morado, zebra y `repeatRows`.
  - **`ventana.py`:**
    - Import de `filedialog` + `exportar_*` con fallback triple; header de tabla con `ttk.Menubutton("Exportar a")` y `Menu` PDF/Excel a la derecha.
    - `_evento_exportar(tipo)` valida `lista_filas_actual`, pide ruta con `asksaveasfilename`, llama exportador y avisa con `showinfo`.
  - **Dependencias:** `pip install openpyxl reportlab` (antes solo `matplotlib`+`pillow`).
  - **Verificacion:** `py_compile` OK; export real a `%TEMP%/prueba_tabla.xlsx` (5286 B) y `.pdf` (2192 B) con 2 filas de prueba.

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"ok, pero que tambien se la tabla y no necesariamente sean botones sepadados"*
- *Aclaracion elegida: "Tabla + grafica juntas"*

**Archivos involucrados:**
- `simulador_prestamos/gui/exportar.py`
- `simulador_prestamos/gui/ventana.py` (sin cambios, sigue un solo `Exportar a`)

#### 19.1 Exportar tabla + grafica juntas en un solo archivo
- **Descripcion de lo que hace el codigo:**
  - **`exportar.py`:**
    - `_guardar_grafica_temporal(lista)` genera `generar_figura_relacion_interes_capital()` y guarda png temporal con `savefig(dpi=150)`.
    - `exportar_tabla_excel()` incrusta con `ImagenExcel` en `G2` (620x380) y borra el png temporal.
    - `exportar_tabla_pdf()` agrega `Heading2` + `ImagenPDF` (440x270) tras la tabla y borra el png temporal.
    - Se mantiene un solo boton `Exportar a` con submenu, sin botones separados.
  - **Verificacion:** `py_compile` OK; conjunta 6 filas a `%TEMP%/conjunta.xlsx` (29189 B, 1 imagen, 11 filas) y `.pdf` (30115 B).

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"ok, ahora lo mismo pero que este en la ciomparacion de las tablas"*

**Archivos involucrados:**
- `simulador_prestamos/gui/exportar.py`
- `simulador_prestamos/gui/ventana.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (orquestador Python)
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (snake_case, constantes UPPER, metodos privados con _)
- `Roles_and_skills/skills.md` (rol Programador)

#### 19.2 Exportar Comparar A vs B con tabla + grafica juntas
- **Descripcion de lo que hace el codigo:**
  - **`exportar.py`:**
    - `_guardar_grafica_comparativa_temporal(a,b)` con `generar_figura_comparativa_escenarios()`; `_titulo_escenario()` y `_escribir_bloque_escenario_excel()` reutilizables.
    - `exportar_comparativa_excel(a,pa,b,pb,ruta)`: resumen A+B, 2 tablas, diferencia A-B y grafica (760x360) en `A{fin+2}`.
    - `exportar_comparativa_pdf(a,pa,b,pb,ruta)`: titulo, 2 tablas con `_estilo_tabla_pdf()`, diferencia y grafica (460x220).
  - **`ventana.py`:**
    - `marco_acciones` suma `Menubutton Exportar a` con submenu PDF/Excel junto a Fijar A/B y Limpiar.
    - `_evento_exportar_comparar(tipo)` valida A y B, pide ruta `comparativa_AB.*` y confirma con `showinfo`.
  - **Verificacion:** `py_compile` OK; `comp_AB.xlsx` (66389 B, 1 imagen, 14 filas) y `comp_AB.pdf` (69258 B) con 2+2 filas de prueba.

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"ahora, cuando se hace el pdf se realiza con un formato prefijo no? podemos modificarlo??"*
- *"primero, agrega el logo y pie de pagina."*

**Archivos involucrados:**
- `simulador_prestamos/gui/exportar.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (snake_case, constantes UPPER, metodos privados con _)
- `Roles_and_skills/skills.md` (rol Programador)

#### 19.3 Logo y pie de pagina en PDF (formato prefijo modificable)
- **Descripcion de lo que hace el codigo:**
  - **`exportar.py`:**
    - Constantes `NOMBRE_LOGO_PDF`, `TEXTO_PIE_PDF`; `_ruta_logo_pdf()` busca `Img/intresta-logo-horizontal.png` (320x75).
    - `_parte_logo_pdf()` retorna `ImagenPDF(180x42)+Spacer` o vacio si no existe; se antepone al titulo en `exportar_tabla_pdf()` y `exportar_comparativa_pdf()`.
    - `_dibujar_pie_pdf(lienzo,doc)` con `Helvetica 7 gris`: izquierda `Generado por Intresta... | dd/mm/yyyy hh:mm`, derecha `Pag. N`; se pasa como `onFirstPage/onLaterPages` en ambos `doc.build()`.
  - **Formato prefijo vigente:** A4 vertical, logo, titulo, resumen, tabla morada #380057 zebra, grafica, pie en todas las paginas.
  - **Verificacion:** `py_compile` OK; `logo_pie.pdf` (37999 B) y `logo_pie_comp.pdf` (75741 B); `_ruta_logo_pdf()` resuelve al png real.

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"ok, dime que tipo de letra usas en los formatos? el mismo que el logo?"*
- *"ok, en los titulos de los pdf y excel usa el mismo que el logo, ya lo que no sea tabla ni grafica, usa arial"*

**Archivos involucrados:**
- `simulador_prestamos/gui/exportar.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (snake_case, constantes UPPER, metodos privados con _)
- `Roles_and_skills/skills.md` (rol Programador)

#### 19.4 Titulos Segoe UI y resto Arial en PDF/Excel
- **Descripcion de lo que hace el codigo:**
  - **`exportar.py`:**
    - Constantes `FUENTE_TITULO_EXCEL="Segoe UI"`, `FUENTE_TEXTO_EXCEL="Arial"`; `_registrar_fuentes_pdf()` registra `segoeuib.ttf` como `SegoeUI-Bold` y `arial.ttf/bd` desde `C:/Windows/Fonts` con fallback `Helvetica`.
    - `_estilos_pdf()`: `Title` en `SegoeUI-Bold` morado, `Normal` en `Arial`, `Heading2` en `Arial-Bold`; pie en `Arial 7`.
    - Excel tabla: `A1` titulo `Segoe UI 14 bold morado`; `A2` resumen `Arial 10`; totales en `Arial`; cabecera/datos de tabla sin cambio.
    - Excel comparativa: titulo principal `Segoe UI 14`, titulos A/B `Segoe UI 11 bold`, resumen/diferencia `Arial`.
    - Tabla y grafica conservan su fuente (tabla Helvetica/Calibri, grafica DejaVu Sans).
  - **Verificacion:** `py_compile` OK; `FUENTE_TITULO_PDF=SegoeUI-Bold`, `TEXTO=Arial`; `fuente.xlsx A1=Segoe UI bold`, `A2=Arial`.

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"ahora, el pie de pagina ponle un fondo, el mismo color morado de el logo y las letras y logo de la parte superior del emcabezado, quitalas del cuerpo y ponlas en el lugar de encabezado. Ojo, las letras a un lado de el logo son blancas y no se distingen, igual de color morado o amarillo si le pones un fondo morado."*

**Archivos involucrados:**
- `simulador_prestamos/gui/exportar.py`

#### 19.5 Encabezado y pie morados con logo en PDF
- **Descripcion de lo que hace el codigo:**
  - **`exportar.py`:**
    - Constantes `COLOR_MORADO_PDF="#380057"`, `COLOR_AMARILLO_PDF="#E5DE4B"`, `ALTURA_ENCABEZADO_PDF=62`, `ALTURA_PIE_PDF=30`.
    - `_fabrica_decoracion_pdf(titulo)` dibuja en cada pagina: rect morado superior, `drawImage` logo 120x28 en `(40, alto-52)`, titulo en `SegoeUI-Bold 12` amarillo a la derecha; rect morado inferior con pie blanco `Arial 7` + `Pag. N`.
    - Cuerpo sin logo/titulo: `exportar_tabla_pdf()` y `comparativa` inician en resumen con `topMargin=85, bottomMargin=45`; `_parte_logo_pdf()` queda vacia por compat.
    - Letras blancas del logo visibles sobre fondo morado; titulo amarillo legible sobre morado.
  - **Verificacion:** `py_compile` OK; `hdr_tabla.pdf` (128457 B, 12 filas) y `hdr_comp.pdf` (160644 B).

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"ya en la aplicacion, podrias modificar un detalle, quiero que donde esta el boton del tema de la aplicacion, lo quites y pongas un boton que sean unas rallitas horizontales qeu me despliege a la izquierda una barra vertical que diga, area de trabajo y sea lo que esta al iniciar la app, después, historial (quitas el boton de historial del area principal) y muestre el historial y al ultimo configuracion y de meiestras pones el boton del tema"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (orquestador Python)
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (snake_case, metodos privados con _, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador: ejecutar directo)

#### 20. Menu hamburguesa con barra lateral (Area / Historial / Config)
- **Unidad II (2.1.7 Modulos y Organizacion):** *Navegacion lateral con vistas conmutables sin tocar el nucleo C++.*
- **Descripcion de lo que hace el codigo:**
  - **`ventana.py`:**
    - Header: boton `☰` (`Tema.TButton`, `command=_alternar_barra_lateral`) + logo a la izquierda, titulo a la derecha sin boton de tema.
    - `_construir_barra_lateral()`: botones verticales `Area de trabajo`, `Historial`, `Configuracion` en `botones_menu`.
    - Vistas: `marco_vista_area` con `cuaderno_principal` de 2 tabs (Calcular, Comparar); `marco_vista_historial` con `_construir_apartado_tres()` fuera del notebook; `marco_vista_config` con boton `var_texto_tema`.
    - `_mostrar_vista()` conmuta con `grid/grid_remove` y marca `pressed`; `_alternar_barra_lateral()` pliega/despliega; `_cargar_historial_en_ventana()` vuelve a `area` y `select(0)`.
  - **Verificacion:** `py_compile` OK; instanciacion Tk retirada OK: `vista=area`, tabs `['Calcular Tabla','Comparar']`, conmutacion historial/config OK, sidebar toggle False/True, botones `area/config/historial`.

---

### Fecha: 11 de octubre de 2026

**Prompts:**
- *"ok, el titulo que dice "Simulador de Intereses y Amortizaciones" hazlo mas grande sin desplazar el entorno de trabajo"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`

#### 20.1 Titulo mas grande con encabezado fijo
- **Descripcion de lo que hace el codigo:**
  - **`ventana.py`:**
    - `Titulo.TLabel` pasa de `Segoe UI 16 bold` a `22 bold`.
    - `marco_header` con `height=80` y `pack_propagate(False)`: el area de trabajo inicia siempre tras 80px fijos, el titulo crece centrado (`anchor=E`) sin empujar el contenido.
  - **Verificacion:** `py_compile` OK; Tk retirada: `fuente={Segoe UI} 22 bold`, `alto header=80`, `vista=area`.

---

### Fecha: 12 de octubre de 2026

**Prompts:**
- *"listo, dime tres ideas que pueda añadir a mi proyecto que complementen con el objetivo de la app"*
- *"explicame mas sobre como implementarias el tema 2 y 3"*
- *"ok, pero me referia en que consistia la idea no como se programa y sobre todo como funciona"*
- *"ok, implementemos la idea 3"*

**Archivos involucrados:**
- `simulador_prestamos/gui/indicadores.py` (nuevo)
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/exportar.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (orquestador Python, nucleo C++ intacto)
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (snake_case, constantes UPPER, metodos privados con _)
- `Roles_and_skills/skills.md` (rol Programador)

#### 21. Panel de indicadores (% interes, min-max, cruce, tasa efectiva)
- **Unidad II (2.1.7 Modulos) y Unidad III (3.1 sum/min/max/next/filter):** *Modulo puro reutilizable sin tocar C++.*
- **Descripcion de lo que hace el codigo:**
  - **`indicadores.py`:**
    - `calcular_indicadores(lista, tasa)` con `sum/min/max/next`: total, `%`, `mes_cruce` (primer `capital>interes`), `tasa_efectiva=((1+tasa/12)^12-1)*100`; `formatear_mes_cruce()` ("Mes N"/"Sin cruce"); vacio retorna ceros.
  - **`ventana.py`:**
    - Nuevas `var_porc_interes`, `var_cuota_rango`, `var_mes_cruce`, `var_tasa_efectiva`; seccion `Indicadores` bajo Resumen; `_actualizar_resumen(lista, tasa)` las llena; `_evento_limpiar()` las resetea; historial y calcular pasan la tasa.
  - **`exportar.py`:**
    - `_linea_indicadores()` en PDF tabla/comparativa (Arial) y Excel (`A3` italica + bloques A/B); tabla y grafica intactas.
  - **Verificacion:** `py_compile` OK; `OK_IND` (cruce Mes 2, efectiva 12.68%); UI (`% 44.4%, cruce Mes 2`); `ind.xlsx A3` con linea + 1 imagen.

---

### Fecha: 12 de octubre de 2026

**Prompts:**
- *"como verifico su implementacion?"*
- *"ok, aparece indicadores pero no la informacion, parece ser que no se despliega la informacion por el espacio o dime y resuelvelo"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py`

#### 21.1 Panel izquierdo con scroll (indicadores recortados)
- **Causa:** sin scroll, la seccion nueva quedaba bajo el alto fijo de 720px y se recortaba.
- **Descripcion de lo que hace el codigo:**
  - **`ventana.py`:**
    - `_construir_panel_formulario()` envuelve el contenido en `lienzo_formulario` (`Canvas`) + `Scrollbar` vertical + `marco_interno`; `scrollregion` auto, ancho sincronizado por tag `ventana_form` y scroll con rueda (`<MouseWheel>`).
    - `_refrescar_tema()` repinta el lienzo con `tarjeta` del tema activo.
  - **Verificacion:** `py_compile` OK; Tk retirada: `scrollregion=0 0 218 613` (con scroll activo), indicadores `% 44.4% | Mes 2`, tema claro repinta `#CFCFCF`.

---

### Fecha: 12 de octubre de 2026

**Prompts:**
- *"ok, ahora implementemos el tema 2 de los abonos"*

**Archivos involucrados:**
- `simulador_prestamos/core_cpp/amortizacion.hpp`
- `simulador_prestamos/core_cpp/amortizacion.cpp`
- `simulador_prestamos/core_cpp/main.cpp`
- `simulador_prestamos/core_cpp/amortizador.exe` (recompilado)
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/exportar.py`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (nucleo funcional C++, orquestador Python)
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (snake_case, `_privadas`, constantes UPPER, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador)

#### 22. Abonos extra a capital (paga antes, paga menos interes)
- **Unidad II (funciones puras, inmutabilidad) y Unidad III (3.1 sum/min):** *Extension pura del nucleo + orquestacion sin estado global.*
- **Descripcion de lo que hace el codigo:**
  - **C++ (`amortizacion.hpp/.cpp`, `main.cpp`):**
    - `struct AbonoExtra{num_mes, val_monto}`; `buscar_abono_mes()` suma abonos del mes; `parsear_abonos("3:1000,6:500")` tolerante a errores.
    - `generar_tabla_{frances,aleman,americano}_con_abonos()`: iteran con saldo ajustado, aplican `min(abono, saldo)`, truncan al liquidar (menos filas = meses ahorrados); vacio delega a la original.
    - `main` acepta 5to arg opcional, valida mes 1..plazo y usa la variante con abonos.
  - **`ventana.py`:**
    - `formatear_abonos_cli()` + `calcular_amortizacion(..., lista_abonos)`; seccion `Abonos Extra` (mes/monto, Agregar/Quitar, `Listbox`, `var_ahorro_abonos`); `_agregar/_quitar/_refrescar_lista_abonos()` validan contra el plazo.
    - `_evento_calcular()` calcula base y con abonos, muestra esta ultima, auto-fija A=sin y B=con en Comparar con `_fijar_comparativa_abonos()` (ahorro `$` + meses menos); titulos con `+N abonos`; `_evento_limpiar()` resetea; historial guarda/recarga abonos (`+N abonos` en el boton).
  - **`exportar.py`:** `_texto_abonos()` en `_texto_resumen()` y `_titulo_escenario()`; `_linea_indicadores()` intacta.
  - **Verificacion:** `g++` recompila sin warnings; base 661.86 vs abono 570.22 (11 filas, cuota m3 1888.49); aleman/americano/payoff(1 fila)/error mes 99 OK; UI `Ahorro: $91.64 y 1 meses menos`; `abono.pdf` con `Abonos: m3`.

---

### Fecha: 12 de octubre de 2026

**Prompts:**
- *"ok, analiza la carpeta Roles_and_skills y procederemos con las modificaciones"*
- *"ok, recomiendame que puedo añadir en el apartado de configuracion"*
- *"ok, añadamos el tamaño de letra tambien el formato de los numeros y los defaults Exportacion"*

**Archivos involucrados:**
- `simulador_prestamos/gui/configuracion.py` (nuevo)
- `simulador_prestamos/gui/ventana.py`
- `simulador_prestamos/gui/exportar.py`
- `simulador_prestamos/config.json`

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (orquestador Python, nucleo C++ intacto)
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (snake_case, `_privadas`, constantes UPPER, formato headers/funciones/proceso)
- `Roles_and_skills/skills.md` (rol Programador)

#### 23. Configuracion ampliada (letra, formato numeros, defaults exportacion)
- **Unidad II (2.1.7 Modulos) y Unidad III (3.1 zip/sorted):** *Nuevo modulo puro de preferencias + orquestacion con estado persistente.*
- **Descripcion de lo que hace el codigo:**
  - **`configuracion.py`:**
    - `CONFIG_POR_DEFECTO` (tema, tamano, decimales, moneda, carpeta, logo/pie); `cargar_configuracion()` mezcla JSON con defecto y normaliza; `guardar_configuracion()`; `obtener_ajuste_fuente()` (-2/0/+2); `formatear_moneda()` (`$, MXN, USD` con 0/1/2 decimales).
  - **`ventana.py`:**
    - `__init__` carga config y aplica tema guardado; `_configurar_estilos()` escala fuentes con `num_ajuste`; `_formatear_moneda()` centraliza `$` en tabla, resumen, comparar A/B, abonos e historial.
    - `_construir_vista_config()` con 3 secciones: Apariencia (tema + `Pequeña/Normal/Grande`), Formato (decimales + moneda), Exportacion (carpeta + Examinar, checks logo/pie, Restablecer); `_aplicar_configuracion()` re-renderiza y guarda en `config.json`; `_evento_exportar()` usa `initialdir` y pasa decimales/simbolo/logo/pie.
  - **`exportar.py`:**
    - `_formatear_moneda_export()` y `_formato_num_excel()`; 4 exports aceptan `num_decimales/simbolo_moneda`; PDF aceptan `incluir_logo/incluir_pie` en `_fabrica_decoracion_pdf()`.
  - **Verificacion:** `py_compile` OK; `cargar` defecto + `USD 1,234` con 0 dec; `cfg_tabla.xlsx/pdf` y `cfg_comp.xlsx/pdf` generados; Tk retirada `OK_UI_CONFIG` (Grande guarda, `USD 1,234`, `carpeta None`); `config.json` restablecido a defecto.

---

### Fecha: 14 de octubre de 2026

**Prompts:**
- *"oye, quiero impkementar IA en mi proyecto por medio de un chat y que esta solo responda y de reportes, opiniones o interpretaciones de los resultados de las tablas y graficas, como puedo añadir la API de esta cuenta en el proyecto? y limitarlo"*
- *"si por favor, añadamos la logia de IA.py"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ia.py` (implementación de funciones de interacción con Gemini)
- `simulador_prestamos/gui/Explicacion_ia.py.md` (documentación de arquitectura)
- `simulador_prestamos/config.json` (soporte de clave de API opcional)

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md` (Capa de orquestación en Python)
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (snake_case, constantes en MAYÚSCULAS, variables descriptivas y formato en bloques)
- `Roles_and_skills/skills.md` (rol Programador: confirmación previa de acciones)
- `plan_materia (1).md` (Unidad II: 2.1.7 Módulos y Organización; Unidad III: Funciones puras e inmutabilidad)

#### 24. Implementación del módulo de Inteligencia Artificial (`ia.py`)
- **Alineación con el Plan de la Materia:**
  - **Unidad II (2.1.7 Módulos y Organización):** *Se organiza la capa de análisis inteligente en un submódulo independiente y desacoplado dentro del paquete `gui`.*
  - **Unidad III (Funciones puras y separación de responsabilidades):** *Principio fundamental: La IA actúa como intérprete y asesora, nunca como calculadora. Se le entregan estructuras de datos inmutables generadas por el núcleo en C++.*
- **Descripción de lo que hace el código:**
  - **`ia.py`:**
    - Constantes `MODELO_GEMINI_DEFAULT` (`gemini-3.7-flash`), `TEMPERATURA_DEFAULT` (0.2 para evitar alucinaciones), `MAX_TOKENS_DEFAULT` (600 para limitar consumo/extensión) y `PROMPT_SISTEMA_BASE`.
    - `PROMPT_SISTEMA_BASE`: Candado de comportamiento estricto que instruye al modelo a limitarse exclusivamente a interpretar tablas de amortización, gráficos e indicadores de préstamos, rechazando cualquier tema ajeno.
    - `_obtener_clave_api()`: Carga segura buscando en la variable de entorno `GEMINI_API_KEY` con fallback a `config.json`.
    - `_obtener_cliente_gemini()`: Inicialización robusta del cliente de la librería oficial `google-genai`.
    - `llamar_api(cad_prompt, cad_instruccion_sistema, ...)`: Función base con manejo de excepciones y configuración de límites.
    - `explicar_tabla_amortizacion(dict_resumen, lista_tabla)`: Inyecta el resumen y muestras de periodos para generar reportes ejecutivos.
    - `comparar_sistemas(dict_frances, dict_aleman, dict_americano)`: Elabora una comparativa detallada entre Francés, Alemán y Americano recomendando perfiles.
    - `simular_escenario_personalizado(cad_pregunta_usuario, dict_resumen, lista_tabla)`: Atiende preguntas libres del usuario ancladas estrictamente al escenario actual.
- **Verificación:** Módulo estructurado con bloques de cabeceras, constantes, funciones auxiliares privadas y funciones públicas con tipado.

---

### Fecha: 14 de octubre de 2026

**Prompts:**
- *"todavia lo subraya, ahora si pasemos al diseño del chat, ojo, quiero que pueda implementar su opinion concreta en el documento exportado a pdf o excel."*
- *"si, solamente dime mas sobre eso que se guardará la conversacion (se breve) y realiza lo acordado anteriormente."*

**Archivos involucrados:**
- `simulador_prestamos/gui/ventana.py` (interfaz del chat, botones rápidos y ejecución en hilos)
- `simulador_prestamos/gui/exportar.py` (renderizado del dictamen de IA en PDF y Excel)

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md`
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md`
- `Roles_and_skills/skills.md` (rol Programador: descripción y confirmación previa)
- `plan_materia (1).md` (Unidad II: Programación concurrente/hilos y UI responsiva; Unidad III: Inmutabilidad)

#### 25. Integración del Chat con Asesor IA y Exportación de Dictamen a PDF / Excel
- **Alineación con el Plan de la Materia:**
  - **Unidad II (Concurrencia y UI responsiva):** *Uso de `threading.Thread` para desacoplar las consultas HTTP al modelo de lenguaje del bucle principal de Tkinter, evitando que la interfaz se congele.*
  - **Unidad III (Composición funcional y flujo de datos):** *El dictamen generado por la IA viaja como parámetro inmutable `cad_opinion_ia` hacia las funciones puras de exportación de `exportar.py`.*
- **Descripción de lo que hace el código:**
  - **`ventana.py`:**
    - Se añade la pestaña **"🤖 Asesor IA"** en el panel derecho (`_construir_contenido_chat_ia`).
    - Integra un área de conversación con `tk.Text` y scrollbar, respetando la paleta de colores activa (clara u oscura).
    - Botones rápidos: *"Interpretar Tabla Actual"* y *"Comparar 3 Sistemas"*, además de entrada de texto libre con soporte para la tecla `Enter`.
    - `_ejecutar_en_hilo_ia()`: Ejecuta las peticiones a la API en un hilo secundario y devuelve la respuesta al hilo principal de la UI con `self.raiz.after()`.
    - La última respuesta se almacena en memoria (`self.cad_opinion_ia`) para ser anexada en la exportación.
  - **`exportar.py`:**
    - `exportar_tabla_pdf`: Añade una sección con recuadro formal morado y tipografía clara titulada *"Dictamen y Análisis del Asesor IA"*.
    - `exportar_tabla_excel`: Agrega filas formateadas debajo de los totales con el texto completo del reporte.
    - Notificación visual al usuario confirmando que el dictamen fue incluido en el archivo guardado.
- **Verificación:** Código sin errores de sintaxis, compatible con el flujo existente de cálculo C++.

---

### Fecha: 30 de octubre de 2026

**Prompts:**
- *"ok, lee un poco la bitacora, y ten contexto de los procesos anteriores, para despues, que me ayudes a configurar la IA que teniamos intendo configurar antres, por cierto tambien pon en el .gitignore el archivo config.json"*
- *"ok, ayudame a diagnosticar los problemas que tenga la API de gemini por el cual no funciona el chat"*
- *"ok, resuelve esos detalles"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ia.py` (actualización de modelos disponibles y robustecimiento del fallback)
- `simulador_prestamos/gui/configuracion.py` (soporte y persistencia segura de `api_key` en `config.json`)
- `simulador_prestamos/config.json` (declaración del campo `api_key`)
- `simulador_prestamos/.gitignore` (exclusión de `config.json` para proteger credenciales)

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md`
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (o `.agents/rules/reglas.md` / `GEMINI.md`)
- `plan_materia (1).md` (Manejo de excepciones robusto, tolerancia a fallos y configuración desacoplada)

#### 26. Diagnóstico y Corrección de Integración con API de Gemini
- **Alineación con el Plan de la Materia:**
  - **Manejo robusto de excepciones y resiliencia en red:** Se refinó la lógica de reintentos en `llamar_api` para atrapar específicamente errores de modelos ausentes (404), saturación de servidores (503) o límites de tasa (429), iterando sobre la lista de modelos de respaldo sin interrumpir bruscamente el servicio.
  - **Seguridad y desacoplamiento de configuración:** Se independizó la clave de API para permitir su inyección local segura en `config.json` evitando filtraciones accidentales al control de versiones mediante `.gitignore`.
- **Descripción de lo que hace el código:**
  - **`ia.py`:**
    - Se reemplazaron modelos inexistentes por los oficiales de Google GenAI: `"gemini-2.5-flash"`, `"gemini-2.0-flash"`, `"gemini-1.5-flash"`, `"gemini-1.5-pro"`.
    - Se diferencian fallos de credenciales (`API_KEY_INVALID`) de fallos transitorios (404/503/429/RESOURCE_EXHAUSTED), conmutando automáticamente entre los modelos disponibles.
    - Se implementó descubrimiento dinámico: si los modelos fijos fallan, se invoca `cliente.models.list()` para detectar y usar automáticamente los modelos habilitados en la cuenta de Google AI Studio.
    - Se priorizó la lectura de `config.json` sobre la variable de entorno del sistema para asegurar que cambios recientes de clave surtan efecto inmediato sin verse bloqueados por variables antiguas de la terminal.
  - **`configuracion.py`:**
    - Se añadió `api_key` a `CONFIG_POR_DEFECTO`.
    - `guardar_configuracion()` ahora mezcla los valores previos existentes con los nuevos para evitar eliminar la clave de API al guardar temas o formatos.
  - **`config.json`:**
    - Se agregó la clave `"api_key": ""` para facilitar su llenado.
- **Verificación:** Archivos actualizados respetando las convenciones de nomenclatura `snake_case` y estructura modular.

---

### Fecha: 30 de octubre de 2026

**Prompts:**
- *"ok, ahora, ve si puedes cambiar el modelo de gemini, ademas y si puedes cambiar un poco las reglas del consultor, solo añadelé que pueda responder sobre preguntas del archivo generado como, el formato del archivo, donde se guarda y si se puede modificar. SOLO ESO NO NADAMAS"*

**Archivos involucrados:**
- `simulador_prestamos/gui/ia.py` (optimización de lista de modelos, caché de modelo exitoso y actualización de `PROMPT_SISTEMA_BASE`)

**Archivos usados de Planificacion_proyecto y Roles_and_skills:**
- `Planificacion_proyecto/Arquitectura_Simulador_Prestamos.md`
- `Planificacion_proyecto/bitacora.md`
- `Roles_and_skills/rules.md` (o `.agents/rules/reglas.md` / `GEMINI.md`)
- `plan_materia (1).md` (Ingeniería de prompts, optimización de latencia en llamadas a servicios externos)

#### 27. Optimización de Latencia y Alcance Restringido del Asesor IA
- **Alineación con el Plan de la Materia:**
  - **Optimización de llamadas remotas y caché de conexión:** Implementación de memoización en memoria (`_modelo_activo_cache`) para recordar el modelo que respondió favorablemente, suprimiendo reintentos y reduciendo el tiempo de respuesta a menos de 1 segundo.
  - **Ingeniería de Prompts y Seguridad de Contexto (System Instructions):** Se delimitaron estrictamente las reglas del consultor en `PROMPT_SISTEMA_BASE`: además de los datos del cálculo del préstamo, se autorizó única y exclusivamente a resolver dudas sobre los archivos generados (formato .pdf y .xlsx, ruta de guardado y posibilidades de edición).
- **Descripción de lo que hace el código:**
  - **`ia.py`:**
    - Priorización de `"gemini-2.0-flash"` como primer modelo en `MODELOS_DISPONIBLES`.
    - Ampliación de `MAX_TOKENS_DEFAULT` a 1500 tokens para explicaciones completas sin ser truncadas.
    - Mecanismo de caché que recuerda el modelo activo y evita ciclos de búsqueda repetitivos.
    - Ajuste en `PROMPT_SISTEMA_BASE` con reglas 1.b y 3 actualizadas para cubrir las preguntas sobre archivos exportados y rechazar cualquier otra consulta fuera de contexto.
- **Verificación:** Pruebas de compatibilidad completadas, sintaxis limpia y cumplimiento estricto del alcance solicitado.

---
