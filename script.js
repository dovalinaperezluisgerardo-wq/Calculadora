// Buscamos el elemento <p> dentro de la pantalla de la calculadora.
const pantalla = document.querySelector(".pantalla p");

// Buscamos todos los botones de la calculadora.
const botones = document.querySelectorAll(".botones button");

// Guarda el primer número de la operación.
let primer_numero = "";

// Guarda el número que estamos escribiendo actualmente.
let numero_actual = "";

// Guarda la operación seleccionada.
let operacion_actual = "";

// Indica si acabamos de obtener un resultado.
let resultado_obtenido = false;


// Recorremos todos los botones.
botones.forEach((boton) => {

    // Detectamos cuando el usuario hace clic en un botón.
    boton.addEventListener("click", async () => {

        // Comprobamos si el botón es una operación.
        if (boton.classList.contains("operacion")) {

            // Si tenemos un número y todavía no tenemos
            // un resultado, lo guardamos como primer número.
            if (numero_actual !== "" && !resultado_obtenido) {
                primer_numero = numero_actual;
            }

            // Guardamos la operación seleccionada.
            operacion_actual = boton.textContent;

            // Limpiamos el número actual para escribir
            // el segundo número.
            numero_actual = "";

            // Indicamos que todavía no tenemos un resultado nuevo.
            resultado_obtenido = false;
        }


        // Comprobamos si el botón es "=".
        else if (boton.classList.contains("igual")) {

            // Si no hay segundo número, no hacemos nada.
            if (numero_actual === "") {
                return;
            }

            // Creamos el objeto que enviaremos a la API.
            const datos = {
                primer_numero: primer_numero,
                operacion: operacion_actual,
                segundo_numero: numero_actual
            };


            // Enviamos los datos a FastAPI.
            const respuesta = await fetch(
                "http://127.0.0.1:8000/calcular",
                {
                    // Utilizamos el método POST.
                    method: "POST",

                    // Indicamos que estamos enviando JSON.
                    headers: {
                        "Content-Type": "application/json"
                    },

                    // Convertimos el objeto JavaScript
                    // en una cadena JSON.
                    body: JSON.stringify(datos)
                }
            );


            // Convertimos la respuesta de la API
            // en un objeto JavaScript.
            const resultado = await respuesta.json();


            // Comprobamos si la API devolvió un error.
            if (resultado.error) {

                // Mostramos el error en la pantalla.
                pantalla.textContent = resultado.error;
            }


            // Si no hubo ningún error.
            else {

                // Mostramos el resultado.
                pantalla.textContent = resultado.resultado;

                // Guardamos el resultado como primer número
                // para poder continuar haciendo operaciones.
                primer_numero = resultado.resultado;

                // Limpiamos el segundo número.
                numero_actual = "";

                // Indicamos que ya obtuvimos un resultado.
                resultado_obtenido = true;
            }
        }


        // Comprobamos si el botón es "C".
        else if (boton.classList.contains("borrar")) {

            // Reiniciamos el primer número.
            primer_numero = "";

            // Reiniciamos el número actual.
            numero_actual = "";

            // Reiniciamos la operación.
            operacion_actual = "";

            // Indicamos que no tenemos resultado.
            resultado_obtenido = false;

            // Mostramos 0 en la pantalla.
            pantalla.textContent = "0";
        }


        // Si no es operación, "=" ni "C",
        // entonces es un botón numérico.
        else {

            // Agregamos el número presionado al número actual.
            numero_actual += boton.textContent;

            // Mostramos el número en la pantalla.
            pantalla.textContent = numero_actual;
        }
    });
});