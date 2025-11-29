from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Pais
from .utils_ollama import interpretar_consulta
from .utils import scrapearPaises


def parseValor(valor: str):
    #convierte un valor string a int, float o strin
    valor = valor.strip()

    # Eliminar comillas
    if (valor.startswith("'") and valor.endswith("'")) or \
       (valor.startswith('"') and valor.endswith('"')):
        valor = valor[1:-1]

    # int
    if valor.isdigit():
        return int(valor)

    # float
    try:
        return float(valor)
    except ValueError:
        return valor


def procesarFiltrosOllama(filtroStr: str):
    ##procesaremos las respuestas ORM de ollama :p
    filtros = {}
    limite = None

    partes = [p.strip() for p in filtroStr.split(",") if "=" in p]

    for parte in partes:
        clave, valor = [x.strip() for x in parte.split("=", 1)]
        valor = parseValor(valor)

        # Meta parámetro de límite
        if clave == "__limit":
            if isinstance(valor, int) and valor > 0:
                limite = valor
            continue

        # Filtro normal
        filtros[clave] = valor

    return filtros, limite


def cargarPaises(request):
    scrapearPaises()
    return redirect("listaPaises")


def listaPaises(request):

    # Pais.objects.all() usa el Manager que solo muestra los activos
    paises = Pais.objects.all()
    consultaUsuario = request.GET.get("consulta", "").strip()

    filtros = {}
    limite = None
    mensajeError = None
    
    # 💡 SOLUCIÓN: ORDENACIÓN POR DEFECTO de A a Z
    paises = paises.order_by('nombre') 

    if consultaUsuario:
        respuesta = interpretar_consulta(consultaUsuario)
        filtroStr = respuesta.get("query") if isinstance(respuesta, dict) else respuesta

        if not filtroStr:
            mensajeError = "No se pudo interpretar la consulta."
        elif "ERROR" in filtroStr:
            mensajeError = "La consulta solicita campos no disponibles."
        else:
            try:
                filtros, limite = procesarFiltrosOllama(filtroStr)

                if filtros:
                    paises = paises.filter(**filtros)

            except Exception as error:
                print(f"[ERROR IA] Filtro: {filtroStr} | Error: {error}")
                mensajeError = "Error al procesar la consulta."

    if limite is not None and limite > 0:
        paises = paises[:limite] 

    contexto = {
        "paises": paises,
        "consulta_actual": consultaUsuario,
        "error": mensajeError,
    }

    return render(request, "paises/lista.html", contexto)


def borradoLogicoPais(request, pk):
    """Realiza un borrado lógico usando el manager allObjects."""
    # Usamos allObjects para asegurar que encontramos el país incluso si ya estaba inactivo
    pais = get_object_or_404(Pais.allObjects, pk=pk)
    pais.delete()
    return redirect("listaPaises")