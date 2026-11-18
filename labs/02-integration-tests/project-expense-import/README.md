# 🏗️ 2.P · Proyecto: importar gastos

| ⏱️ Duración | 🧪 Tipo | 🧱 Bloque | 🛠️ Stack |
|---|---|---|---|
| 3–4 h escribir la suite · 1–2 h revisar | 🏗️ `project` | 2 · Pruebas de integración | Python 3.12+ · pytest 9.2 · requests 2.34 · pytest-httpserver 1.2 · SQLite |

## 🎯 Objetivos
- Escribir desde cero la suite de integración de una aplicación de tres piezas que hablan con algo real: un archivo, una base de datos y un servicio HTTP.
- Aplicar todo el bloque en un mismo lugar: datos de prueba junto a las pruebas, una base nueva por prueba, un servidor de prueba local y sus fallas.
- Comprobar transacciones de verdad: después de cada error, mirar cómo quedó la base, no solo qué excepción salió.
- **La pregunta del dominio:** si una importación falla a la mitad, ¿la base queda exactamente como estaba, y el mismo archivo se puede volver a importar? Tu suite tiene que darse cuenta el día en que no sea así.

## 📍 Dónde correr los comandos
Con el entorno virtual activo (el de la raíz ya trae pytest, requests y pytest-httpserver), cada parte se corre desde su carpeta:
- **Tu suite:** dentro de `your-suite/`.
- **La caza que acepta el proyecto:** dentro de `acceptance/`.
- **La aplicación y la suite de referencia:** dentro de `reference/`.

## 🛣️ Dos formas de usar este proyecto
| Camino | Qué haces | Tiempo |
|---|---|---|
| 🔨 **Construir y comparar** | Lee [BRIEF.md](BRIEF.md), escribe tu suite en `your-suite/tests/` (en tu rama o fork), pásale la caza de `acceptance/` y después lee [REVIEW.md](REVIEW.md) para comparar tu suite con la de `reference/` | 3–4 h |
| 🔍 **Solo revisar** | Lee la suite de `reference/tests/` guiado por [REVIEW.md](REVIEW.md), pásale la caza y rómpela: borra una prueba y mira qué mutante sobrevive | 1–2 h |

**Recomendación:** construye si resolviste los labs 2.2 a 2.4 sin mirar las soluciones. Aquí nadie te dice qué datos elegir ni qué estado revisar después de un error, y es justo lo que el bloque enseñó. Si tienes poco tiempo, revisa, pero haz al menos tres veces el ejercicio de «borra una prueba».

### Mirar la suite de referencia funcionando
Dentro de `reference/`, igual en PowerShell o Bash:

```bash
python -m pytest --durations=3
```

**Qué deberías ver:**

```text
0.51s call     tests/test_rates.py::test_a_service_that_is_down_means_unavailable
0.51s call     tests/test_rates.py::test_a_slow_service_means_unavailable
0.48s teardown tests/test_store.py::test_a_saved_import_survives_closing_the_database
16 passed in 1.74s
```

Dieciséis pruebas con un archivo, una base y un servidor reales, en menos de dos segundos. Las dos más lentas esperan un `timeout` a propósito (lab 2.4); la limpieza de la última prueba es la que apaga el servidor de prueba.

### Escribir y correr tu suite
[`your-suite/`](your-suite/) ya trae su [`pyproject.toml`](your-suite/pyproject.toml), que importa la aplicación desde `../reference/src`, un [`conftest.py`](your-suite/tests/conftest.py) con `httpserver_listen_address` y una primera prueba de ejemplo en [`tests/test_store.py`](your-suite/tests/test_store.py). Dentro de `your-suite/`, en PowerShell o Bash:

```bash
python -m pytest
```

### Pasarle la caza a tu suite
La caza corre tu suite contra la aplicación real y contra los 13 mutantes del [BRIEF](BRIEF.md#criterios-de-aceptación). Por defecto caza con la suite de referencia; para usar la tuya, nombra su carpeta en `EXPENSES_SUITE` (la ruta es relativa a `acceptance/`). Dentro de `acceptance/`:

PowerShell:

```powershell
$env:EXPENSES_SUITE = "../your-suite"
python -m pytest
Remove-Item Env:EXPENSES_SUITE
```

Bash:

```bash
EXPENSES_SUITE=../your-suite python -m pytest
```

Con la suite de ejemplo tal cual (una sola prueba), la caza termina así:

```text
13 failed, 1 passed
```

Pasa el guardián (tu suite pasa con la aplicación real) y sobreviven los 13 mutantes. Cuando tu suite esté completa:

```text
14 passed
```

La caza tarda alrededor de medio minuto con una suite completa: corre tu suite 14 veces, y cada vez esperas los `timeout` de tus pruebas.

### Pasarle la caza a la referencia
Sin `EXPENSES_SUITE`, la caza usa `reference/`. Dentro de `acceptance/`, en PowerShell o Bash:

```bash
python -m pytest
```

```text
14 passed
```

## 👥 Suites de la comunidad
¿Escribiste la tuya? Abre un issue con el enlace a tu fork o rama y la agregamos aquí. No se copian dentro de este repositorio: solo se mantiene una referencia.

## 🔁 Retrospectiva
- ¿Qué mutante te costó más matar, y qué dato o qué comprobación te faltaba?
- ¿Cuántas de tus pruebas comprueban el estado de la base después de un error? ¿Cuáles solo miran la excepción?
- Si hiciste el electivo 2.5: ¿qué prueba de tu suite correrías también contra PostgreSQL, y por qué esa?
- ¿Qué lab del bloque conviene repasar?
