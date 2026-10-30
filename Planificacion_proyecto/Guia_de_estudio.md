# Guia de estudio - Programacion Funcional
## Unidades I y II - Explicado como si fuera tu primer dia

> Materia: PROGRAMACION FUNCIONAL - 3er semestre Grupo B
> 1a Evaluacion parcial: 01/10/2026 (Unidades I y II)
> Fuente: `plan_materia (1).md` + carpeta `Roles_and_skills`

Esta guia no asume que sabes programar. Si sabes usar una calculadora y una receta de cocina, ya puedes entender todo.

---

# PARTE 1 - UNIDAD I: Fundamentos del paradigma funcional

## 1.1 Que es la programacion funcional (1.1.1)

Imagina 2 aparatos:

* **Licuadora normal (programacion comun):** echas fruta, la licuadora CAMBIA lo que hay dentro. Si la abres a la mitad, ya no hay fruta, hay jugo. El estado cambio.
* **Calculadora magica (programacion funcional):** le das 2 + 3 y te devuelve 5, pero NO cambia el 2 ni el 3. Siempre que le des 2 + 3 te da 5. Nunca te sorprende.

**Programacion funcional = resolver todo con calculadoras magicas llamadas funciones puras.**

Una funcion pura tiene 2 reglas:
1. Mismo ingrediente, mismo resultado. Siempre.
2. No ensucia la cocina. No cambia nada fuera de ella.

Ejemplo en Python:

```python
# Funcion pura: siempre que le des 2 y 3, devuelve 5
def sumar(num_a, num_b):
    return num_a + num_b

print(sumar(2, 3))  # 5
print(sumar(2, 3))  # 5 otra vez, nunca cambia
```

Ejemplo de funcion NO pura (la evitamos en este paradigma):

```python
total = 0  # caja fuera de la funcion

def sumar_ensuciando(num):
    global total
    total = total + num  # cambia algo de afuera, ensucia
    return total
```

## 1.1 Que es un paradigma (1.1.2)

Paradigma = forma de pensar para resolver problemas. Como estilos de cocinar:

1. **Estructurada:** receta paso 1, paso 2, paso 3 en orden.
2. **Orientada a objetos (POO):** moldes para hacer galletas. Cada galleta (objeto) tiene sus datos y sabe hacer cosas.
3. **Funcional (PF):** puras matematicas. Conectas funciones como tuberias.

No hay uno malo, solo son estilos distintos.

## 1.1 Funciones matematicas (1.1.4)

En la escuela viste `f(x) = x * 2`.

* Si `x = 5`, el resultado es `10`. Siempre.
* No importa cuantas veces lo hagas, ni que dia sea.

Eso es lo que copiamos en programacion funcional. Predecible = menos errores.

```python
def duplicar(num):
    return num * 2
```

## 1.1 Cambios de estado (1.1.5)

Estado = como estan las cosas en este momento.

* Con estado que cambia: `saldo = 100`, luego `saldo = saldo - 20`, ahora vale 80. La caja cambio.
* Sin cambio (funcional): en vez de cambiar la caja, creas una caja nueva.

```python
# Estilo con cambio (comun, pero no funcional)
saldo = 100
saldo = saldo - 20  # la variable cambio

# Estilo funcional: no cambiamos, creamos nuevo valor
saldo_inicial = 100
saldo_nuevo = saldo_inicial - 20
# saldo_inicial sigue siendo 100, saldo_nuevo es 80
```

Por que nos importa? Porque cuando muchas partes cambian la misma caja, nadie sabe quien la rompio. Si nadie la cambia, es facil encontrar errores.

## 1.1 POO vs PF (1.1.6)

Piensa en un banco:

* **POO:** tienes un objeto `Cuenta` que guarda tu dinero dentro y tiene botones `cuenta.retirar()`. El dinero vive dentro del objeto y cambia.
* **PF:** tienes datos `saldo = 100` y una funcion `retirar(saldo, cantidad)` que te devuelve el nuevo saldo. Los datos viajan, no viven encerrados.

| POO | PF |
|---|---|
| Dato vive dentro del objeto | Dato viaja como argumento |
| `cuenta.retirar(20)` cambia la cuenta | `nuevo = retirar(100, 20)` crea un nuevo valor |
| El estado cambia con el tiempo | Se evita cambiar, se crean valores nuevos |

---

## 1.2 Los 3 paradigmas con el mismo ejemplo

Problema: tienes precios `[10, 20, 30]` y quieres sumarle IVA 16% a cada uno.

### 1.2.1 Estructurada: pasos en orden

