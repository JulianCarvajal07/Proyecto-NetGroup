import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.contrib import messages
from .models import Usuarios, visita
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q
import pytz
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login  as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib import messages





COLOMBIA_TZ = pytz.timezone('America/Bogota')


#INGRESO DE PAGINA PRINCIPAL

def inicio(request):
    return render(request, 'paginas/login.html')

#==========================================================================================================

#INGRESO DE USUARIOS 
def login_usuario(request):
    if request.method == 'POST':
        usuario_input = request.POST['nombre']
        contraseña_input = request.POST['contrasena']
        user = authenticate(request, username=usuario_input, password=contraseña_input)

        if user is not None:
            auth_login(request, user)
            return redirect('preregistro')
        else:
            error = "Usuario o contraseña incorrectos"
            return render(request, 'paginas/login.html', {'error': error})


    return render(request, 'login.html')

#==========================================================================================================


def preregistro(request):

    if request.method == 'POST':
        campos_obligatorios = [
            'txttipoidentificacion',
            'txtidentificacion',
            'txtnombre',
            'txtapellido',
            'txttelefono',
            'txtempresa',
            'txtcargo',
            'txtnotarjeta',
            'txtautoriza',
            'txtmotivovisita',
            'foto',
        ]

        faltantes = [campo for campo in campos_obligatorios if not request.POST.get(campo)]

        if faltantes:
            messages.error(request, "ERROR, ALGUNOS CAMPOS SON OBLIGATORIOS")

        else:
            tipoidentificacion = request.POST['txttipoidentificacion']
            identificacion = request.POST['txtidentificacion']
            nombre = request.POST['txtnombre'].upper()
            apellido = request.POST['txtapellido'].upper()
            telefono = request.POST['txttelefono']
            empresa = request.POST.get('txtempresa', '').upper()
            cargo = request.POST.get('txtcargo', '').upper()
            ingresavehiculo = 'txtingresavehiculo' in request.POST
            placa = request.POST.get('txtplaca', '').upper()
            notarjeta = request.POST['txtnotarjeta']
            autoriza = request.POST['txtautoriza']
            motivovisita = request.POST.get('txtmotivovisita')
            foto = request.POST.get('foto')

            nueva_visita = visita(
                tipoidentificacion=tipoidentificacion,
                identificacion=identificacion,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                empresa=empresa,
                cargo=cargo,
                ingresavehiculo=ingresavehiculo,
                placa=placa,
                notarjeta=notarjeta,
                autoriza=autoriza,
                motivovisita=motivovisita,
                foto=foto,
            )
            nueva_visita.save()
            messages.success(request, "Visita registrada correctamente.")

    return render(request, 'paginas/preregistro.html')


#===========================================================================================================

def registronoc(request):
    
    visitantenoc = visita.objects.exclude(
            Q(firma__isnull=False) &
            Q(horadeingresonoc__isnull=False) &
            Q(horadesalidanoc__isnull=False)
            |
            Q(fecha_salida__isnull=False)
    ).order_by('-id')

    return render(request, 'paginas/registronoc.html', {'visitantes': visitantenoc})


#===========================================================================================================
@login_required(login_url='/login/')
def guardar_firma(request):

    if request.method == 'POST':
        firma_base64 = request.POST.get('firma')
        visitante_id = request.POST.get('visitante_id')
        
        print("Firma recibida:", firma_base64[:100])  # Muestra los primeros 100 caracteres
        print("Visitante ID:", visitante_id)
               
        if not firma_base64 or not visitante_id:
            #Puedes manejar el error aquí si falta algo
            return redirect('registronoc')  # o mostrar un mensaje

        visitante = visita.objects.get(id=visitante_id)
        visitante.firma = firma_base64  # Guardar directamente como texto
        visitante.horadeingresonoc = timezone.now() #Marca la hora de ingreso                                            
        visitante.usuario_noc = request.user.nombre # Guardar el nombre del usuario que registro la firma del visitante

        visitante.save()
        print("✅ Firma guardada correctamente.")
        print("Ingeniero que lo ingreso:", visitante.usuario_noc)  # Debería mostrar el nombre del usuario logueado


        # Redirigir a la misma página o a otra
        return redirect('registronoc')  # o 'lista_visitantes'
    
    #===================================================================================
