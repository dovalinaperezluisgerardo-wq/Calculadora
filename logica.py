# Importamos FastAPI para crear nuestra API
from fastapi import FastAPI

# Importamos BaseModel para crear el modelo
# que validará los datos recibidos
from pydantic import BaseModel

# Importamos CORSMiddleware para permitir
# que nuestro frontend pueda comunicarse con la API
from fastapi.middleware.cors import CORSMiddleware


# Creamos nuestra aplicación FastAPI
app = FastAPI()


# Configuramos CORS
# Esto permite que el navegador acepte las peticiones
# que vienen desde nuestro frontend
app.add_middleware(
    CORSMiddleware,
# Permitimos peticiones desde cualquier origen
    allow_origins=["*"],
# Permitimos el envío de credenciales
    allow_credentials=True,
# Permitimos cualquier método HTTP
# como GET, POST, PUT, DELETE, etc.
    allow_methods=["*"],
# Permitimos cualquier encabezado HTTP
    allow_headers=["*"],
)


# Creamos un modelo para los datos
# que recibirá nuestra calculadora
class DatosCalculadora(BaseModel):
# Primer número de la operación
    primer_numero: float
# Operación que queremos realizar
    operacion: str
# Segundo número de la operación
    segundo_numero: float


# Creamos una ruta POST llamada /calcular
# Aquí recibiremos los datos enviados por JavaScript
@app.post("/calcular")
def calcular(datos: DatosCalculadora):

    try:

        # Obtenemos el primer número enviado
        numero_1 = datos.primer_numero
        # Obtenemos el segundo número enviado
        numero_2 = datos.segundo_numero
        # Creamos un objeto de nuestra clase Calculadora
        # utilizando el primer número
        calculadora = Calculadora(numero_1)
        # Ejecutamos la operación solicitada
        operacion = calculadora.operar(
        datos.operacion,numero_2)
        # Devolvemos el resultado obtenido
        return operacion
        # Capturamos el error cuando se intenta
        # dividir entre cero
    except ZeroDivisionError as error:
        # Convertimos el error a texto y lo enviamos
        # como respuesta JSON
        return {"error": str(error)}

        # Capturamos errores relacionados
        # con valores inválidos
    except ValueError as error:

        # Enviamos el mensaje del error
        return {"error": str(error)}


# Creamos la clase que contiene
# la lógica de nuestra calculadora
class Calculadora:

    # Constructor de la clase
    def __init__(self, numero_inicial):

    # Guardamos el número inicial
        self.numero = numero_inicial

    # Guardamos una copia del número inicial
    # para poder utilizarlo cuando presionamos C
        self.numero_inicial = numero_inicial

    # Método encargado de realizar las operaciones
    def operar(self, opcion, segundo_numero=None):
    # Si la opción recibida es C,
    # restauramos el número inicial
        if opcion == "c":
            self.numero = self.numero_inicial
            # Guardamos el resultado
            resultado = {"resultado": self.numero}

        # Comprobamos que exista un segundo número
        if segundo_numero is None:
        # Si no existe, lanzamos un error
            raise TypeError("ingresa un numero")

        # Si la operación es suma
        if opcion == "+":
            resultado = self.numero + segundo_numero


        # Si la operación es resta
        elif opcion == "-":

            resultado = self.numero - segundo_numero


        # Si la operación es multiplicación
        elif opcion == "x":

            resultado = self.numero * segundo_numero


        # Si la operación es división
        elif opcion == "/":

        # Comprobamos manualmente si el segundo número es 0
            if segundo_numero == 0:
                # Lanzamos nuestro propio error
                raise ZeroDivisionError("ERROR")
            # Realizamos la división
            resultado = self.numero / segundo_numero

        # Si ninguna operación coincide
        else:
        # Lanzamos un error indicando
        # que el tipo de número es inválido
            raise ValueError("tipo de numero invalido")

        # Devolvemos el resultado dentro
        # de un diccionario
        return {"resultado": resultado}
