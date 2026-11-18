# 🗺️ Sílabo · Testing en Python con pytest

**Meta:** escribir y mantener pruebas automatizadas con criterio profesional: pruebas que fallan por la razón correcta.
**Público:** sabes Python básico (funciones, clases, módulos) y escribiste pocas pruebas o ninguna → puedes probar un proyecto real en sus tres niveles y mantener la suite en equipo.
**Stack:** Python 3.12+ (verificado en 3.12 y 3.15) · pytest 9.2.0 · pytest-cov 7.1.0. Bloque 2: requests y pytest-httpserver; el electivo 2.5, testcontainers con Docker. Las librerías de los bloques 3 y 4 ya están elegidas (ver el mapa de construcción); sus versiones se fijan al construirlos.
**Sesiones:** 1–2 h por lab

**Leyenda**
- Estado: ⬜ `pending` sin construir · 🟨 `built` construido y verificado, esperando a un aprendiz · ✅ `done` resuelto por un aprendiz y con su feedback aplicado
- Tipo de tema: 🎯 `core` el camino · 🔬 `deep-dive` más a fondo · 🔀 `alternative` otra tecnología · ➕ `elective` opcional · 🆕 `modern` pone el camino al día
- Tipo de lab: 🧩 `challenge` starter + solución · 🔭 `exploration` demo guiada · 💭 `concept` sin código · 🏗️ `project` cierra el bloque

## El camino de un vistazo
| Bloque | Al terminar podrás… | Estado |
|---|---|---|
| 1 · Pruebas unitarias | Escribir, diseñar y organizar pruebas unitarias que atrapan bugs reales | 🟨 `built` |
| 2 · Pruebas de integración | Probar tu código junto con lo real: archivos, una base de datos y un servicio HTTP | ⬜ `pending` |
| 3 · Pruebas de aceptación | Probar el sistema completo como lo usa una persona: una línea de comandos y una API web | ⬜ `pending` |
| 4 · Calidad de la suite | Mantener una suite confiable en equipo: arreglar pruebas inestables, escribir la prueba primero, medir qué bugs atrapa y correrla sola en cada cambio | ⬜ `pending` |

Cada bloque sube un nivel en la pirámide de pruebas (lab 1.1) y se apoya en el anterior. Los términos del oficio están en el [glosario](GLOSSARY.md).

## Bloque 1 · Pruebas unitarias
Escribir, diseñar y organizar pruebas unitarias que atrapan bugs reales.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| [1.1](labs/01-unit-tests/01-what-is-a-test/README.md) | Qué es una prueba y sus tipos | 🎯 `core` | 💭 `concept` | Distinguir una prueba unitaria de una de integración o de aceptación, y reconocer una prueba que no puede fallar | 🟨 `built` |
| [1.2](labs/01-unit-tests/02-first-tests/README.md) | Primeras pruebas con pytest | 🎯 `core` | 🧩 `challenge` | Escribir, correr y leer pruebas; comprobar resultados, decimales y errores | 🟨 `built` |
| [1.3](labs/01-unit-tests/03-test-case-design/README.md) | Diseño de casos de prueba | 🎯 `core` | 🧩 `challenge` | Elegir qué casos probar (uno por clase de datos, los límites y los errores) y escribirlos como una tabla | 🟨 `built` |
| [1.4](labs/01-unit-tests/04-organize-suite/README.md) | Organizar la suite | 🎯 `core` | 🧩 `challenge` | Compartir la preparación entre pruebas, y marcar y elegir qué pruebas correr | 🟨 `built` |
| [1.5](labs/01-unit-tests/05-test-doubles/README.md) | Dobles de prueba | 🎯 `core` | 🧩 `challenge` | Aislar tu código del reloj, los archivos, el entorno y los servicios externos | 🟨 `built` |
| [1.6](labs/01-unit-tests/06-coverage/README.md) | Cobertura | 🎯 `core` | 🔭 `exploration` | Medir qué ejecutan tus pruebas y saber qué no te dice esa cifra | 🟨 `built` |
| [1.P](labs/01-unit-tests/project-split-bill/README.md) | Proyecto: dividir la cuenta | 🎯 `core` | 🏗️ `project` | Escribir desde cero la suite unitaria de una aplicación de línea de comandos que ya funciona | 🟨 `built` |

