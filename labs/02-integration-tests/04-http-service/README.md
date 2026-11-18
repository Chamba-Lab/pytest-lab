# 🧩 2.4 · Un servicio HTTP

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1,5–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · pytest 9.2 · requests 2.34 · pytest-httpserver 1.2 |

## 🎯 Objetivos
- Probar un cliente HTTP contra un servidor de prueba real que corre en tu máquina.
- Comprobar que el cliente pide lo correcto: la ruta, los parámetros y los encabezados.
- Simular las fallas de un servicio a pedido: un error HTTP, una respuesta lenta y un servicio caído.
- Explicar por qué todo cliente HTTP necesita un tiempo de espera (*timeout*).
- Medir cuánto tarda cada prueba con `--durations`.

## 💡 Por qué importa
Tu código habla con servicios de otros: pagos, mapas, el clima. En el lab [2.1](../01-what-changes/README.md) viste que un doble del cliente solo repite lo que creías del servicio. Pero probar contra el servicio de verdad tampoco sirve: no puedes pedirle que se caiga, que tarde diez segundos o que responda 500 justo cuando corre tu prueba. Aquí pruebas el adaptador, el cliente, contra un servidor HTTP **real** que tú programas, con las respuestas y las fallas que necesitas.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, en la carpeta **`starter/`** de este lab. `requests` y `pytest-httpserver` ya están en el `requirements.txt` de la raíz.

## 🧠 Conceptos

### Un servidor de prueba local (*test server*)
El cliente de este lab hace peticiones HTTP: abre una conexión, manda `GET /v1/current?city=Lima` y lee la respuesta. Para probarlo con lo real necesitas algo que escuche en un puerto y responda. La idea es levantar un **servidor HTTP de verdad en tu propia máquina**, solo durante la prueba, y decirle qué responder. El plugin `pytest-httpserver` lo trae como la fixture `httpserver`:

```python
import requests

def test_the_server_answers(httpserver):
    httpserver.expect_request("/hello").respond_with_json({"message": "hola"})

    response = requests.get(httpserver.url_for("/hello"), timeout=2)

    assert response.json() == {"message": "hola"}
```

`url_for("/hello")` es la dirección completa, como `http://127.0.0.1:52817/hello` en este lab: el puerto lo elige el sistema en cada corrida. La petición cruza la red de tu máquina de verdad; lo único que no es real es quién responde.

### Lo que el servidor espera (*expectations*)
`expect_request` no solo dice qué responder: dice **a qué petición**. Además de la ruta, puede exigir los parámetros de la URL (`query_string`) y los encabezados (`headers`):

```python
httpserver.expect_request(
    "/v1/news", query_string={"topic": "deportes"}, headers={"Accept-Language": "es"}
).respond_with_json([])
```

Si llega una petición que no coincide con ninguna expectativa, el servidor no la contesta con lo que registraste. Así, la misma prueba comprueba lo que **mandó** el cliente y lo que hizo con la respuesta.

### Fallas a pedido
Con un servidor que controlas, cada falla es una línea:

| Falla | Cómo se simula |
|---|---|
| Un error del servicio | `respond_with_data("...", status=500)`, o `404` para «no existe» |
| Una respuesta lenta | `.with_post_hook(Delay(1.5))` antes de responder (`from pytest_httpserver.hooks import Delay`) |
| Un servicio caído | Apuntar el cliente a un puerto donde no escucha nadie (en este lab, la fixture `down_url`) |

### Tiempo de espera (*timeout*)
`requests` espera la respuesta **todo lo que haga falta** si no le das un límite: si el servicio se cuelga, tu programa se cuelga con él. Por eso las peticiones llevan `timeout=` en segundos; si se cumple, `requests` lanza `requests.Timeout` en lugar de seguir esperando:

```python
requests.get(url, timeout=2)   # a los 2 s sin respuesta: requests.Timeout
```

