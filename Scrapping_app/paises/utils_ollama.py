import ollama

def interpretar_consulta(texto):

    MODELO = "gemma3:4b" 

    prompt = f"""
Actúa como un Experto en Backend Django y ORM. Tu única tarea es traducir lenguaje natural a argumentos de filtros de consultas (QuerySet filters) de Django.

CONTEXTO DE LA BASE DE DATOS:
Trabajas exclusivamente con el modelo 'Pais'.
Los únicos campos disponibles son:
1. nombre (String): El nombre del país. Usa 'istartswith' o 'icontains'.
2. capital (String): La capital del país. Usa 'istartswith' o 'icontains'.
3. poblacion (Integer): Cantidad de habitantes. Usa 'gt' (mayor que), 'lt' (menor que), 'gte', 'lte'.
4. area (Float): Área en km2.

REGLAS ESTRICTAS:
1. NO inventes campos (ej: no uses 'continente').
2. Tu salida debe ser SOLO los argumentos dentro de la función .filter().
3. Si hay múltiples condiciones, sepáralas por coma.
4. NO uses JSON. NO uses Markdown. Solo devuelve el texto plano.
5. Si la instrucción no tiene sentido o pide campos imposibles, responde: ERROR

EJEMPLOS (Few-Shot):
Entrada de usuario: "Busca países que empiecen con M"
salida: nombre__istartswith='M'

Entrada de usuario: "Paises con población mayor a 5 millones"
salida: poblacion__gt=5000000

Entrada de usuario: "Muestrame paises con area menor a 1000 y que la capital contenga la letra A"
salida: area__lt=1000, capital__icontains='A'

Entrada de usuario: "Paises con población entre 1000 y 5000"
salida: poblacion__gte=1000, poblacion__lte=5000

Entrada de usuario: "Paises que inicien con S y terminen con A"
salida: nombre__istartswith='S', nombre__iendswith='A'





INSTRUCCIÓN ACTUAL:
"{texto}"
Assistant:
"""

    try:
        
        resp = ollama.generate(model=MODELO, prompt=prompt)
        
        resultado = resp["response"].strip()

        # Elimanos los markdown para que en views no haya problema 
        resultado = resultado.replace("```python", "").replace("```", "").strip()
        
        # Liamparemos el modelo para tomar en cuenta las respuesas ORM
        if "Assistant:" in resultado:
            resultado = resultado.split("Assistant:")[-1].strip()

        return resultado

    except Exception as e:
        print(f"Error conectando con Ollama: {e}")
        return ""