# 🔭 2.5 · Dependencias en contenedores

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–1,5 h | 🔭 `exploration` | ➕ `elective` | Python 3.12+ · pytest 9.2 · testcontainers 4.15 · psycopg 3.3 · PostgreSQL 18.7 |

> [!IMPORTANT]
> Este lab es **electivo** y necesita **Docker** (Docker Desktop en Windows y macOS) encendido. Si no lo tienes, puedes saltarlo: el resto del camino no lo usa. Las pruebas de PostgreSQL se saltan solas cuando Docker no está.

## 🎯 Objetivos
- Explicar qué es un contenedor y por qué sirve para tener la base de datos de producción en una prueba.
- Levantar PostgreSQL en un contenedor solo durante las pruebas, con testcontainers.
- Correr las mismas pruebas contra dos bases con una fixture parametrizada.
- Reconocer dos diferencias entre SQLite y PostgreSQL que una suite solo con SQLite no ve.
- Hacer que las pruebas que necesitan Docker se salten solas cuando no está.

## 💡 Por qué importa
En el lab [2.3](../03-real-database/README.md) probaste contra SQLite: rápido, sin instalar nada. Pero en producción casi nunca corre SQLite, sino PostgreSQL, MySQL u otra base con un servidor, y cada una tiene sus reglas. Una consulta que pasa en SQLite puede fallar en producción. La salida es probar contra **la misma base** que producción, sin instalarla en tu máquina ni dejar nada atrás: un contenedor que nace con la prueba y desaparece al terminar.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, en la carpeta **`demo/`** de este lab. Antes del primer experimento, instala las dos librerías de este lab (no están en el `requirements.txt` de la raíz). Igual en PowerShell o Bash:

```bash
python -m pip install -r requirements.txt
```

## 🧠 Conceptos

### Contenedor e imagen (*container*, *image*)
Para tener PostgreSQL en tu máquina tendrías que instalarlo, configurarlo y acordarte de limpiar lo que tus pruebas dejen. Un **contenedor** es un programa que corre aislado del resto de tu sistema, con sus propios archivos, y que se borra entero cuando ya no lo necesitas. Nace de una **imagen**: un paquete con el programa y todo lo que necesita, en una versión fija. `postgres:18.7-alpine` es la imagen oficial de PostgreSQL 18.7. Docker descarga la imagen una vez, y cada contenedor que crea a partir de ella arranca limpio.

El contenedor escucha en su propio puerto (5432, en PostgreSQL), y Docker lo conecta con un puerto libre de tu máquina para que tus pruebas lleguen a él.

### Contenedores desde las pruebas (testcontainers)
`testcontainers` crea el contenedor desde el código de la prueba, espera a que la base esté lista para recibir conexiones y te da su dirección. Al salir del `with`, lo borra:

```python
from testcontainers.community.postgres import PostgresContainer

with PostgresContainer("postgres:18.7-alpine", driver=None) as container:
    url = container.get_connection_url()   # postgresql://test:test@localhost:55012/test
    ...                                    # conectarse y probar
# aquí el contenedor ya no existe
```

Arrancar un contenedor cuesta segundos, así que en la demo vive en una fixture con `scope="session"` (lab [1.4](../../01-unit-tests/04-organize-suite/README.md)): uno solo para toda la corrida. Para aislar cada prueba sin crear otro contenedor, la demo usa la estrategia «deshacer al terminar» del lab [2.1](../01-what-changes/README.md): `Contacts` nunca confirma, así que el `rollback()` de la limpieza borra la tabla y sus filas.

### Una fixture, dos bases (*parametrized fixture*)
En el lab [1.3](../../01-unit-tests/03-test-case-design/README.md) parametrizaste una prueba con una tabla de casos. Una **fixture** también se puede parametrizar: con `params=`, cada prueba que la pide corre una vez por cada valor, y la fixture lee el valor actual en `request.param`:

```python
@pytest.fixture(params=["sqlite", "postgres"])
def contacts(request):
    if request.param == "sqlite":
        ...   # una base SQLite en memoria
    else:
        ...   # una conexión al contenedor
```

pytest muestra el valor en el nombre de la prueba: `test_search_ignores_case[sqlite]` y `test_search_ignores_case[postgres]`.

### Saltar lo que no se puede correr
Si falta Docker o una librería, la prueba no debe fallar: no hay un bug que reportar. `pytest.importorskip("psycopg")` importa una librería o salta la prueba si no está instalada, y `pytest.skip("…")` dentro de una fixture salta todas las pruebas que la piden, con su motivo.

