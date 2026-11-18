# 🧩 2.3 · Una base de datos real

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1,5–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · pytest 9.2 · SQLite (incluido en Python) |

## 🎯 Objetivos
- Escribir una fixture que prepara algo antes de la prueba y lo limpia después, con `yield`.
- Darle a cada prueba una base de datos SQLite nueva, en memoria, con su esquema creado.
- Cargar datos de prueba conocidos en la base antes de una consulta.
- Comprobar una transacción «todo o nada» mirando cómo queda la base después de un error.
- Elegir datos de prueba que pongan a prueba lo que solo una base real hace: restricciones, consultas y comillas.

## 💡 Por qué importa
Casi toda aplicación guarda sus datos en una base de datos, y buena parte de sus bugs vive en el SQL: una consulta que suma en vez de tomar el máximo, una regla que la base debía hacer cumplir y nadie escribió, un nombre con apóstrofo que rompe la consulta. Un doble de la base (lab [1.5](../../01-unit-tests/05-test-doubles/README.md)) no ejecuta SQL, así que no ve ninguno. Aquí pruebas el adaptador contra una base **real**, y aplicas lo que viste en el lab [2.1](../01-what-changes/README.md): cada prueba prepara su base y la limpia al terminar.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, en la carpeta **`starter/`** de este lab.

## 🧠 Conceptos

### Preparar y limpiar con `yield` (*yield fixture*)
Las fixtures del lab 1.4 terminaban con `return`: entregaban algo y ahí acababa su trabajo. Pero algunas cosas hay que cerrarlas o borrarlas **después** de la prueba: una conexión, un archivo abierto, un servidor. Si la fixture usa `yield` en lugar de `return`, pytest corre la fixture hasta el `yield`, le entrega ese valor a la prueba y, **cuando la prueba termina**, sigue con lo que viene después del `yield`:

```python
@pytest.fixture
def log_file(tmp_path):
    file = (tmp_path / "app.log").open("w", encoding="utf-8")  # preparación
    yield file                                                 # aquí corre la prueba
    file.close()                                               # limpieza
```

Lo de antes del `yield` es la preparación (*setup*) y lo de después, la limpieza (*teardown*). pytest corre la limpieza aunque la prueba falle, que es justo lo que pedía el lab 2.1.

### Una base de datos real, sin servidor (SQLite)
SQLite es una base de datos SQL completa que vive en un archivo, o en la memoria, y viene incluida en Python con el módulo `sqlite3`. No hay que instalar ni levantar nada. Con `":memory:"` como nombre, cada conexión crea una base nueva que desaparece al cerrarla:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE cities (name TEXT NOT NULL)")
conn.execute("INSERT INTO cities (name) VALUES (?)", ("Lima",))
conn.execute("SELECT name FROM cities").fetchall()   # [('Lima',)]
conn.close()
```

Los valores van como **parámetros** (el `?` y la tupla), nunca pegados al texto del SQL: el módulo se encarga de pasarlos a la base tal como son.

### Datos sembrados (*seed data*)
Para probar una consulta como «los tres mejores» hace falta una base con datos, y conocerlos de memoria para saber qué debe responder. La idea es una fixture que **siembra** datos fijos sobre la base vacía. Como en el lab 1.4, una fixture puede pedir otra:

```python
@pytest.fixture
def cities_db(db):
    for name in ["Lima", "Cusco", "Arequipa"]:
        db.execute("INSERT INTO cities (name) VALUES (?)", (name,))
    return db
```

La prueba que pide `cities_db` recibe la misma base de `db`, ya con tres ciudades, y la limpieza de `db` sigue corriendo al final.

### Transacciones: todo o nada (*transaction*)
Registrar un partido guarda el puntaje de varios jugadores. Si el segundo puntaje es inválido, ¿qué pasa con el primero? Una **transacción** agrupa varios cambios para que la base los aplique **todos o ninguno**: al final se confirman (*commit*) o se deshacen (*rollback*). En `sqlite3`, `with conn:` abre ese bloque: si termina bien, confirma; si sale con una excepción, deshace y deja pasar la excepción.

```python
with conn:                                   # todo lo de este bloque, o nada
    conn.execute("INSERT INTO cities (name) VALUES (?)", ("Piura",))
    conn.execute("INSERT INTO cities (name) VALUES (?)", ("Tacna",))
