def celcius_faren(celcius: float) -> float:
    return((celcius * 9/5) +32 )

temp_base: float = 20.60

temp_f: float = celcius_faren(temp_base)

print(f"La temperstura original es de: {temp_base:>8.2}")
print(f"La temperatura en F:{celcius_faren:>8.2}")