```python
precios = [10, 20, 30]
resultado = []  # caja vacia

for precio in precios:  # paso 1: recorre uno por uno
    con_iva = precio * 1.16  # paso 2: calcula
    resultado.append(con_iva)  # paso 3: guarda

print(resultado)
```

Lees de arriba a abajo como receta.

### 1.2.2 Orientada a objetos: molde + objetos

```python
class CalculadoraIVA:  # el molde
    def __init__(self, tasa):
        self.tasa = tasa  # cada calculadora guarda su tasa

    def aplicar(self, precio):
        return precio * (1 + self.tasa)

mi_calc = CalculadoraIVA(0.16)  # creo un objeto
print(mi_calc.aplicar(10))
```

El dato `tasa` vive dentro del objeto.

### 1.2.3 Funcional: funciones puras conectadas

```python
def agregar_iva(precio):
    return precio * 1.16  # pura: mismo precio, mismo resultado

precios = [10, 20, 30]
resultado = list(map(agregar_iva, precios))

print(resultado)
```

No hay pasos que cambien cajas, solo transformas la lista en otra lista nueva. `map` lo veras a fondo en Unidad III, por ahora quedate con la idea: entra una lista, sale una lista nueva.

---

## 1.3 Python basico para poder hacer funcional

### 1.3.1 Estructura de un programa

Todo programa Python es:

```python
# 1. Arriba: traer herramientas (imports)
# 2. En medio: definir funciones
# 3. Abajo: usar esas funciones

def saludar(nombre):
    return "Hola " + nombre

print(saludar("Ana"))
```

### 1.3.2 Tipos de datos

Son los tipos de ingredientes.

**Numericos (1.3.2.1):**

```python
entero = 10          # int, sin punto decimal
decimal = 10.5       # float, con punto
complejo = 2 + 3j    # complejo, para mates avanzadas (casi no lo usaras)
cientifico = 1.5e3   # 1500.0, el e3 significa "por 1000"
```

**Logicos (1.3.2.2):**

```python
tengo_hambre = True   # solo puede ser True o False
es_de_noche = False
```

Es como un interruptor: prendido o apagado.

**Cadena string (1.3.2.3):**

```python
nombre = "Ana"
saludo = 'Hola'
```

Texto siempre entre comillas.

### 1.3.3 Operadores

**Aritmeticos (1.3.3.1):** para mates.

```python
print(10 + 3)   # 13 suma
print(10 - 3)   # 7 resta
print(10 * 3)   # 30 multiplicacion
print(10 / 3)   # 3.33 division normal
print(10 // 3)  # 3 division sin decimales
print(10 % 3)   # 1 residuo: cuanto sobra
print(2 ** 3)   # 8 potencia: 2x2x2
```

**Logicos (1.3.3.2):** para combinar preguntas de si/no.

```python
print(True and False)  # False, los dos deben ser True
print(True or False)   # True, con que uno sea True basta
print(not True)        # False, invierte
```

**Condicionales / comparacion (1.3.3.3):** preguntan y responden True/False.

```python
print(5 > 3)   # True
print(5 < 3)   # False
print(5 == 5)  # True, doble igual para comparar
print(5 != 3)  # True, diferente
```

**Ternario (1.3.3.3.1):** un `if` en una sola linea.

```python
edad = 20
mensaje = "mayor" if edad >= 18 else "menor"
print(mensaje)  # mayor
```

Se lee: "pon 'mayor' SI edad >= 18, SI NO pon 'menor'".

### 1.3.4 Estructuras de datos: las 4 cajas

**Lista `list` (1.3.4.1):** mochila donde cabe todo y puedes cambiar lo de dentro. Orden importa.

```python
frutas = ["manzana", "pera", "mango"]
print(frutas[0])  # manzana, se cuenta desde 0
frutas.append("uva")  # agrega al final
```

**Diccionario `dict` (1.3.4.2):** cajonera con etiquetas.

```python
alumno = {"nombre": "Luis", "edad": 20}
print(alumno["nombre"])  # Luis, lo buscas por etiqueta
```

**Conjunto `set` (1.3.4.3):** bolsa donde no hay repetidos y no hay orden.

```python
numeros = {1, 2, 2, 3}
print(numeros)  # {1, 2, 3}, el repetido desaparece
```

**Tupla `tuple` (1.3.4.4):** como lista pero sellada, no se puede cambiar. Ideal para funcional.

```python
punto = (10, 20)
# punto[0] = 99  # esto daria error, no se puede cambiar
```

