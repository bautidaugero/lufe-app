import os
from dotenv import load_dotenv
from django.shortcuts import render
import requests
from django.http import FileResponse, HttpResponse
from .lufe_api import get_entidad, get_indicadores, get_indicadores_por_periodo, get_indicadores_post_balance, get_autoridades, get_documentos, get_documentos_por_periodo, get_deudas, get_periodos
from .lufe_api import get_entidades_zip, get_indicadores_zip, get_autoridades_zip, get_empleo_zip
import json

load_dotenv()

API_KEY = os.getenv("APIKEY")

def home(request):
    return render(request, "core/home.html")

def buscar_entidad(request):
    entidad = None
    error = None
    if request.method == "POST":
        cuit = request.POST.get("cuit")
        if cuit:
            entidad = get_entidad(cuit)
            if entidad is None:
                error = "No se encontró la entidad o hubo un error en la consulta."
        else:
            error = "Debe ingresar un CUIT."
    return render(request, "core/buscar_entidad.html", {"entidad": json.dumps(entidad) if entidad else None, "error": error})

def buscar_indicadores(request):
    indicadores = None
    error = None
    if request.method == "POST":
        cuit = request.POST.get("cuit")
        if cuit:
            indicadores = get_indicadores(cuit)
            if indicadores is None:
                error = "No se encontraron indicadores o hubo un error en la consulta."
        else:
            error = "Debe ingresar un CUIT."
    return render(request, "core/buscar_indicadores.html", {"indicadores": json.dumps(indicadores) if indicadores else None, "error": error})

from .lufe_api import get_autoridades

def buscar_autoridades(request):
    autoridades = None
    error = None
    if request.method == "POST":
        cuit = request.POST.get("cuit")
        if cuit:
            autoridades = get_autoridades(cuit)
            if autoridades is None:
                error = "No se encontraron autoridades o hubo un error en la consulta."
        else:
            error = "Debe ingresar un CUIT."
    return render(request, "core/buscar_autoridades.html", {"autoridades": json.dumps(autoridades) if autoridades else None, "error": error})

def buscar_documentos(request):
    documentos = None
    error = None
    cuit = ""
    periodo = ""
    if request.method == "POST":
        cuit = (request.POST.get("cuit") or "").strip()
        periodo = (request.POST.get("periodo") or "").strip()
        if cuit:
            if periodo:
                documentos = get_documentos_por_periodo(cuit, periodo)
            else:
                documentos = get_documentos(cuit)
            # Extrae el archivo_id correctamente
            if documentos and "documentos" in documentos:
                for doc in documentos["documentos"]:
                    doc["archivo_id"] = doc["url"].split("/")[-1]
            if not documentos:
                error = "No se encontraron documentos o hubo un error en la consulta."
        else:
            error = "Debe ingresar un CUIT."
    return render(
        request,
        "core/buscar_documentos.html",
        {"documentos": documentos, "error": error, "cuit": cuit, "periodo": periodo}
    )

def descargar_documento(request, cuit, archivo_id):
    api_url = f"https://legajounicoapi.produccion.gob.ar/lufe/entidades/{cuit}/archivos/{archivo_id}"
    api_key = os.getenv("API_KEY")
    headers = {"apikey": API_KEY}
    response = requests.get(api_url, headers=headers)
    print(headers)
    if response.status_code == 200:
        filename = response.headers.get('Content-Disposition', 'documento.pdf')
        resp = HttpResponse(response.content, content_type=response.headers.get('Content-Type', 'application/pdf'))
        resp['Content-Disposition'] = f'attachment; filename="{cuit}.pdf"'
        return resp
    else:
        return HttpResponse("No se pudo descargar el archivo.", status=400)

def buscar_deudas(request):
    deudas = None
    error = None
    cuit = ""
    if request.method == "POST":
        cuit = (request.POST.get("cuit") or "").strip()
        if cuit:
            deudas = get_deudas(cuit)
            if not deudas:
                error = "No se encontraron deudas o hubo un error en la consulta."
        else:
            error = "Debe ingresar un CUIT."
    return render(
        request,
        "core/buscar_deudas.html",
        {"deudas": json.dumps(deudas) if deudas else None, "error": error, "cuit": cuit}
    )

def buscar_periodos(request):
    periodos = None
    error = None
    cuit = ""
    if request.method == "POST":
        cuit = (request.POST.get("cuit") or "").strip()
        print("CUIT recibido:", cuit)  # <-- Agrega este print
        if cuit:
            periodos = get_periodos(cuit)
            print("Respuesta de get_periodos:", periodos)  # <-- Y este print
            if not periodos:
                error = "No se encontraron períodos o hubo un error en la consulta."
        else:
            error = "Debe ingresar un CUIT."
    return render(
        request,
        "core/buscar_periodos.html",
        {"periodos": periodos, "error": error, "cuit": cuit}
    )

def descargar_entidades_zip(request):
    folder = "entidades"
    filename = "entidades.zip"
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)
    if get_entidades_zip():  # Asegúrate que get_entidades_zip guarde en full_path
        if os.path.exists(full_path):
            return FileResponse(open(full_path, "rb"), as_attachment=True, filename=filename)
    return HttpResponse("No se pudo descargar el archivo.", status=400)

def descargar_indicadores_zip(request):
    folder = "indicadores"
    filename = "indicadores.zip"
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)
    if get_indicadores_zip():  # Asegúrate que get_indicadores_zip guarde en full_path
        if os.path.exists(full_path):
            return FileResponse(open(full_path, "rb"), as_attachment=True, filename=filename)
    return HttpResponse("No se pudo descargar el archivo.", status=400)

def descargar_autoridades_zip(request):
    folder = "autoridades"
    filename = "autoridades.zip"
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)
    if get_autoridades_zip():  # Asegúrate que get_autoridades_zip guarde en full_path
        if os.path.exists(full_path):
            return FileResponse(open(full_path, "rb"), as_attachment=True, filename=filename)
    return HttpResponse("No se pudo descargar el archivo.", status=400)

def descargar_empleo_zip(request):
    folder = "empleo"
    filename = "empleo.zip"
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)
    print("Llamando a get_empleo_zip()")
    resultado = get_empleo_zip()  # Asegúrate que get_empleo_zip guarde en full_path
    print("Resultado de get_empleo_zip():", resultado)
    print("Existe el archivo?", os.path.exists(full_path))
    if resultado and os.path.exists(full_path):
        return FileResponse(open(full_path, "rb"), as_attachment=True, filename=filename)
    return HttpResponse("No se pudo descargar el archivo.", status=400)









