from django.shortcuts import render
from .models import Persona
from .forms import PersonaForm
from .external import apiReniec
from decouple import config

tokenApi = config('TOKEN')
def personaRegister(request):
    form = None
    persona = None
    mensaje = None

    if request.method == 'POST':
        form = PersonaForm(request.POST)
        dni = request.POST.get('dni')

        if Persona.objects.filter(dni=dni).exists():
            persona = Persona.objects.get(dni=dni)
            mensaje = "Registro encontrado"

        elif form.is_valid():

            try:
                # Si no existe, consultar a la api de la reniec
                api = apiReniec.ApiNet(tokenApi)
                res = api.get_person(dni)

                if (res):
                    nombres = res.get('nombres')
                    apellidoPat = res.get('apellidoPaterno')
                    apellidoMat = res.get('apellidoMaterno')

                    # guardar la nueva persona
                    persona = Persona(
                        dni=dni,
                        nombre=nombres,
                        apePaterno=apellidoPat,
                        apeMaterno=apellidoMat
                    )
                    persona.save()
                    mensaje = "Datos obtenidos satisfactoriamente"
                else:
                    mensaje = "Error al obtener los datos de la API"
            except Exception as e:
                mensaje = "Error al procesar la solicitud"
        else:
            mensaje = "Formulario invalido"
    else:
        form = PersonaForm()
    print(form)
    return render(request, 'persona/registrarPersona.html', {'form': form, 'persona': persona, 'mensaje': mensaje})


