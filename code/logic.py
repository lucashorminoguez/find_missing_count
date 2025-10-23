import re
from collections import Counter

def encontrar_faltantes(texto_a_buscar, prefijo, inicio, fin, repeticiones):
    patron = re.escape(prefijo) + r"(\d+)" if prefijo else r"(\d+)"
    encontrados = re.findall(patron, texto_a_buscar)
    
    faltantes = []
    
    if repeticiones < 2:
        numeros_encontrados = set(int(n) for n in encontrados)
        faltantes = [f"{prefijo}{n}" for n in range(inicio, fin + 1) if n not in numeros_encontrados]
    else:
        contador_numeros = Counter(encontrados)
        for n in range(inicio, fin + 1):
            num_str = str(n)
            veces_encontrado = contador_numeros.get(num_str, 0)
            if veces_encontrado < repeticiones:
                faltantes.append(f"{prefijo}{num_str}")

    return faltantes
