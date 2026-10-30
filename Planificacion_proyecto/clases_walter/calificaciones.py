def calificaciones(n1, n2, n3) -> float: 
    return((n1 + n2 + n3 )/5.0)

def aprueba(promedio:float) -> bool:
    return(promedio >5.9)

def reporte(estudiante: str, promedio:float, aprobado:bool) -> str:
    estado:str = "Aprobado" if aprobado else "Reprobado"
    return f"Alumno {estudiante :<12} | promedio: {promedio:>5.2f} | Estodo: {aprobado}"
alumno:str = "kelvin"
calif_a: float = 9.0
calib: float = 8.6
calic : float = 5.4

promedio_final : float = calificaciones(calif_a, calib, calic)
aprobado : bool = aprueba(promedio_final)
repo : str = reporte(alumno, promedio_final, aprobado)
print(repo)