```

## 📚 Documentación
- [pytest · Teardown/Cleanup (aka Fixture finalization)](https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization)
- [Python · `sqlite3`: el tutorial](https://docs.python.org/3/library/sqlite3.html#tutorial)
- [Python · `sqlite3`: cómo usar parámetros en las consultas](https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries)
- [Python · `sqlite3`: la conexión como gestor de contexto (`with conn:`)](https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager)

## 🧭 Escenario

### El código
[`scores.py`](starter/scores.py) ya funciona: la tabla de puntajes de un juego. **No lo cambies.** Cada función recibe una conexión abierta, así que la prueba puede darle una base propia.

| Función | Promete |
|---|---|
| `create_schema(conn)` | Crea la tabla `scores` (jugador y puntos); la base rechaza los puntos negativos |
| `add_score(conn, player, points)` | Guarda un puntaje. Uno negativo → `sqlite3.IntegrityError` |
| `history(conn, player)` | Todos los puntajes de un jugador, en el orden en que se guardaron |
| `top(conn, n=3)` | Los `n` jugadores con el mejor puntaje individual, de mayor a menor; los empates, en orden alfabético |
| `record_match(conn, results)` | Guarda el puntaje de cada jugador de un partido (`{"ana": 10, ...}`), todos o ninguno |

[`tests/conftest.py`](starter/tests/conftest.py) ya trae la parte de la caza; tus fixtures van debajo. Tus pruebas van en [`tests/test_scores.py`](starter/tests/test_scores.py).

### Cómo se revisa tu trabajo
La caza de mutantes del [lab 1.2](../../01-unit-tests/02-first-tests/README.md):

| Mutante | Bug sembrado | Lo mata la tarea |
|---|---|---|
| `m1-history-newest-first` | `history` devuelve los puntajes del más nuevo al más viejo | 1 |
| `m2-no-points-check` | La tabla no rechaza los puntos negativos | 1 |
| `m3-total-not-best` | `top` suma los puntajes de cada jugador en vez de tomar el mejor | 2 |
| `m4-no-limit` | `top` devuelve todos los jugadores, no solo `n` | 2 |
| `m5-sql-by-hand` | `history` pega el nombre del jugador dentro del texto del SQL | 2 |
| `m6-not-atomic` | `record_match` guarda cada puntaje en su propia transacción | 3 |

## ✅ Tareas

Corre todo con este comando, igual en PowerShell o Bash:

```bash
python -m pytest
```

### Tarea 1 · Una base nueva para cada prueba
**Meta:** una fixture que crea la base, se la da a la prueba y la cierra al final. **La validan:** `[m1-history-newest-first]` y `[m2-no-points-check]`.

- [ ] En `conftest.py`, escribe la fixture `db`: conecta a `":memory:"`, crea el esquema con `create_schema`, entrega la conexión con `yield` y ciérrala después.
- [ ] En `test_scores_are_saved_in_order(db)`: guarda dos puntajes de `"ana"`, 10 y después 4, y comprueba lo que devuelve `history`.
- [ ] En `test_negative_points_are_rejected(db)`: guardar `-1` lanza `sqlite3.IntegrityError` (`pytest.raises`, lab 1.2).

🔮 **Predict first:** cuando termines la tarea 3, prueba `db` con `scope="module"` (lab 1.4): todas las pruebas del archivo comparten una sola base. ¿Qué pruebas fallan, y por qué? Después, vuelve a dejarla sin `scope`.

### Tarea 2 · Datos sembrados en la base
**Meta:** probar las consultas con datos que conoces. **La validan:** `[m3-total-not-best]`, `[m4-no-limit]` y `[m5-sql-by-hand]`.

- [ ] En `conftest.py`, escribe la fixture `seeded_db`: pide `db` y guarda estos cinco puntajes, en este orden, con `add_score`:

  | Jugador | Puntos |
  |---|---|
  | `beto` | 7 |
  | `ana` | 5 |
  | `ana` | 9 |
  | `carla` | 7 |
  | `dani` | 2 |

- [ ] En `test_top_shows_the_best_score_of_each_player(seeded_db)`: comprueba la lista completa que devuelve `top(seeded_db)`. Calcúlala tú a partir de la tabla, sin correr el código.
- [ ] En `test_a_name_with_an_apostrophe(db)`: guarda un puntaje de `"O'Higgins"` y léelo con `history`.

🔮 **Predict first:** con `"O'Higgins"`, ¿`m5-sql-by-hand` falla en tu `assert` o antes, y con qué error? ¿Y si usaras un nombre común, como `"ohiggins"`?

### Tarea 3 · Todo o nada
**Meta:** comprobar que un partido con un puntaje inválido no deja la base a medias. **La valida:** `[m6-not-atomic]`.

- [ ] En `test_a_failed_match_saves_nothing(db)`: `record_match(db, {"ana": 10, "beto": -1})` lanza `sqlite3.IntegrityError`, y después la base no tiene ningún puntaje (`top(db)` devuelve una lista vacía).

🔮 **Predict first:** ¿qué excepción lanza `m6-not-atomic` con este partido, y qué queda en la base después? ¿Basta con comprobar la excepción?

**Criterio de éxito:** `python -m pytest` dentro de `starter/` termina en verde: 12 pruebas pasan, ninguna se salta.

## 🔍 Command dissection
| Código | Qué hace |
|---|---|
| `sqlite3.connect(":memory:")` | Abre una base nueva en memoria; desaparece al cerrar la conexión |
| `conn.execute(sql, (valor,))` | Ejecuta una sentencia; los `?` del SQL se reemplazan por los valores de la tupla |
| `cursor.fetchall()` | Todas las filas del resultado, como una lista de tuplas (`execute` devuelve un *cursor*, el objeto que recorre esas filas) |
| `with conn:` | Una transacción: confirma al salir bien; deshace si sale una excepción |
| `conn.close()` | Cierra la conexión; con `:memory:`, la base se borra |

## 💼 En proyectos reales
- **Nunca uses la base de producción para probar.** Las pruebas crean, cambian y borran datos. Usa una base propia de las pruebas, creada y destruida por ellas.
- **Pegar valores dentro del SQL no es solo un bug: es un agujero de seguridad.** Si el texto viene de un usuario, puede cerrar la comilla y agregar su propio SQL (*SQL injection*). Los parámetros lo evitan.
- **«Deshacer al terminar» tiene una trampa.** Con una base cara de crear, muchos equipos comparten una conexión y hacen `conn.rollback()` en la limpieza de cada prueba. Pero si el código bajo prueba confirma por su cuenta (como `add_score`, con `with conn:`), el rollback ya no deshace nada: se comprobó con este mismo esquema, y la fila confirmada seguía ahí. Las herramientas grandes, como SQLAlchemy o Django, lo resuelven con transacciones dentro de otra transacción (*savepoints*).
- **SQLite no es tu base de producción.** Si en producción usas PostgreSQL o MySQL, algunas consultas se comportan distinto. El electivo [2.5](../05-containers/README.md) lo muestra.

## 🚀 Reto extra
Agrega a `scores.py` (en tu rama, no en el lab) una función `rename_player(conn, old, new)` que cambie el nombre en todos sus puntajes dentro de una transacción. Escribe primero sus pruebas, incluida una que demuestre que un error a mitad de camino no deja nombres mezclados.

## 🆘 Pistas
<details><summary>Pista 1 · dirección</summary>

La fixture `db` tiene cuatro líneas: conectar, crear el esquema, `yield` y cerrar. `seeded_db` pide `db`, llama a `add_score` cinco veces y devuelve `db`. Para `top`, toma el mejor puntaje de cada jugador y ordénalos; mira bien los empates.
</details>

<details><summary>Pista 2 · más concreta</summary>

```python
@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    yield conn
    conn.close()
