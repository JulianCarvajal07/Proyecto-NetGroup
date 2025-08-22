from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre, contrasena=None, rol='noc'):
        if not nombre:
            raise ValueError("El usuario debe tener un nombre")
        usuario = self.model(nombre=nombre, rol=rol)
        usuario.set_password(contrasena)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, nombre, contrasena):
        usuario = self.create_user(nombre=nombre, contrasena=contrasena, rol='admin')
        usuario.is_admin = True
        usuario.save(using=self._db)
        return usuario

#==================================================================================================

class Usuarios(AbstractBaseUser):
    ID = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    rol = models.CharField(max_length=20, default='noc')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'nombre'
    REQUIRED_FIELDS = ['rol']

    def __str__(self):
        return self.nombre

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'Usuarios'
        managed = True

#==================================================================================================

class visita (models.Model):
    id = models.AutoField(primary_key=True)
    tipoidentificacion = models.CharField(max_length=20)
    identificacion = models.CharField(max_length=30) 
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    empresa = models.CharField(max_length=100, null=True, blank=True)
    cargo = models.CharField(max_length=50, null=True, blank=True)
    ingresavehiculo = models.BooleanField(default=False)
    placa = models.CharField(max_length=10, null=True, blank=True)  
    notarjeta = models.CharField(max_length=20) 
    autoriza= models.CharField(max_length=100)
    foto= models.TextField(null=True, blank=True)  # Almacenar la foto como una cadena base64
    firma = models.TextField(null=True, blank=True)  # Almacenar la firma como una cadena base64
    usuario_noc = models.CharField(max_length=100)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    horadeingresonoc = models.DateTimeField(null=True, blank=True)
    horadesalidanoc = models.DateTimeField(null=True, blank=True)
    motivovisita = models.CharField(max_length=255)
    nombre_archivo_foto = models.CharField(max_length=100, null=True, blank=True)
    nombre_archivo_firma = models.CharField(max_length=100, null=True, blank=True)




    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.identificacion}"

    
    class Meta:
        db_table = 'visita'  # Nombre exacto de la tabla en MySQL
        managed = True      # Para que Django no intente crearla ni modificarla

# Create your models here.