## Bloque 2 · Pruebas de integración
Probar tu código junto con lo real: archivos, una base de datos y un servicio HTTP.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| [2.1](labs/02-integration-tests/01-what-changes/README.md) | Qué cambia al integrar | 🎯 `core` | 💭 `concept` | Decidir qué parte de un sistema probar con lo real y cuál con un doble, y mantener cada prueba aislada aunque use algo real | 🟨 `built` |
| [2.2](labs/02-integration-tests/02-real-files/README.md) | Archivos reales | 🎯 `core` | 🧩 `challenge` | Probar código que lee y escribe archivos: guardar datos de prueba, comparar lo escrito con un archivo esperado y no caer en las diferencias entre Windows y Linux | 🟨 `built` |
| [2.3](labs/02-integration-tests/03-real-database/README.md) | Una base de datos real | 🎯 `core` | 🧩 `challenge` | Probar consultas contra SQLite, preparando la base antes de cada prueba y limpiándola después | 🟨 `built` |
| 2.4 | Un servicio HTTP | 🎯 `core` | 🧩 `challenge` | Probar un cliente HTTP contra un servidor de prueba local y simular sus fallas: errores, respuestas lentas y un servicio caído | ⬜ `pending` |
| 2.5 | Dependencias en contenedores | ➕ `elective` | 🔭 `exploration` | Levantar PostgreSQL en un contenedor solo durante las pruebas y ver qué esconde probar con SQLite. Necesita Docker | ⬜ `pending` |
| 2.P | Proyecto: importar gastos | 🎯 `core` | 🏗️ `project` | Escribir la suite de integración de un importador que lee un archivo, consulta un servicio de tipos de cambio y guarda en una base de datos | ⬜ `pending` |

## Bloque 3 · Pruebas de aceptación
Probar el sistema completo como lo usa una persona: una línea de comandos y una API web.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 3.1 | Aceptación y criterios de aceptación | 🎯 `core` | 💭 `concept` | Escribir criterios de aceptación con la forma Dado / Cuando / Entonces y elegir qué recorridos merecen una prueba de punta a punta | ⬜ `pending` |
| 3.2 | Una línea de comandos de caja negra | 🎯 `core` | 🧩 `challenge` | Probar un programa de terminal como proceso aparte: argumentos, salida, errores y código de salida | ⬜ `pending` |
| 3.3 | Una API web de punta a punta | 🎯 `core` | 🧩 `challenge` | Probar una API web levantada de verdad, por sus rutas y respuestas | ⬜ `pending` |
| 3.4 | Pruebas en el navegador | ➕ `elective` | 🔭 `exploration` | Automatizar un recorrido en un navegador real y entender por qué estas pruebas son las más frágiles | ⬜ `pending` |
| 3.P | Proyecto: agenda de turnos | 🎯 `core` | 🏗️ `project` | Escribir la suite de aceptación de una API de turnos a partir de su contrato | ⬜ `pending` |

## Bloque 4 · Calidad de la suite
Mantener una suite confiable en equipo: arreglar pruebas inestables, escribir la prueba primero, medir qué bugs atrapa y correrla sola en cada cambio.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 4.1 | Pruebas inestables | 🎯 `core` | 🔭 `exploration` | Reconocer, reproducir y arreglar una prueba que falla a veces | ⬜ `pending` |
| 4.2 | Desarrollo guiado por pruebas | 🎯 `core` | 🧩 `challenge` | Escribir la prueba antes que el código, en ciclos cortos de rojo, verde y refactorización | ⬜ `pending` |
| 4.3 | Pruebas basadas en propiedades | 🔬 `deep-dive` | 🧩 `challenge` | Describir reglas que se cumplen para cualquier dato y dejar que la herramienta busque el contraejemplo | ⬜ `pending` |
| 4.4 | Mutation testing | 🔬 `deep-dive` | 🔭 `exploration` | Medir con una herramienta qué bugs dejaría pasar tu suite, como la caza de mutantes de los labs | ⬜ `pending` |
| 4.5 | La suite en integración continua | 🎯 `core` | 🔭 `exploration` | Correr la suite sola en cada cambio, en varias versiones de Python, con cobertura y sin pruebas lentas en el camino | ⬜ `pending` |
| 4.P | Proyecto: rescatar una suite | 🎯 `core` | 🏗️ `project` | Llevar una suite heredada (inestable, lenta y sin automatizar) a un estado confiable, y correrla en cada cambio | ⬜ `pending` |

