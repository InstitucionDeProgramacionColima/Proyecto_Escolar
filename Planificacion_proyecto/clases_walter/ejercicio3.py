from clases_walter import temperaturas

def lecutra(temp :float)-> bool:
    return temp <= 50.0

lecturat = tuple[float, ...]=(22, 33.6, 23.1, 4.9, 7.0, 444.0)

lecturasf : list [float] = [t for t in lecturat if lecutra(t)]

lecturas_farenheit: list [float] = [celcius_faren(t) in lecturasf]


print(f"Datos originales: {lecturat}")
print(f"Datos filtrados : {lecturasf}")
print(f"A farenheit: {[round(f, 2) for f in celcius_faren]}")