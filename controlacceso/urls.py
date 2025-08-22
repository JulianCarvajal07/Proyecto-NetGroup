from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_usuario, name='login'),
    path('preregistro/', views.preregistro, name='preregistro'),
    path('registronoc/', views.registronoc, name='registronoc'),
    path('visitantes/', views.visitantes, name='visitantes'),
    path('guardar_firma/', views.guardar_firma, name='guardar_firma'),
    path('guardar_salida_noc/', views.guardar_salida_noc, name='guardar_salida_noc'),
    path('salida/', views.boton_salida, name='boton_salida'),
    path('buscar_por_identificacion/', views.buscar_por_identificacion, name='buscar_por_identificacion'),
    path('modificar_visitante/', views.modificar_visitante, name='modificar_visitante'),
]

if settings.DEBUG:
        #Esta función genera rutas automáticas para que Django pueda servir archivos almacenados en la carpeta MEDIA_ROOT (carpeta base) usando la URL MEDIA_URL.
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


