import re
from collections import Counter

def encontrar_faltantes(texto_a_buscar, prefijo, inicio, fin, ocurrencias):
    """
    Encuentra nros faltantes en un rango, considerando ocurrencias.
    Funciona si el rango es ascendente (1 a 5) o descendente (5 a 1).
    Maneja ceros a la izquierda (ej: "a0001" se trata como "a1").
    """
    # El patrón sigue capturando todos los dígitos (ej: "0001")
    patron = re.escape(prefijo) + r"(\d+)" if prefijo else r"(\d+)"
    encontrados = re.findall(patron, texto_a_buscar)

    # --- INICIO DE LA CORRECCIÓN ---
    # Normalizamos los números: convertimos ["0001", "01", "1"] en ["1", "1", "1"]
    # al pasarlos por int() y luego de vuelta a str().
    numeros_normalizados = [str(int(num)) for num in encontrados]
    
    # Contamos sobre la lista normalizada
    contador_numeros = Counter(numeros_normalizados)
    # --- FIN DE LA CORRECCIÓN ---
    
    faltantes = []
    
    rango_a_revisar = []
    if inicio <= fin:
        rango_a_revisar = range(inicio, fin + 1)
    else:
        rango_a_revisar = range(inicio, fin - 1, -1) 

    for n in rango_a_revisar:
        num_str = str(n) # Esto ya produce "1", "2", "3"...
        veces_encontrado = contador_numeros.get(num_str, 0) # Compara "1" con "1"

        if veces_encontrado < ocurrencias:
            faltantes.append(f"{prefijo}{num_str}")

    return faltantes