## 📚 Documentación
- [Testcontainers for Python · PostgreSQL](https://testcontainers-python.readthedocs.io/en/latest/modules/postgres/README.html)
- [pytest · Parametrizing fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html#parametrizing-fixtures)
- [pytest · Skipping on a missing import dependency](https://docs.pytest.org/en/stable/how-to/skipping.html#skipping-on-a-missing-import-dependency)
- [SQLite · Datatypes In SQLite](https://www.sqlite.org/datatype3.html) y [el operador LIKE](https://www.sqlite.org/lang_expr.html#the_like_glob_regexp_match_and_extract_operators)
- [PostgreSQL · Pattern Matching (`LIKE`, `ILIKE`)](https://www.postgresql.org/docs/18/functions-matching.html)

## 🧭 Escenario
La demo está terminada. [`contacts.py`](demo/contacts.py) guarda contactos (nombre y edad) y los busca por parte del nombre, sin distinguir mayúsculas. Recibe una conexión de cualquiera de las dos bases y el marcador de parámetros de su *driver* (la librería que habla con esa base): `?` en `sqlite3`, `%s` en `psycopg`.

| Archivo | Qué hay |
|---|---|
| [`conftest.py`](demo/conftest.py) | La fixture `postgres_url` (el contenedor, una vez por corrida) y la fixture parametrizada `contacts` |
| [`tests/test_contacts.py`](demo/tests/test_contacts.py) | Tres pruebas que corren en las dos bases: seis en total |
| [`experiments/test_types.py`](demo/experiments/test_types.py) | La prueba del experimento 3; no se corre por defecto |

## 🧪 Experimentos

### Experimento 1 · Lo que cuesta un contenedor
Corre las pruebas dos veces, con los tiempos (lab [2.4](../04-http-service/README.md)). Igual en PowerShell o Bash:

```bash
python -m pytest --durations=3
```

🔮 **Predict first:** ¿qué fase va a ser la más lenta, y cuánto va a tardar? ¿Cambia en la segunda corrida?

<details><summary>👀 Qué deberías ver</summary>

```text
19.96s setup    tests/test_contacts.py::test_search_finds_part_of_a_name[postgres]
0.49s teardown tests/test_contacts.py::test_each_test_starts_empty[postgres]
...
6 passed in 20.52s
```

La preparación de la **primera** prueba de PostgreSQL: ahí arranca el contenedor. La primera vez incluye la descarga de la imagen (unos 300 MB en disco), y por eso tardó 20 s. En la segunda corrida la imagen ya está, y la misma fase bajó a 3,7 s: es lo que tarda PostgreSQL en arrancar y aceptar conexiones. Las demás pruebas de PostgreSQL tardan centésimas, porque con `scope="session"` comparten el contenedor. La limpieza de la última es la que lo apaga.
</details>

### Experimento 2 · Mayúsculas y minúsculas
Abre [`contacts.py`](demo/contacts.py) y, en `search`, cambia `lower(name) LIKE lower({self.p})` por `name LIKE {self.p}`. Corre otra vez el comando del experimento 1.

🔮 **Predict first:** sin los `lower`, ¿falla también `test_search_finds_part_of_a_name`, que busca `"Torres"`? ¿Y `test_search_ignores_case`, que busca `"ana"`: en una base, en las dos o en ninguna?

<details><summary>👀 Qué deberías ver</summary>

```text
E       AssertionError: assert [] == ['Ana Torres']
FAILED tests/test_contacts.py::test_search_ignores_case[postgres] - Assertion...
1 failed, 5 passed
```

`test_search_finds_part_of_a_name` sigue pasando: `"Torres"` ya viene con su mayúscula. `test_search_ignores_case` falla solo en PostgreSQL. En SQLite, `LIKE` no distingue mayúsculas de las letras ASCII (las del inglés, sin tildes ni eñes) ; sí distingue `Ñ` de `ñ`: `'Ñ' LIKE 'ñ'` da `0`; en PostgreSQL `LIKE` las distingue siempre, y para ignorarlas existe `ILIKE`. Una suite solo con SQLite habría pasado, y la búsqueda habría fallado en producción.

Deja el archivo como estaba. Igual en PowerShell o Bash:

```bash
git restore contacts.py
```
</details>

### Experimento 3 · Un texto en una columna de números
La tabla declara `age INTEGER NOT NULL`. La prueba del experimento intenta guardar la edad `"veinte"` y espera un error. Igual en PowerShell o Bash:

```bash
python -m pytest experiments/test_types.py
```

🔮 **Predict first:** con el texto `"veinte"` en una columna de números, cada base puede rechazarlo, convertirlo en un número o guardarlo como texto. ¿Qué hace cada una?

<details><summary>👀 Qué deberías ver</summary>

```text
FAILED experiments/test_types.py::test_age_must_be_a_number[sqlite] - Failed: DID NOT RAISE Exception
1 failed, 1 passed
```

PostgreSQL lo rechaza (`psycopg.errors.InvalidTextRepresentation: invalid input syntax for type integer: "veinte"`). SQLite lo **guarda**: en SQLite el tipo de una columna es una preferencia (*type affinity*), no una regla, y `SELECT typeof(age)` devuelve `text`. Las tablas `STRICT` de SQLite sí hacen cumplir el tipo, pero hay que pedirlas.
</details>

### Experimento 4 · Sin Docker
No hace falta apagar Docker: basta con apuntar a una dirección donde no hay ninguno.

PowerShell:

```powershell
$env:DOCKER_HOST = "tcp://127.0.0.1:1"
python -m pytest -rs
Remove-Item Env:DOCKER_HOST
```

Bash:

```bash
DOCKER_HOST=tcp://127.0.0.1:1 python -m pytest -rs
```

🔮 **Predict first:** las seis pruebas piden la misma fixture, `contacts`. ¿Por qué las de PostgreSQL se pueden saltar sin que se salten también las de SQLite? Busca la respuesta en [`conftest.py`](demo/conftest.py) antes de correrlo.

<details><summary>👀 Qué deberías ver</summary>

```text
SKIPPED [1] tests\test_contacts.py:4: Docker is not running
SKIPPED [1] tests\test_contacts.py:11: Docker is not running
SKIPPED [1] tests\test_contacts.py:17: Docker is not running
3 passed, 3 skipped
```

Las tres de SQLite pasan y las tres de PostgreSQL se saltan, con el motivo que escribió la fixture. `contacts` solo pide `postgres_url` dentro de la rama de PostgreSQL, con `request.getfixturevalue("postgres_url")`: una fixture se puede pedir así, desde el código, en vez de en la firma. Las pruebas de SQLite nunca llegan a pedirla, y por eso su `pytest.skip` no las alcanza. Ninguna falla: no tener Docker no es un bug de tu código. `-rs` es la opción que muestra los motivos de los saltos al final.
</details>

## 💼 En proyectos reales
- **Prueba contra la base que usa producción**, con la misma versión mayor. Las pruebas rápidas de la lógica pueden seguir con dobles o SQLite; las del adaptador de la base, contra la real.
- **Fija la etiqueta de la imagen** (`postgres:18.7-alpine`, no `postgres:latest`). Con `latest`, la suite cambia de versión de base el día que alguien publica una nueva, sin que nadie lo decida.
- **En el CI, Docker suele estar disponible** (los runners de Linux de GitHub Actions lo traen), así que las pruebas que aquí se saltan sin Docker sí corren allí.
- **Testcontainers tiene módulos para muchos servicios**: MySQL, Redis, Kafka, MongoDB, servidores de correo de prueba. La idea es la misma de este lab.

## 🧹 Limpieza
`testcontainers` borra el contenedor al final de cada corrida. Para comprobar que no quedó ninguno, igual en PowerShell o Bash:

```bash
docker ps -a --filter label=org.testcontainers=true
```

La lista debe salir vacía. Las imágenes sí quedan en tu máquina, para que la próxima corrida no las descargue. Si no las usas para otra cosa, bórralas:

```bash
docker image rm postgres:18.7-alpine testcontainers/ryuk:0.8.1
```

`testcontainers/ryuk` es el pequeño contenedor que `testcontainers` usa para borrar los demás aunque pytest se cierre a la mitad.

## 🆘 Pistas
<details><summary>Las pruebas de PostgreSQL dan <code>DockerException: Invalid bind address format</code></summary>

Si alguna vez usaste Testcontainers Desktop o Testcontainers para Java, puede existir un archivo `.testcontainers.properties` en tu carpeta de usuario con líneas como `tc.host=tcp\://127.0.0.1\:63573`. `testcontainers` para Python usa ese `tc.host` antes que tu Docker, y no entiende las barras de ese formato. Las tres pruebas de PostgreSQL terminan con *error* (no se saltan, porque Docker sí responde):

```text
E   docker.errors.DockerException: Invalid bind address format: port is required: tcp\://127.0.0.1\:63573
```

Si ya no usas esas herramientas, comenta las líneas `docker.host` y `tc.host` con `#`.
</details>

<details><summary>Las pruebas de PostgreSQL dicen «Docker is not running», pero Docker está encendido</summary>

En Windows y macOS, Docker Desktop tiene que estar abierto y con su motor iniciado. Comprueba con `docker version`: debe mostrar una sección `Server`.
</details>

<details><summary>La primera corrida se queda quieta un buen rato</summary>

Está descargando la imagen de PostgreSQL. Puedes descargarla antes, con su progreso a la vista: `docker pull postgres:18.7-alpine`.
</details>

## 🎤 Autoevaluación
1. ¿Qué diferencia hay entre una imagen y un contenedor?
2. ¿Por qué el contenedor vive en una fixture de `scope="session"` y no en una por prueba? ¿Cómo se aíslan entonces las pruebas?
3. Da dos ejemplos de algo que pasa en SQLite y falla en PostgreSQL. ¿Qué haría tu equipo para no enterarse en producción?
4. ¿Por qué una prueba que necesita Docker debe saltarse, y no fallar, cuando Docker no está?
5. ¿Qué gana y qué pierde una suite que prueba el adaptador de la base contra un contenedor, en lugar de contra SQLite?

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué sigue sin estar claro?

**Siguiente:** [Proyecto 2.P · Importar gastos](../project-expense-import/README.md)
