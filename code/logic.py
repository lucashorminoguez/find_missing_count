import re
from collections import Counter

def encontrar_faltantes(texto_a_buscar, prefijo, inicio, fin, repeticiones):
    """
    Encuentra nros faltantes en un rango, considerando repeticiones.
    Funciona si el rango es ascendente (1 a 5) o descendente (5 a 1).
    """
    patron = re.escape(prefijo) + r"(\d+)" if prefijo else r"(\d+)"
    encontrados = re.findall(patron, texto_a_buscar)

    contador_numeros = Counter(encontrados)
    
    faltantes = []
    
    rango_a_revisar = []
    if inicio <= fin:
        rango_a_revisar = range(inicio, fin + 1)
    else:
        rango_a_revisar = range(inicio, fin - 1, -1) 

    for n in rango_a_revisar:
        num_str = str(n)
        veces_encontrado = contador_numeros.get(num_str, 0)

        if veces_encontrado < repeticiones:
            faltantes.append(f"{prefijo}{num_str}")

    return faltantes