Regla rapida: si no quieres que nadie lo cambie, usa tupla. Si necesitas orden y cambios, lista.

### 1.3.5 Condicionales: tomar decisiones

**if solo (1.3.5.1):**

```python
edad = 20
if edad >= 18:
    print("puedes entrar")
```

**if-else (1.3.5.2):** un camino u otro.

```python
edad = 15
if edad >= 18:
    print("puedes entrar")
else:
    print("no puedes entrar")
```

**if-elif-else (1.3.5.3):** varios caminos.

```python
calif = 85
if calif >= 90:
    print("excelente")
elif calif >= 70:
    print("aprobado")
else:
    print("reprobado")
```

**match-case (1.3.5.4):** el interruptor multiple moderno.

```python
sistema = "frances"
match sistema:
    case "frances":
        print("cuota fija")
    case "aleman":
        print("capital fijo")
    case "americano":
        print("solo intereses")
    case _:
        print("sistema desconocido")
```

El `_` es el "todos los demas".

### 1.3.6 Control de flujo: repetir sin copiar-pegar

**Iterables e iteradores (1.3.6.1):** iterable = algo que puedes recorrer uno por uno (lista, texto). Iterador = el dedo que apunta al siguiente.

```python
for letra in "hola":  # "hola" es iterable
    print(letra)
```

**for (1.3.6.2):** repite para cada elemento.

```python
for i in [1, 2, 3]:
    print(i)
```

**while (1.3.6.3):** repite mientras algo sea verdad. Cuidado: si nunca se vuelve falso, no para.

```python
contador = 0
while contador < 3:
    print(contador)
    contador = contador + 1
```

**range, break, continue (1.3.6.4):**

```python
for i in range(5):  # 0,1,2,3,4
    if i == 2:
        continue  # salta el 2, sigue con el 3
    if i == 4:
        break  # rompe el ciclo, ya no sigue
    print(i)
```

**Anidadas (1.3.6.5):** un ciclo dentro de otro, como tablas de multiplicar.

```python
for fila in [1, 2]:
    for col in ["a", "b"]:
        print(fila, col)
```

---

# PARTE 2 - UNIDAD II: Las funciones (el corazon funcional)

## 2.1.1 Que es una funcion y por que usarla

Funcion = mini-maquina con nombre. Le metes ingredientes, te devuelve un plato.

Ventajas: no repites codigo, es mas facil probar, es mas facil leer.

**Declaracion y llamada (2.1.1.3):**

```python
# Declarar = construir la maquina
def saludar(nombre):  # nombre es el parametro (el hueco)
    return "Hola " + nombre

# Llamar = usar la maquina
print(saludar("Ana"))   # "Ana" es el argumento (lo que pones en el hueco)
print(saludar("Luis"))
```

Parametro = el nombre del hueco en la receta. Argumento = lo que realmente pones al usarla.

## 2.1.2 return y None

**return (2.1.2.1):** lo que la funcion te entrega de vuelta.

```python
def sumar(a, b):
    return a + b  # entrega el resultado y termina

resultado = sumar(2, 3)
print(resultado)  # 5
```

Sin `return`, o con `return` vacio, Python entrega `None` (2.1.2.2). `None` = "nada, caja vacia".

```python
def solo_saluda(nombre):
    print("Hola " + nombre)  # muestra, pero no devuelve nada

x = solo_saluda("Ana")
print(x)  # None
```

Truco de examen: `print` muestra en pantalla, `return` entrega el valor para guardarlo. Son distintos.

## 2.1.3 Parametros (las entradas)

**Posicionales (2.1.3.1):** importa el orden.

```python
def restar(a, b):
    return a - b

print(restar(10, 3))  # 7, a=10 b=3
```

**Con nombre keyword (2.1.3.2):** dices cual es cual, el orden ya no importa.

```python
print(restar(b=3, a=10))  # 7 tambien
```

**Predeterminados (2.1.3.3):** si no me das nada, uso este valor.

```python
def saludar(nombre="amigo"):
    return "Hola " + nombre

print(saludar())       # Hola amigo
print(saludar("Ana"))  # Hola Ana
```

**Variables *args y **kwargs (2.1.3.4):** cuando no sabes cuantos llegaran.

```python
# *args = bolsa con N valores sueltos (llega como tupla)
def sumar_todo(*numeros):
    total = 0
    for n in numeros:
        total = total + n
    return total

print(sumar_todo(1, 2, 3, 4))  # 10

# **kwargs = bolsa con N valores etiquetados (llega como dict)
def mostrar_datos(**datos):
    for etiqueta, valor in datos.items():
        print(etiqueta, valor)

mostrar_datos(nombre="Ana", edad=20)
```

