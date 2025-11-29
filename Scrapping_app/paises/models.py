from django.db import models

class FiltroPaisesNoEliminados(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(eliminado=False)


class Pais(models.Model):
    """utilizamos Unique para que no se repitan los nombres y se agreguen a la base de datos"""
    nombre = models.CharField(max_length=50, unique= True)
    capital = models.CharField(max_length=50) 
    poblacion = models.BigIntegerField()
    area = models.FloatField() 
    eliminado = models.BooleanField(default=False) 

    # solo muestra los paises que no han sido borrados logicamente
    objects = FiltroPaisesNoEliminados()

    # Muestra todos los paises para que en cada carga nueva no de error de llave duplicada
    allObjects = models.Manager()

    def __str__(self):
        return self.nombre
    
    def delete(self, *arg, **kwargs):
        ## actualizamos el atributo de pais de eliminado a true
        self.eliminado = True
        self.save()