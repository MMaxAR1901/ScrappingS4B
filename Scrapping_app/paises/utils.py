import requests
from bs4 import BeautifulSoup
from .models import Pais
from django.core.exceptions import ObjectDoesNotExist


URL = "https://www.scrapethissite.com/pages/simple/"


def scrapearPaises():

    # Obtenemos la página
    try:
        respuesta = requests.get(URL, timeout=8)
        respuesta.raise_for_status()
    except Exception as e:
        print(f"Error al obtener la página: {e}")
        return

    sopa = BeautifulSoup(respuesta.text, "html.parser")
    paises_html = sopa.select("div.country")

    for pais_html in paises_html:

        # extracción de datos, basandonos en el codigo fuente.
        def limpiezaTexto(selector):
            tag = pais_html.select_one(selector)
            return tag.get_text(strip=True) if tag else ""

        nombreSucio = limpiezaTexto("h3.country-name")
        capital = limpiezaTexto("span.country-capital")
        poblacion_str = limpiezaTexto("span.country-population")
        area_str = limpiezaTexto("span.country-area")

        # normalización para los nombres
        nombre = " ".join(nombreSucio.replace("\xa0", " ").split()).upper()

      
        # convertimos población y area a int y float
        try:
            poblacion = int(poblacion_str.replace(",", ""))
            area = float(area_str.replace(",", ""))
        except ValueError:
            print(f"Error en datos numéricos para {nombre}")
            continue

        ## si el pais existe lo actualizamos, sino lo crearemos
        try:
            pais_obj = Pais.allObjects.get(nombre__iexact=nombre)

            # Actualizar
            pais_obj.capital = capital
            pais_obj.poblacion = poblacion
            pais_obj.area = area
            pais_obj.eliminado = False
            pais_obj.save()

        except ObjectDoesNotExist:
            # Crear
            Pais.objects.create(
                nombre=nombre,
                capital=capital,
                poblacion=poblacion,
                area=area,
                eliminado=False,
            )

        except Exception as e:
            print(f"Error inesperado al procesar {nombre}: {e}")
            continue
