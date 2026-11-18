# 🗺️ Sílabo · Testing en Python con pytest

**Meta:** escribir y mantener pruebas automatizadas con criterio profesional: pruebas que fallan por la razón correcta.
**Público:** sabes Python básico (funciones, clases, módulos) y escribiste pocas pruebas o ninguna → puedes probar un proyecto real en sus tres niveles y mantener la suite en equipo.
**Stack:** Python 3.12+ (verificado en 3.12 y 3.15) · pytest 9.2.0 · pytest-cov 7.1.0. Las librerías de los bloques 2 a 4 se fijan cuando se construyan.
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
| 4 · Calidad de la suite | Mantener una suite confiable en equipo: pruebas inestables, propiedades, mutation testing, TDD y CI | ⬜ `pending` |

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
| 2.1 | Qué cambia al integrar | 🎯 `core` | 💭 `concept` | Decidir qué parte de un sistema probar con lo real y cuál con un doble, y preparar y limpiar el entorno de cada prueba | ⬜ `pending` |
| 2.2 | Archivos y el sistema de archivos | 🎯 `core` | 🧩 `challenge` | Probar código que lee y escribe archivos y carpetas reales sin ensuciar tu máquina | ⬜ `pending` |
| 2.3 | Una base de datos real | 🎯 `core` | 🧩 `challenge` | Probar consultas contra SQLite, con datos de prueba y cada prueba aislada en su transacción | ⬜ `pending` |
| 2.4 | Un servicio HTTP | 🎯 `core` | 🧩 `challenge` | Probar un cliente HTTP contra un servidor de prueba y simular errores de red | ⬜ `pending` |
| 2.5 | Dependencias en contenedores | ➕ `elective` | 🔭 `exploration` | Levantar una base de datos de verdad en un contenedor solo durante las pruebas | ⬜ `pending` |
| 2.P | Proyecto: por definir | 🎯 `core` | 🏗️ `project` | Escribir la suite de integración de un servicio pequeño con base de datos y un servicio externo | ⬜ `pending` |

## Bloque 3 · Pruebas de aceptación
Probar el sistema completo como lo usa una persona: una línea de comandos y una API web.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 3.1 | Aceptación y criterios de aceptación | 🎯 `core` | 💭 `concept` | Escribir criterios de aceptación con la forma Dado / Cuando / Entonces y elegir qué recorridos merecen una prueba de punta a punta | ⬜ `pending` |
| 3.2 | Una línea de comandos de caja negra | 🎯 `core` | 🧩 `challenge` | Probar un programa de terminal como proceso aparte: argumentos, salida, errores y código de salida | ⬜ `pending` |
| 3.3 | Una API web de punta a punta | 🎯 `core` | 🧩 `challenge` | Probar una API web levantada de verdad, por sus rutas y respuestas | ⬜ `pending` |
| 3.4 | Pruebas en el navegador | ➕ `elective` | 🔭 `exploration` | Automatizar un recorrido en un navegador real y entender por qué estas pruebas son las más frágiles | ⬜ `pending` |
| 3.P | Proyecto: por definir | 🎯 `core` | 🏗️ `project` | Escribir la suite de aceptación de una aplicación a partir de su contrato | ⬜ `pending` |

## Bloque 4 · Calidad de la suite
Mantener una suite confiable en equipo.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 4.1 | Pruebas inestables | 🎯 `core` | 🔭 `exploration` | Reconocer, reproducir y arreglar una prueba que falla a veces | ⬜ `pending` |
| 4.2 | Desarrollo guiado por pruebas | 🎯 `core` | 🧩 `challenge` | Escribir la prueba antes que el código, en ciclos cortos de rojo, verde y refactorización | ⬜ `pending` |
| 4.3 | Pruebas basadas en propiedades | 🔬 `deep-dive` | 🧩 `challenge` | Describir reglas que se cumplen para cualquier dato y dejar que la herramienta busque el contraejemplo | ⬜ `pending` |
| 4.4 | Mutation testing | 🔬 `deep-dive` | 🔭 `exploration` | Medir con una herramienta qué bugs dejaría pasar tu suite, como la caza de mutantes de los labs | ⬜ `pending` |
| 4.5 | La suite en el CI | 🎯 `core` | 🔭 `exploration` | Correr la suite en cada cambio, en varias versiones de Python, con cobertura y sin pruebas lentas en el camino | ⬜ `pending` |
| 4.P | Proyecto: por definir | 🎯 `core` | 🏗️ `project` | Llevar una suite heredada a un estado confiable y automatizarla | ⬜ `pending` |