## 2.1.4 Funciones como objetos (la idea estrella funcional)

En Python una funcion es un objeto mas, como un numero o una lista. Eso permite 3 trucos:

**Asignar a variables (2.1.4.1):**

```python
def saludar(nombre):
    return "Hola " + nombre

mi_funcion = saludar  # sin parentesis: guardo la maquina, no la uso
print(mi_funcion("Ana"))  # Hola Ana
```

**Pasar como argumento (2.1.4.2):** le das una maquina a otra maquina.

```python
def aplicar_doble(funcion, valor):
    return funcion(funcion(valor))

def sumar_uno(n):
    return n + 1

print(aplicar_doble(sumar_uno, 5))  # 7
```

Esto es la base de `map, filter` que veras en Unidad III.

**lambda (2.1.4.3):** funcion mini sin nombre, para una sola linea.

```python
# normal
def duplicar(n):
    return n * 2

# lambda: lambda entradas: lo que devuelve
duplicar2 = lambda n: n * 2
print(duplicar2(5))  # 10

# uso tipico: dentro de otra funcion
numeros = [1, 2, 3]
print(list(map(lambda n: n * 2, numeros)))  # [2, 4, 6]
```

## 2.1.5 Recursion: funcion que se llama a si misma

Imagina muñecas rusas: abres una y dentro hay otra igual mas pequeña, hasta llegar a la ultima que ya no se abre.

Necesitas 2 partes (2.1.5.1 y 2.1.5.2):
* **Caso base:** cuando parar.
* **Caso recursivo:** llamarse con algo mas pequeño.

```python
def cuenta_regresiva(n):
    if n <= 0:  # caso base: parar
        print("despegue")
        return
    print(n)
    cuenta_regresiva(n - 1)  # caso recursivo: mismo problema mas chico

cuenta_regresiva(3)
# 3, 2, 1, despegue
```

Clasico factorial: 5! = 5*4*3*2*1

```python
def factorial(n):
    if n <= 1:  # base
        return 1
    return n * factorial(n - 1)  # recursivo

print(factorial(5))  # 120
```

Si olvidas el caso base, nunca para y Python se queja.

## 2.1.6 Documentar: docstrings y comentarios

**docstring (2.1.6.1):** manual pegado a la funcion entre `"""`.

```python
def area_rectangulo(base, altura):
    """Devuelve el area. base y altura deben ser positivos."""
    return base * altura

print(area_rectangulo.__doc__)
```

**Comentarios (2.1.6.2):** notas con `#`. Explica el POR QUE, no lo obvio.

```python
# Ajuste de centavos: si el saldo es menor a 1 centavo, lo dejamos en 0
if saldo < 0.01:
    saldo = 0
```

## 2.1.7 Modulos: cajones para ordenar

Modulo = archivo `.py` con funciones que puedes reutilizar.

```python
# archivo mis_mates.py
def sumar(a, b):
    return a + b
```

```python
# archivo programa.py
import mis_mates  # 2.1.7.2 importar
print(mis_mates.sumar(2, 3))

# otra forma: traer solo lo que ocupo
from mis_mates import sumar
print(sumar(2, 3))
```

Tu proyecto hace esto: `core_cpp` calcula, `gui` muestra. Cada parte en su cajon.

## 2.1.8 Probar que funciona: assert y pruebas

**assert (2.1.8.2):** vigilante que grita si algo esta mal.

```python
def sumar(a, b):
    return a + b

assert sumar(2, 3) == 5  # si no es 5, el programa se detiene aqui
assert sumar(0, 0) == 0
print("todo bien")
```

**Prueba unitaria (2.1.8.1):** probar cada funcion por separado con varios casos, sobre todo los bordes (cero, negativos, vacios).

```python
def dividir(a, b):
    if b == 0:
        return 0  # evitamos rompernos
    return a / b

assert dividir(10, 2) == 5
assert dividir(10, 0) == 0
```

---

# PARTE 3 - Repaso rapido para el examen

## Mini glosario en una linea

* Funcion pura: mismo input, mismo output, no cambia nada fuera.
* Paradigma: estilo de pensar al programar.
* Estado: valor actual de tus variables.
* Inmutabilidad: no cambiar, crear valores nuevos.
* Parametro vs argumento: hueco vs lo que pones en el hueco.
* return vs print: entregar para guardar vs mostrar en pantalla.
* None: nada, vacio.
* *args: muchos valores sueltos. **kwargs: muchos valores con etiqueta.
* lambda: funcion pequeña sin nombre.
* Recursion: funcion que se llama a si misma hasta el caso base.
* Modulo: archivo con funciones reutilizables.
* assert: comprobacion que detiene todo si falla.

