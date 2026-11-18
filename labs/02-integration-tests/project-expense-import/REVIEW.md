# 🔍 Revisión guiada · Importar gastos

Cómo leer la suite de referencia, por qué es como es, y cómo comprobar que cada prueba sirve de verdad.

## Orden de lectura
1. [`tests/conftest.py`](reference/tests/conftest.py): **lo real de cada prueba.** Una base `:memory:` nueva con `yield`, un cliente apuntado al servidor de prueba, y dos fixtures que devuelven una función: `serve_rate` registra un tipo de cambio y `csv_file` escribe un CSV en `tmp_path`.
2. [`src/expenses/rates.py`](reference/src/expenses/rates.py) y [`tests/test_rates.py`](reference/tests/test_rates.py): el adaptador HTTP contra el servidor de prueba, con sus cuatro fallas (404, 500, lento y caído). Es el lab 2.4 aplicado a otro servicio.
3. [`src/expenses/store.py`](reference/src/expenses/store.py) y [`tests/test_store.py`](reference/tests/test_store.py): el adaptador de la base. Tres pruebas, cada una sobre algo que solo una base real muestra: los `Decimal` que vuelven exactos, la suma al céntimo y lo que queda en disco al cerrar.
4. [`src/expenses/importer.py`](reference/src/expenses/importer.py) y [`tests/test_importer.py`](reference/tests/test_importer.py): **la respuesta a la pregunta del dominio.** El importador lee y valida todo, pide los tipos de cambio y solo al final guarda, en una transacción. Las pruebas lo atacan por cada lado: una línea mala, un servicio que falla, un reintento y los duplicados.