## Reglas de diseño
1. **La app más pequeña que hace visible el tema.** Cada lab trae su propio módulo pequeño; ninguno arrastra el dominio del anterior.
2. **Ninguna aplicación crece lab tras lab:** la integración ocurre en el proyecto del bloque.
3. **Cada tema tiene un único lab dueño**, que lo enseña. Los labs siguientes lo usan y enlazan a su dueño.
4. **Labs de testing al revés:** el código de producción ya está terminado; tú escribes las pruebas. Tus pruebas se validan con una **caza de mutantes**: deben pasar con el código real y fallar contra versiones con bugs sembrados. El proyecto de cada bloque funciona igual.
5. **Primero la idea, después pytest.** Cada lab presenta el concepto sin la herramienta y luego muestra cómo lo escribe pytest.
6. **Un bloque por nivel de la pirámide.** Las pruebas de integración y de aceptación tienen sus propios bloques; el bloque 1 se queda en las unitarias.
7. **Lo real, sin dejar rastro.** Desde el bloque 2 las pruebas usan cosas reales (archivos, una base de datos, un servidor), y cada prueba prepara lo que usa y lo limpia al terminar: nada queda en tu máquina ni pasa de una prueba a otra.
8. **El camino principal no necesita Docker.** Solo el electivo 2.5 lo usa, y sus pruebas se saltan solas cuando Docker no está.

## Mapa de construcción
| ID | Dueño de | Se apoya en | Parte de |
|---|---|---|---|
| 1.1 | Qué es una prueba, los niveles de la pirámide, Arrange-Act-Assert, las propiedades de una buena prueba, la prueba que no puede fallar, qué es un mutante | — | Nada: solo `CONCEPT.md` |
| 1.2 | Descubrimiento de pruebas, `assert` y su introspección, `pytest.approx` y `Decimal`, `pytest.raises`, leer un fallo, `-k` / `-x` / `-v`, la caza de mutantes | 1.1 | Módulo `grades.py` terminado |
| 1.3 | Clases de equivalencia, valores límite, un caso por razón de fallo, `parametrize` e `ids` | 1.2 | Módulo `passwords.py` terminado |
| 1.4 | Fixtures, fixtures que usan fixtures, `scope`, `conftest.py`, marcas propias, `-m`, `markers` en la configuración | 1.2, 1.3 | Módulo `cart.py` terminado |
| 1.5 | Inyección de dependencias, dummy / stub / fake / spy / mock, `tmp_path`, `create_autospec`, `monkeypatch` | 1.4 | Módulo `loans.py` terminado |
| 1.6 | Cobertura de líneas y de ramas, pytest-cov, los límites de la cobertura | 1.2, 1.3 | `demo/` terminado |
| 1.P | `capsys`, fixtures que devuelven una función, archivos con BOM | 1.1–1.6 | La aplicación `splitbill` terminada; la suite, desde cero |
| 2.1 | Qué es una prueba de integración por dentro: el borde entre tu código y lo real, cuándo integrar y cuándo usar un doble, aislamiento con recursos compartidos (preparar, limpiar, independencia del orden), el costo de lo real | 1.1, 1.5 | Nada: solo `CONCEPT.md` |
| 2.2 | Datos de prueba junto a las pruebas (`Path(__file__).parent`), archivos esperados (*golden files*), texto frente a bytes, `encoding` y `newline`, carpetas que faltan y archivos que ya existen | 1.3, 1.5 (`tmp_path`) | Módulo `roster.py` terminado |
| 2.3 | Fixtures con `yield` (preparar y limpiar), `sqlite3` y la base `:memory:` por prueba, parámetros en el SQL, datos sembrados, transacciones (*commit*, *rollback*, `with conn:`); el *rollback* por prueba va en 💼 | 1.4, 2.1 | Módulo `scores.py` terminado |
| 2.4 | Servidor de prueba local (pytest-httpserver), revisar lo que pidió el cliente, errores HTTP, tiempo de espera (*timeout*), conexión rechazada | 1.5, 2.3 | Cliente HTTP terminado con requests |
| 2.5 | testcontainers, una base de datos en un contenedor por sesión, diferencias entre SQLite y PostgreSQL, saltar sin Docker | 2.3 | `demo/` terminado |
| 2.P | Lo que falte va en «Lo nuevo de este proyecto» del BRIEF | 2.1–2.4 | La aplicación terminada; la suite, desde cero |
| 3.1 | Criterios de aceptación (Dado / Cuando / Entonces), caja negra, qué recorridos merecen una prueba de punta a punta | 1.1, 2.1 | Nada: solo `CONCEPT.md` |
| 3.2 | Correr un programa desde una prueba (`subprocess`), argumentos, salida estándar y de error, código de salida, entorno del proceso | 3.1 | Una CLI terminada (puede retomar `splitbill`: sus pruebas de caja negra están en la historia de git) |
| 3.3 | Levantar la app en otro proceso (uvicorn), esperar a que esté lista, puerto libre, probar por sus rutas | 3.2, 2.4 | API terminada con FastAPI |
| 3.4 | Playwright con pytest-playwright, selectores, esperas automáticas, por qué es la prueba más frágil | 3.3 | `demo/` terminado |
| 3.P | Lo que falte va en «Lo nuevo de este proyecto» del BRIEF | 3.1–3.3 | La API de turnos terminada y su contrato; la suite, desde cero |
| 4.1 | Causas de inestabilidad (orden, tiempo, estado compartido, azar), orden aleatorio con pytest-randomly, por qué reintentar es un parche | 1.4, 1.5 | `demo/` con una suite inestable |
| 4.2 | TDD: rojo, verde y refactorizar en ciclos cortos | 1.3 | Un módulo vacío: el aprendiz escribe las pruebas y el código |
| 4.3 | Propiedades, estrategias de datos y el contraejemplo mínimo (*shrinking*) con Hypothesis | 1.3 | Módulo terminado |
| 4.4 | Mutation testing con cosmic-ray (corre en Windows; mutmut necesita WSL), mutantes que sobreviven, costo | 1.2 | `demo/` con un módulo y su suite |
| 4.5 | Integración continua (CI) con GitHub Actions, matriz de versiones, cobertura mínima, separar las pruebas lentas | 1.4, 1.6 | `demo/` con un repositorio pequeño |
| 4.P | Lo que falte va en «Lo nuevo de este proyecto» del BRIEF | 4.1–4.5 | Una aplicación con una suite heredada, con problemas sembrados |