```

`top(seeded_db)` debe ser `[("ana", 9), ("beto", 7), ("carla", 7)]`.
</details>

## ✔️ Respuestas verificadas
<details><summary>Ábrelas solo después de terminar las tareas</summary>

Se ejecutó con pytest 9.2.0; el CI verifica cada lab en Python 3.12 y 3.15.

**Tarea 1.** Con `scope="module"` fallan dos pruebas: `test_top_shows_the_best_score_of_each_player` y `test_a_failed_match_saves_nothing`. La base es una sola para todo el archivo, así que los puntajes de `"ana"` de la primera prueba (10 y 4) siguen ahí cuando `seeded_db` siembra los suyos, y el mejor de ana pasa a ser 10:

```text
E       AssertionError: assert [('ana', 10),... ('carla', 7)] == [('ana', 9), ... ('carla', 7)]
```

Y la última prueba encuentra la base llena, no vacía. Las pruebas que solo guardan y leen sus propios datos siguen pasando: la fuga solo se ve cuando una prueba depende de **toda** la base. Con la base nueva por prueba, ninguna ve lo de otra.

**Tarea 2.** `m5-sql-by-hand` falla **antes** del `assert`, dentro de `history`: la comilla del nombre cierra el texto del SQL antes de tiempo, y la base rechaza la consulta. Con `"ohiggins"`, en cambio, el SQL armado a mano es válido y `m5` sobrevive:

```text
E       sqlite3.OperationalError: near "Higgins": syntax error
```

Un doble no ejecuta SQL, así que nunca lo vería: este bug solo existe entre tu código y la base. Ojo también con `top`: tu tabla tiene dos empates a propósito (beto y carla con 7), y ana tiene dos puntajes cuya suma (14) supera a todos. Esos datos son los que matan a `m3` y a `m4` con una sola prueba.

**Tarea 3.** `m6-not-atomic` lanza la misma `IntegrityError` al llegar al puntaje de beto, pero el de ana ya quedó confirmado en su propia transacción. Si solo compruebas la excepción, sobrevive; mirar la base después lo delata:

```text
E       AssertionError: assert [('ana', 10)] == []
```

Comprobar la excepción dice que el error se detectó; comprobar el estado dice que **no dejó nada a medias**. Es la pregunta que vuelve en el proyecto del bloque.
</details>

## 🎤 Autoevaluación
1. ¿Qué diferencia hay entre una fixture con `return` y una con `yield`? ¿Cuándo necesitas la segunda?
2. ¿Por qué una base `:memory:` nueva por prueba es una forma de «uno nuevo por prueba» (lab 2.1), y qué costo tendría con una base de un servidor?
3. Explica qué es una transacción con un ejemplo de tu vida diaria, y qué significa que algo sea «todo o nada».
4. ¿Por qué `f"... WHERE player = '{player}'"` es un bug y un riesgo de seguridad a la vez? ¿Cómo se escribe bien?
5. Tus pruebas de base de datos pasan solas y fallan cuando corres toda la suite. ¿Qué revisarías primero?

La solución completa está en [`solution/`](solution/).

**Siguiente:** [2.4 · Un servicio HTTP](../04-http-service/README.md)