## 📚 Documentación
- [pytest-httpserver · Tutorial](https://pytest-httpserver.readthedocs.io/en/latest/tutorial.html)
- [pytest-httpserver · Howto: hooks como `Delay`](https://pytest-httpserver.readthedocs.io/en/latest/howto.html)
- [requests · Timeouts](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)
- [requests · Errores y excepciones](https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions)

## 🧭 Escenario

### El código
[`weather.py`](starter/weather.py) ya funciona: un cliente de un servicio del clima. **No lo cambies.** Recibe la dirección del servicio, la clave y el tiempo de espera, así que la prueba lo apunta a su propio servidor.

| Si el servicio… | `WeatherClient.current(city)`… |
|---|---|
| Responde 200 con `{"city": "Lima", "temp_c": 19.5}` | Devuelve `Reading(city="Lima", celsius=19.5)` |
| Responde 404 | Lanza `CityNotFound` |
| Responde cualquier otro error (500, 503…) | Lanza `WeatherUnavailable` |
| No responde antes del `timeout`, o no está | Lanza `WeatherUnavailable` |

Cada petición es `GET /v1/current?city=<ciudad>`, con la clave en el encabezado `X-Api-Key`.

En [`tests/conftest.py`](starter/tests/conftest.py) ya están la parte de la caza y dos fixtures: `httpserver_listen_address`, que hace que el servidor escuche en `127.0.0.1` (ver 💼), y `down_url`, para la tarea 3. Tus pruebas van en [`tests/test_weather.py`](starter/tests/test_weather.py).

### Cómo se revisa tu trabajo
La caza de mutantes del [lab 1.2](../../01-unit-tests/02-first-tests/README.md). Esta tarda unos 20 segundos: cada mutante corre tus pruebas, y algunas esperan un *timeout* a propósito.

| Mutante | Bug sembrado | Lo mata la tarea |
|---|---|---|
| `m1-wrong-query-name` | Manda la ciudad como `?q=` en vez de `?city=` | 1 |
| `m2-no-api-key` | No manda el encabezado `X-Api-Key` | 1 |
| `m3-reads-wrong-field` | Lee la temperatura del campo `temp` en vez de `temp_c` | 1 |
| `m4-not-found-is-unavailable` | Trata el 404 como cualquier otro error | 2 |
| `m5-errors-parsed` | No revisa el código de estado: intenta leer el JSON de cualquier respuesta | 2 |
| `m6-no-timeout` | Hace la petición sin `timeout` | 3 |
| `m7-network-errors-escape` | Deja escapar los errores de red de `requests` en vez de lanzar `WeatherUnavailable` | 3 |

## ✅ Tareas

Corre todo con este comando, igual en PowerShell o Bash:

```bash
python -m pytest
```

### Tarea 1 · Un servidor de prueba local
**Meta:** que el servidor responda solo a la petición correcta, y comprobar lo que el cliente hace con la respuesta. **La validan:** `[m1-wrong-query-name]`, `[m2-no-api-key]` y `[m3-reads-wrong-field]`.

- [ ] En `conftest.py`, escribe la fixture `client`: pide `httpserver` y devuelve un `WeatherClient` con `httpserver.url_for("/")`, `api_key="test-key-not-secret"` y `timeout=0.5`.
- [ ] En `test_reads_the_current_weather(httpserver, client)`: registra una expectativa para `/v1/current` que exija `city=Lima` y la clave del cliente (`client.api_key`) en `X-Api-Key`, y que responda `{"city": "Lima", "temp_c": 19.5}`. Comprueba el `Reading` completo.

🔮 **Predict first:** si tu expectativa no exigiera el encabezado, ¿qué mutante sobreviviría? ¿Y si no exigiera la ciudad?

### Tarea 2 · Errores HTTP
**Meta:** que cada error del servicio llegue como la excepción correcta. **La validan:** `[m4-not-found-is-unavailable]` y `[m5-errors-parsed]`.

- [ ] En `test_an_unknown_city_is_not_found`: el servidor responde 404 y `current("Atlantis")` lanza `CityNotFound`.
- [ ] En `test_a_server_error_means_unavailable`: el servidor responde 500 y `current` lanza `WeatherUnavailable`.

🔮 **Predict first:** ¿pasaría la prueba del error 500 si te olvidaras de registrar la respuesta, sin ningún `expect_request`?

### Tarea 3 · Lento y caído
**Meta:** que el cliente no se cuelgue cuando el servicio tarda o no está. **La validan:** `[m6-no-timeout]` y `[m7-network-errors-escape]`.

- [ ] En `test_a_slow_service_times_out`: el servidor tarda 1,5 s en responder (`Delay(1.5)`), más que el `timeout` del cliente (0,5 s), y `current` lanza `WeatherUnavailable`.
- [ ] En `test_a_service_that_is_down_is_unavailable(down_url)`: crea un `WeatherClient` apuntado a `down_url`, con `timeout=0.5`, y comprueba que lanza `WeatherUnavailable`.

🔮 **Predict first:** la prueba del servicio caído no tiene ningún `Delay`. ¿Cuánto crees que tarda? Mídelo con el comando de la 🔍 *Command dissection*.

**Criterio de éxito:** `python -m pytest` dentro de `starter/` termina en verde: 13 pruebas pasan, ninguna se salta.

## 🔍 Command dissection
| Código | Qué hace |
|---|---|
| `httpserver.url_for("/ruta")` | La URL completa del servidor de prueba, con su puerto |
| `expect_request(ruta, query_string={...}, headers={...})` | La petición que el servidor espera; `method="POST"` cambia el método (por defecto, cualquiera) |
| `.respond_with_json(datos)` · `.respond_with_data(texto, status=N)` | La respuesta: JSON con código 200, o texto con el código que elijas |
| `httpserver.check_assertions()` | Falla si el servidor recibió algo que no esperaba |
| `python -m pytest --durations=5` | Al final, las cinco fases más lentas (preparación, prueba y limpieza) con su tiempo |

## 💼 En proyectos reales
- **Revisa que el servidor no recibió nada raro.** Una petición que no coincide con ninguna expectativa no rompe la prueba por sí sola (ver la respuesta de la tarea 2). Llama a `httpserver.check_assertions()` al final de las pruebas que dependen de un error.
- **`localhost` puede costar medio segundo por petición en Windows.** Antes de fijar `httpserver_listen_address`, el servidor escuchaba en `localhost` y cada petición del cliente tardaba 0,5 s, justo su `timeout`. Windows prueba primero la dirección IPv6 (`::1`), donde no escucha nadie, espera, y recién después usa `127.0.0.1`. Con el servidor en `127.0.0.1`, las mismas pruebas pasaron de 3,6 s a 1,6 s.
- **Ponle `timeout` a toda petición en producción.** Sin él, un servicio colgado deja hilos y procesos esperando para siempre. Hay herramientas de análisis de código, como el linter Ruff (regla `S113`), que marcan las peticiones sin `timeout`.
- **Los dobles del transporte existen**, como [responses](https://pypi.org/project/responses/) o [respx](https://pypi.org/project/respx/): reemplazan a `requests` sin abrir ninguna conexión. Son más rápidos, pero no cruzan la red, así que no ven un `timeout` mal puesto ni un puerto cerrado.
- **Contra el servicio real de verdad**, algunos equipos corren pocas pruebas, aparte y con una marca (lab 1.4), contra el entorno de prueba (*sandbox*) del proveedor, para confirmar que su servidor de prueba sigue diciendo lo mismo que el servicio.

## 🚀 Reto extra
Agrega a `WeatherClient` (en tu rama, no en el lab) un reintento: si el servicio responde 503, vuelve a pedir una vez. Pruébalo con `httpserver.expect_ordered_request`, que responde a las peticiones en el orden en que las registraste: primero un 503 y después la respuesta buena. ¿Cómo compruebas que no reintenta ante un 404?

## 🆘 Pistas
<details><summary>Pista 1 · dirección</summary>

La fixture `client` es como las del lab 1.4, pero pide `httpserver`. En cada prueba, primero registras con `expect_request` lo que el servidor responde, y después llamas al cliente dentro de `pytest.raises` cuando esperas un error.
</details>

<details><summary>Pista 2 · más concreta</summary>

```python
httpserver.expect_request(
    "/v1/current", query_string={"city": "Lima"}, headers={"X-Api-Key": client.api_key}
).respond_with_json({"city": "Lima", "temp_c": 19.5})
```

Tarea 3: `httpserver.expect_request("/v1/current").with_post_hook(Delay(1.5)).respond_with_json({...})`.
</details>

## ✔️ Respuestas verificadas
<details><summary>Ábrelas solo después de terminar las tareas</summary>

Se ejecutó con pytest 9.2.0; el CI verifica cada lab en Python 3.12 y 3.15.

**Tarea 1.** Sin el encabezado en la expectativa sobrevive `m2-no-api-key`; sin la ciudad, `m1-wrong-query-name`. En los dos casos el servidor responde a la petición mala como si fuera buena, y el cliente recibe el JSON. Cuando la expectativa sí los exige, la petición del mutante no coincide, el servidor no la contesta con lo registrado y el cliente lo nota:

```text
E           weather.WeatherUnavailable: the service answered 500
```

`m3` muere por otra razón: lee un campo que el servicio no manda (`KeyError: 'temp'`), el mismo bug del ejemplo del lab 2.1. Aquí lo atrapa una prueba porque la respuesta tiene el formato del servicio, no el que el cliente supone.

**Tarea 2.** Sí, pasa. Una petición que no coincide con ninguna expectativa recibe un **500** del propio servidor de prueba, con el texto `No handler found for request`, y el cliente lo convierte en `WeatherUnavailable`, que es justo lo que la prueba esperaba. La prueba pasa por la razón equivocada: comprueba «nadie registró nada», no «el servicio falló». Con `httpserver.check_assertions()` al final, falla y lo dice:

```text
E           AssertionError: No handler found for request <Request 'http://127.0.0.1:63368/v1/current?city=Lima' [GET]> with data b''.
```

`m5` muere en la versión buena porque intenta leer como JSON el texto del error: `requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`.

**Tarea 3.** En Windows, alrededor de **0,5 s**, lo mismo que la prueba lenta:

```text
0.52s call     tests/test_weather.py::test_a_slow_service_times_out
0.50s call     tests/test_weather.py::test_a_service_that_is_down_is_unavailable
```

En Windows, una conexión a un puerto cerrado de tu propia máquina no se rechaza al instante: el sistema reintenta durante unos 2 s (lo medimos sin `timeout`: 2,03 s). Con `timeout=0.5`, `requests` se rinde antes y lanza `ConnectTimeout`, que es a la vez un `Timeout` y un `ConnectionError`. En Linux, el rechazo llegó en 0,02 s. Por eso `m7` deja escapar este error del sistema:

```text
E           urllib3.exceptions.ConnectTimeoutError: (<HTTPConnection(host='127.0.0.1', port=56939) at 0x...>, 'Connection to 127.0.0.1 timed out. (connect timeout=0.5)')
```

Y `m6`, sin `timeout`, espera los 1,5 s del servidor, recibe la respuesta y no lanza nada: `Failed: DID NOT RAISE WeatherUnavailable`.
</details>

## 🎤 Autoevaluación
1. ¿Qué ve una prueba contra un servidor de prueba local que no ve una prueba con un mock del cliente?
2. ¿Por qué conviene que la expectativa exija los parámetros y los encabezados, y no solo la ruta?
3. Una prueba de «el servicio respondió 500» pasa aunque nadie registró el 500. ¿Cómo puede pasar y cómo lo evitas?
4. ¿Qué le pasa a tu aplicación en producción si un cliente HTTP no tiene `timeout` y el servicio se cuelga?
5. Tu suite de integración tarda cada día más. ¿Cómo encuentras las pruebas lentas, y qué dos causas de este lab revisarías primero?

La solución completa está en [`solution/`](solution/).

**Siguiente:** 2.5 · Dependencias en contenedores (electivo), o directo al [proyecto 2.P](../project-expense-import/README.md)