## Notas para los siguientes labs
- El entorno es único (`.venv` en la raíz, `requirements.txt`). Cada variante tiene su `pyproject.toml` con `[tool.pytest]` y `pythonpath = ["."]`.
- La caza de mutantes vive en `tests/test_mutant_hunt.py` de cada challenge, con los mutantes en `tests/mutants/<id>/` y un `tests/conftest.py` que antepone el mutante a la ruta de importación según una variable de entorno. Los stubs del starter usan `pytest.skip("TODO …")`. Copia la caza del lab 1.2 y cambia el módulo y la variable (`GRADES_MUTANT` → la del nuevo lab); conserva `PYTHONIOENCODING=utf-8` (ver `docs/lessons.md`).
- Cada trampa del README se verifica en una copia limpia con un script que imprime cuántas pruebas corrieron; los mutantes se generan con un script que exige que cada reemplazo ocurra exactamente una vez.
- 1.4 revisa la organización con `tests/test_structure.py`. En `conftest.py`, la parte de la caza va arriba (antes de importar el módulo) y las fixtures abajo. Los stubs del starter no piden fixtures en su firma: una fixture inexistente es un *error* de preparación, no un `skip`.
- El proyecto 1.P se valida con una caza de mutantes de toda la aplicación (`acceptance/`), que corre la suite del aprendiz contra la referencia y contra cada mutante. El bloque 3 puede retomar `splitbill`: las pruebas de caja negra de su línea de comandos están en la historia de git (antes de la reconstrucción del bloque 1).
- **El bloque 1 está construido completo (1.1–1.6 y 1.P).** Queda esperar el feedback de quienes lo resuelvan; el CI corre el verificador en Python 3.12 y 3.15 y la caza del proyecto.
- **Los bloques 2 a 4 están planificados** (18 nov 2026): librerías elegidas y dominio de cada proyecto. El bloque 2 se construye ahora; los bloques 3 y 4 esperan el primer feedback del bloque 1, porque copiarán sus patrones. Las versiones se fijan al construir cada bloque.
- **Bloque 2:** `tmp_path` y `monkeypatch` son del 1.5; el 2.2 los usa con un enlace, sin volver a enseñarlos. Las fixtures con `yield` son del 2.3. Las dependencias del 2.5 (testcontainers y el driver de PostgreSQL) van en un `requirements` propio del lab, para que el camino principal no las instale.