## Decisiones y por qué
| Decisión | Por qué | Aprendido en |
|---|---|---|
| Ningún mock: archivo, base y servidor son reales | Los 13 mutantes son bugs de encaje (SQL, transacciones, HTTP, bytes). Un doble de cualquiera de las tres piezas habría dejado vivo al menos a uno | 2.1 |
| El CSV principal vive en `tests/data/` y los de cada prueba se escriben en `tmp_path` | El de `tests/data/` es el ejemplo realista y revisado (tildes, dos monedas, un medio céntimo); los de `tmp_path` muestran un solo caso cada uno, a la vista dentro de la prueba | 2.2 |
| Una base `:memory:` nueva por prueba, con `yield` | Ninguna prueba ve los gastos de otra, y la limpieza corre aunque la prueba falle | 2.3 |
| Después de cada error, `assert store.expenses() == []` | La excepción dice que el error se detectó; la base vacía dice que no quedó nada a medias. `m05` y `m06` lanzan la misma excepción que la referencia | 2.3 |
| Una prueba con una base en un archivo, cerrada y abierta de nuevo | Con `:memory:` y una sola conexión, un gasto sin confirmar se ve igual que uno confirmado (`m13`) | [BRIEF](BRIEF.md#cerrar-no-es-confirmar) |
| `httpserver_listen_address` en `127.0.0.1` | Con `localhost`, en Windows cada petición esperaba medio segundo antes de usar IPv4 | 2.4 |
| `len(httpserver.log) == 1` con dos líneas en USD | «Un tipo de cambio por moneda» es una promesa sobre lo que el cliente **manda**, y solo el servidor puede contarlo | [BRIEF](BRIEF.md#contar-las-peticiones-que-recibió-el-servidor-httpserverlog) |
| `expect_oneshot_request` con un 503 y después la respuesta buena | Es la forma más corta de «falla una vez y después funciona», que es lo que pregunta el reintento | [BRIEF](BRIEF.md#una-respuesta-que-vale-una-sola-vez-expect_oneshot_request) |

## Trampas encontradas al construirla
- **Una prueba con `with conn:` se miente a sí misma.** La primera versión de `test_a_saved_import_survives_closing_the_database` abría la conexión con `with sqlite3.connect(path) as conn:`. Pero `with` sobre una conexión **confirma** al salir: la prueba hace el `commit` que debía hacer `save_import`. Con esa versión, `m13` sobrevive (se comprobó). Ahora la prueba cierra con `conn.close()`, que no confirma nada.
- **Un mutante roto no es un mutante muerto.** Al generar `m05`, un `\n` mal escapado dejó el archivo con un error de sintaxis. La caza lo dio por muerto (la suite «falló»), pero fallaba por no poder importar el paquete. Antes de correr la caza, cada mutante se compila con `ast.parse`.
- **`SUM` en SQLite convierte el texto a `float`.** `amount_pen` se guarda como texto para no perder céntimos, pero `SUM(amount_pen)` lo suma como número de punto flotante: 10,10 + 20,20 da `30.299999999999997`. La referencia suma en Python con `Decimal`; los datos de `test_the_total_is_exact_to_the_cent` se eligieron para que el error se vea.
- **`round()` de Python no redondea como el dominio.** Redondea los medios al par (`round(4.625, 2)` da `4.62`), igual que `ROUND_HALF_EVEN`. El dominio pide medio céntimo hacia arriba, y solo un dato que termina justo en medio céntimo (1,25 × 3,70) separa las dos reglas.

## 🔨 Rómpelo tú
Esta tabla dice qué pruebas de la referencia matan a cada mutante. Se midió corriendo la suite contra cada mutante (Python 3.12, pytest 9.2.0, en Windows); las cifras son «pruebas que fallan / pruebas que corrieron».

| Mutante | Falla | Pruebas que lo matan | Fallo real |
|---|---|---|---|
| `m01-rounds-half-even` | 1/16 | Solo `test_imports_every_row_converted_to_soles` | `... amount_pen=Decimal('4.62')) != Expense(... amount_pen=Decimal('4.63'))` |
| `m02-request-per-row` | 1/16 | Solo `test_asks_for_each_currency_only_once` | `assert 2 == 1` |
| `m03-asks-rate-for-pen` | 6/16 | Las seis pruebas del importador que llegan a pedir tipos de cambio con alguna línea en PEN, como `test_soles_need_no_rate` | `expenses.rates.RatesUnavailable: the rates service answered 500` |
| `m04-unknown-currency-is-unavailable` | 1/16 | Solo `test_an_unknown_currency_is_not_found` | `expenses.rates.RatesUnavailable: the rates service answered 404` |
| `m05-saves-as-it-reads` | 3/16 | `test_an_invalid_line_saves_nothing_and_says_which`, `test_a_failed_rate_saves_nothing` y `test_a_failed_import_can_be_tried_again` | `assert [Expense(spen...al('118.40'))] == []` |
| `m06-saves-as-it-converts` | 2/16 | `test_a_failed_rate_saves_nothing` y `test_a_failed_import_can_be_tried_again` | `assert [Expense(spen...al('118.40'))] == []` |
| `m07-duplicate-by-name` | 1/16 | Solo `test_a_copy_with_another_name_is_a_duplicate` | `Failed: DID NOT RAISE DuplicateImport` |
| `m08-import-recorded-first` | 1/16 | Solo `test_a_failed_import_can_be_tried_again` | `expenses.importer.DuplicateImport: trip.csv was already imported` |
| `m09-total-in-sql` | 1/16 | Solo `test_the_total_is_exact_to_the_cent` | `assert Decimal('30.299999999999997') == Decimal('30.30')` |
| `m10-no-timeout` | 1/16 | Solo `test_a_slow_service_means_unavailable` | `Failed: DID NOT RAISE RatesUnavailable` |
| `m11-line-number-off` | 1/16 | Solo `test_an_invalid_line_saves_nothing_and_says_which` | `Actual message: "line 2: invalid amount '12.345'"` |
| `m12-reads-latin-1` | 1/16 | Solo `test_imports_every_row_converted_to_soles` | `description='CafÃ© y pan'` frente a `description='Café y pan'` |
| `m13-never-commits` | 1/16 | Solo `test_a_saved_import_survives_closing_the_database` | `assert [] == [Expense(spen...mal('18.50'))]` |

**El ejercicio:** borra (en tu rama) una de las pruebas que aparecen con «Solo» y vuelve a pasar la caza. El mutante de esa fila sobrevive. Después borra `test_soles_need_no_rate`: `m03` sigue muriendo, porque otras cinco pruebas lo cubren.

**Qué enseña la tabla:**
- **Casi todo mutante muere con una sola prueba.** En una suite de integración cada prueba mira un borde distinto, y por eso pocas se cubren entre sí: 10 de 13 filas dicen «Solo».
- **`m05` y `m06` son el mismo error con distinto disparador.** Uno guarda antes de validar el resto; el otro, antes de tener todos los tipos de cambio. La prueba de la línea mala solo ve al primero; la del servicio que falla, a los dos. Por eso la pregunta del dominio necesita las dos pruebas.
- **`m08` es el bug más fácil de no ver.** Todas las pruebas de «no guarda nada» pasan con él: la base no tiene gastos. Lo que quedó a medias es la marca de «ya importado», y solo un reintento lo muestra.

## Lo que falta a propósito
- **Un servicio de tipos de cambio real.** La suite confía en el contrato del BRIEF. Un equipo agregaría pocas pruebas, aparte y con una marca, contra el entorno de prueba del proveedor (lab 2.4).
- **PostgreSQL.** La aplicación solo conoce SQLite. Con otra base, `total_pen` y las transacciones merecerían correr también contra ella (electivo 2.5).
- **Archivos enormes y concurrencia:** dos importaciones del mismo archivo a la vez no están cubiertas.

## Preguntas para desafiar el diseño
1. ¿Por qué `test_a_failed_rate_saves_nothing` pone la línea en USD **antes** que la de EUR? ¿Qué mutantes dejaría de atrapar esa prueba si las invirtieras?
2. `m03` muere con seis pruebas. ¿Cuál dejarías si tuvieras que quedarte con una sola, y por qué esa?
3. Si el equipo decide guardar los gastos válidos y reportar solo las líneas malas, ¿qué pruebas de la referencia tendrían que cambiar? ¿Qué pregunta del dominio la reemplazaría?
4. ¿Qué ganarías y qué perderías si `store` usara una base en un archivo de `tmp_path` en todas las pruebas, y no solo en una?
5. La huella del archivo es el SHA-256 de su contenido. ¿Qué pasa si alguien exporta la misma planilla dos veces y Excel cambia un espacio al final? ¿Es un bug de la aplicación o una regla que el BRIEF debería decir?