def guardar_salida_noc(request):
    if request.method == 'POST':
        visitante_id = request.POST.get('visitante_id')
        hora_salida_str= request.POST.get('horadesalidanoc')
        motivo_visita = request.POST.get('motivovisita')

        if not visitante_id or not hora_salida_str:
            print("⚠️ Datos incompletos:", visitante_id, hora_salida_str)
            messages.error (request,"SE DEBE LLENAR TODOS LOS CAMPOS PARA REGISTRAR LA SALIDA DEL NOC")
            return redirect('registronoc')

        try:
            visitante = visita.objects.get(id=visitante_id)
            hora_salida = datetime.fromisoformat(hora_salida_str)
            visitante.horadesalidanoc = hora_salida
            visitante.motivovisita = motivo_visita  # Guardar el motivo de la visita
            visitante.save()
            print("✅ Hora de salida guardada correctamente.")


            # return redirect('registronoc')  # Redirigir a la página de registro NOC
        
            # Determinar si el campo motivovisita está vacío o no
            deshabilitar_motivo = bool(visitante.motivovisita and visitante.motivovisita.strip())
            
            return render(request, 'registronoc.html', {
                'visitante': visitante,
                'deshabilitar_motivo': deshabilitar_motivo
            })


        except Exception as e:
            return redirect('registronoc')
         #   print("❌ Error al guardar la hora de salida:", e)
          #  return HttpResponse("Error interno", status=500)
        
#===========================================================================================================
def boton_salida(request):
    if request.method == 'POST':
        visitante_id = request.POST.get('visitante_id')
        print("Visitante ID para marcar salida:", visitante_id)
        if visitante_id:
            try:
                visitante = visita.objects.get(id=visitante_id)
                visitante.fecha_salida = timezone.now()
                visitante.save()
            except visita.DoesNotExist:
                messages.error(request, "Visitante no encontrado.")
                return redirect('visitantes')
    
    return redirect('visitantes')

#===========================================================================================================


def visitantes(request):
    query = request.GET.get('q')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    visitas = visita.objects.all()  # ✅ usamos el modelo correcto

    paginator = Paginator(visitas, 10)  # ← Aquí se define siempre

    page_number = request.GET.get('page') or 1  # ← Por defecto, página 1
    page_obj = paginator.get_page(page_number)


    # 🔍 Búsqueda general
    if query:
        visitas = visitas.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(identificacion__icontains=query) |
            Q(empresa__icontains=query) |
            Q(cargo__icontains=query) |
            Q(telefono__icontains=query) |
            Q(autoriza__icontains=query) |
            Q(usuario_noc__icontains=query) |
            Q(motivovisita__icontains=query)
        )

    # 📅 Filtro por fecha
    if desde:
        visitas = visitas.filter(fecha_ingreso__gte=desde)
    if hasta:
        visitas = visitas.filter(fecha_ingreso__lte=hasta)

    # ✅ Filtros dinámicos por campo
    campos_dinamicos = ['autoriza', 'telefono', 'empresa', 'cargo']
    for campo in campos_dinamicos:
        valor = request.GET.get(f'filtro_{campo}')
        if valor:
            filtro = {f"{campo}__icontains": valor}
            visitas = visitas.filter(**filtro)

    context = {
        'visitantes': visitas,
        'query': query,
        'desde': desde,
        'hasta': hasta,
        'page_obj': page_obj,
    }

    return render(request, 'paginas/visitantes.html', context)
#===========================================================================================================

def buscar_por_identificacion(request):
    if request.method == 'GET' and 'txtidentificacion' in request.GET:
        try:
            identificacion = request.GET['txtidentificacion'].strip()
            
            if not identificacion:
                return JsonResponse({'error': 'Identificación vacía'}, status=400)
            
            # Usamos filter() en lugar de get() para obtener todos los resultados
            visitantes = visita.objects.filter(identificacion=identificacion)
            
            if not visitantes.exists():
                return JsonResponse({'error': 'No encontrado'}, status=404)
                
            # Tomamos el último registro (puedes cambiar la lógica según tus necesidades)
            ultimo_visitante = visitantes.latest('fecha_ingreso')  # Asegúrate de tener este campo
            
            response_data = {
                #'txttipoidentificacion': ultimo_visitante.tipoidentificacion,
                'txtnombre': ultimo_visitante.nombre,
                'txtapellido': ultimo_visitante.apellido,
                'txttelefono': ultimo_visitante.telefono,
                'txtempresa': ultimo_visitante.empresa,
                'txtcargo': ultimo_visitante.cargo,
                'txtingresavehiculo': ultimo_visitante.ingresavehiculo,
                'txtplaca': ultimo_visitante.placa if ultimo_visitante.ingresavehiculo else '',
                #'txtnotarjeta': ultimo_visitante.notarjeta,
                #'txtautoriza': ultimo_visitante.autoriza,
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({'error': f'Error en el servidor: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Solicitud inválida'}, status=400)