## 10 preguntas tipo examen (con respuesta corta)

1. Que es una funcion pura? -> Da lo mismo siempre y no cambia nada fuera.
2. Diferencia POO vs PF? -> POO guarda y cambia estado en objetos, PF transforma con funciones puras.
3. Que devuelve una funcion sin return? -> None.
4. Diferencia print y return? -> print muestra, return entrega para guardar.
5. Que es *args? -> Recibe N valores sueltos como tupla.
6. Que es **kwargs? -> Recibe N valores con nombre como dict.
7. Que es lambda? Da ejemplo. -> Funcion anonima de una linea: `lambda x: x*2`.
8. Partes de una recursion? -> Caso base para parar y caso recursivo que se llama mas chico.
9. list vs tuple? -> list se puede cambiar, tuple no.
10. Para que sirve assert? -> Comprueba que una funcion da lo esperado, si falla se detiene.

## Como conectar esto con tu proyecto

* `amortizacion.cpp`: `calcular_tasa_mensual`, `calcular_fila_frances` son funciones puras de Unidad I y II.
* `graficas.py`: usa `sum(fila["interes"] for fila in tabla)` y comprehensions, ejemplo real de estilo funcional.
* `ventana.py`: es POO (`class AplicacionSimulador`) + funcional (llama al nucleo puro). Perfecto ejemplo de POO vs PF conviviendo.

---

# ANEXO - Temas complementarios

## A.1 Comprehensions (listas de una linea)

Forma corta de crear listas en una sola linea, en vez de usar `for` con `append`.

```python
# Normal
numeros = [1, 2, 3, 4, 5]
doblados = []
for n in numeros:
    doblados.append(n * 2)

# Comprehension (lo mismo, una linea)
doblados = [n * 2 for n in numeros]

# Con condicion
pares = [n for n in range(10) if n % 2 == 0]  # [0, 2, 4, 6, 8]
```

**Ejercicio:** Crea una lista `cuadrados` con los cuadrados de los numeros del 1 al 5 usando comprehension.

## A.2 filter y reduce (herramientas funcionales)

`filter` se queda con algunos elementos, `reduce` junta todo en uno solo.

```python
from functools import reduce

numeros = [1, 2, 3, 4, 5, 6]

# filter: solo pares
pares = list(filter(lambda n: n % 2 == 0, numeros))  # [2, 4, 6]

# reduce: sumar todos
total = reduce(lambda a, b: a + b, numeros)  # 21
```

| Funcion | Hace | Ejemplo |
|---------|------|---------|
| `map` | Transforma cada uno | `[1,2,3]` -> `[2,4,6]` |
| `filter` | Se queda con algunos | `[1,2,3,4]` -> `[2,4]` |
| `reduce` | Junta todo en uno | `[1,2,3,4]` -> `10` |

**Ejercicio:** Usa `filter` para quedarte solo con los numeros mayores a 3 de la lista `[1, 5, 2, 8, 3, 9]`.

## A.3 Manejo de errores (try/except)

Si tu programa se va a romper, mejor que tu decidas que pasa en vez de que Python se cuelgue.

```python
def dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "No puedes dividir entre cero"

print(dividir(10, 0))  # "No puedes dividir entre cero"
print(dividir(10, 2))  # 5.0
```

**Ejercicio:** Escribe una funcion `convertir_a_numero(texto)` que intente convertir el texto a entero. Si no puede, regresa `"Eso no es un numero"`. Prueba con `"42"` y con `"hola"`.

## A.4 Inmutabilidad profunda (no cambiar lo de adentro)

Si copias algo que tiene cosas adentro, copia tambien lo de adentro.

```python
# NO funcional (cambia la original)
original = [[1, 2], [3, 4]]
original[0].append(99)  # ¡Cambiaste la original!

# SI funcional (crea una copia nueva)
original = [[1, 2], [3, 4]]
nueva = [fila[:] for fila in original]  # copia cada fila
nueva[0].append(99)
print(original)  # [[1, 2], [3, 4]]  <- intacta
print(nueva)     # [[1, 2, 99], [3, 4]]
```

**Ejercicio:** Dada la lista `datos = [[10, 20], [30, 40]]`, crea una copia profunda llamada `copia` y agrega `99` al primer sublista de `copia`. Verifica que `datos` sigue igual.
