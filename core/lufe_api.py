import os
import requests
from dotenv import load_dotenv, find_dotenv
from django.http import FileResponse, HttpResponse, StreamingHttpResponse

load_dotenv(find_dotenv(filename="apikey.env"))

API_BASE_URL = "https://legajounicoapi.produccion.gob.ar/lufe"
API_KEY = os.getenv("APIKEY")


# Función para llamar a la API y manejar errores devuelve un JSON
def llamar_api(endpoint: str, params: dict = None) -> dict | None:
    #print(f"API_KEY disponible: {'Sí' if API_KEY else 'No'}")
    #print(f"API_KEY valor: {API_KEY}")

    headers = {"apikey": API_KEY}
    #print(f"Headers enviados: {headers}")

    url = f"{API_BASE_URL}/{endpoint}"
    #print(f"URL de la petición: {url}")

    try:
        response = requests.get(url, headers=headers, params=params)
        #print(f"Código de respuesta: {response.status_code}")
        #print(f"Respuesta completa: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error detallado al llamar a la API: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Respuesta de error: {e.response.text}")
        return None


def descargar_zip(endpoint: str, filename: str) -> bool:
    headers = {"apikey": API_KEY}
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            #print(f"Archivo {filename} guardado correctamente.")
            return True
        else:
            print(f"Error {response.status_code}: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Error al descargar el archivo: {e}")
        return False

# Endpoints que devuelven un JSON
def get_entidad(cuit: str) -> dict | None:
    return llamar_api(f"entidades/{cuit}")

def get_indicadores(cuit: str) -> dict | None:
    return llamar_api(f"entidades/{cuit}/indicadores")

def get_indicadores_por_periodo(cuit: str, periodo: str) -> dict | None:
    return llamar_api(f"entidades/{cuit}/periodos/{periodo}/indicadores")

def get_indicadores_post_balance(cuit: str) -> dict | None:
    return llamar_api(f"entidades/{cuit}/indicadorespostbalance")

def get_autoridades(cuit: str) -> dict | None:
    return llamar_api(f"entidades/{cuit}/autoridades")

def get_documentos(cuit: str) -> dict | None:
    return llamar_api(f"entidades/{cuit}/documentos")

def get_documentos_por_periodo(cuit: str, periodo: str) -> dict | None:
    return llamar_api(f"entidades/{cuit}/periodos/{periodo}/documentos")

def get_deudas(cuit: str) -> dict | None:
    return llamar_api(f"entidades/{cuit}/deudas")

def get_periodos(cuit: str) -> dict | None:
    return llamar_api(f"entidades/{cuit}/periodos")

# Funciones que devuelven archivos ZIP
def get_entidades_zip(path="entidades.zip") -> bool:
    return descargar_zip("/downloadentidadesall", path)


def get_indicadores_zip(path="indicadores.zip") -> bool:
    return descargar_zip("/downloadindicadoresall", path)

def get_autoridades_zip(path="autoridades.zip") -> bool:
    return descargar_zip("/downloadautoridadesall", path)

def get_empleo_zip(path="empleo.zip") -> bool:
    return descargar_zip("/downloadempleoall", path)

def descargar_entidades_zip(request):
    folder = "entidades"
    filename = "entidades.zip"
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)
    if get_entidades_zip(full_path):
        if os.path.exists(full_path):
            return FileResponse(open(full_path, "rb"), as_attachment=True, filename=filename)
    return HttpResponse("No se pudo descargar el archivo.", status=400)

def descargar_indicadores_zip(request):
    folder = "indicadores"
    filename = "indicadores.zip"
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)
    if get_indicadores_zip(full_path):
        if os.path.exists(full_path):
            return FileResponse(open(full_path, "rb"), as_attachment=True, filename=filename)
    return HttpResponse("No se pudo descargar el archivo.", status=400)

def descargar_autoridades_zip(request):
    folder = "autoridades"
    filename = "autoridades.zip"
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)
    if get_autoridades_zip(full_path):
        if os.path.exists(full_path):
            return FileResponse(open(full_path, "rb"), as_attachment=True, filename=filename)
    return HttpResponse("No se pudo descargar el archivo.", status=400)

def descargar_empleo_zip(request):
    folder = "empleo"
    filename = "empleo.zip"
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)
    print("Llamando a get_empleo_zip()")
    resultado = get_empleo_zip(full_path)
    print("Resultado de get_empleo_zip():", resultado)
    print("Existe el archivo?", os.path.exists(full_path))
    if resultado and os.path.exists(full_path):
        return FileResponse(open(full_path, "rb"), as_attachment=True, filename=filename)
    return HttpResponse("No se pudo descargar el archivo.", status=400)