## Reglas de diseño
1. **La app más pequeña que hace visible el tema.** Cada lab trae su propio módulo pequeño; ninguno arrastra el dominio del anterior.
2. **Ninguna aplicación crece lab tras lab:** la integración ocurre en el proyecto del bloque.
3. **Cada tema tiene un único lab dueño**, que lo enseña. Los labs siguientes lo usan y enlazan a su dueño.
4. **Labs de testing al revés:** el código de producción ya está terminado; tú escribes las pruebas. Tus pruebas se validan con una **caza de mutantes**: deben pasar con el código real y fallar contra versiones con bugs sembrados. El proyecto de cada bloque funciona igual.
5. **Primero la idea, después pytest.** Cada lab presenta el concepto sin la herramienta y luego muestra cómo lo escribe pytest.
6. **Un bloque por nivel de la pirámide.** Las pruebas de integración y de aceptación tienen sus propios bloques; el bloque 1 se queda en las unitarias.

## Mapa de construcción
| ID | Dueño de | Se apoya en | Parte de |
|---|---|---|---|
| 1.1 | Qué es una prueba, los niveles de la pirámide, Arrange-Act-Assert, las propiedades de una buena prueba, la prueba que no puede fallar, qué es un mutante | — | Nada: solo `CONCEPT.md` |
| 1.2 | Descubrimiento de pruebas, `assert` y su introspección, `pytest.approx`, `pytest.raises`, leer un fallo, `-k` / `-x` / `-v`, la caza de mutantes | 1.1 | Módulo `grades.py` terminado |
| 1.3 | Clases de equivalencia, valores límite, un caso por razón de fallo, `parametrize` e `ids` | 1.2 | Módulo `passwords.py` terminado |
| 1.4 | Fixtures, fixtures que usan fixtures, `scope`, `conftest.py`, marcas propias, `-m`, `markers` en la configuración | 1.2, 1.3 | Módulo `cart.py` terminado |
| 1.5 | Inyección de dependencias, dummy / stub / fake / spy / mock, `tmp_path`, `create_autospec`, `monkeypatch` | 1.4 | Módulo `loans.py` terminado |
| 1.6 | Cobertura de líneas y de ramas, pytest-cov, los límites de la cobertura | 1.2, 1.3 | `demo/` terminado |
| 1.P | — | 1.1–1.6 | La aplicación `splitbill` terminada; la suite, desde cero |

## Notas para los siguientes labs
- El entorno es único (`.venv` en la raíz, `requirements.txt`). Cada variante tiene su `pyproject.toml` con `[tool.pytest]` y `pythonpath = ["."]`.
- La caza de mutantes vive en `tests/test_mutant_hunt.py` de cada challenge, con los mutantes en `tests/mutants/<id>/` y un `tests/conftest.py` que antepone el mutante a la ruta de importación según una variable de entorno. Los stubs del starter usan `pytest.skip("TODO …")`. Copia la caza del lab 1.2 y cambia el módulo y la variable (`GRADES_MUTANT` → la del nuevo lab); conserva `PYTHONIOENCODING=utf-8` (ver `docs/lessons.md`).
- Cada trampa del README se verifica en una copia limpia con un script que imprime cuántas pruebas corrieron; los mutantes se generan con un script que exige que cada reemplazo ocurra exactamente una vez.
- 1.4 revisa la organización con `tests/test_structure.py`. En `conftest.py`, la parte de la caza va arriba (antes de importar el módulo) y las fixtures abajo. Los stubs del starter no piden fixtures en su firma: una fixture inexistente es un *error* de preparación, no un `skip`.
- El proyecto 1.P se valida con una caza de mutantes de toda la aplicación (`acceptance/`), que corre la suite del aprendiz contra la referencia y contra cada mutante. El bloque 3 puede retomar `splitbill`: las pruebas de caja negra de su línea de comandos están en la historia de git (antes de la reconstrucción del bloque 1).
- **El bloque 1 está construido completo (1.1–1.6 y 1.P).** Queda esperar el feedback de quienes lo resuelvan; el CI corre el verificador en Python 3.12 y 3.15 y la caza del proyecto.
- Los bloques 2 a 4 pasan otra vez por el workflow `syllabus` antes de construirse: elegir librerías (por ejemplo, un servidor HTTP de prueba, testcontainers, Hypothesis, mutmut), fijar versiones y el dominio de cada proyecto.
