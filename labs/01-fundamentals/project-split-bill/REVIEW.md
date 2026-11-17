# 🔍 Revisión guiada · Dividir la cuenta

Cómo leer la implementación de referencia, por qué es como es, y cómo comprobar que sus pruebas sirven de verdad.

## Orden de lectura
1. [`src/splitbill/money.py`](reference/src/splitbill/money.py): **la respuesta a la pregunta del dominio.** `split` reparte en céntimos enteros, así que la suma cierra por construcción, no por redondeo.
2. [`src/splitbill/ledger.py`](reference/src/splitbill/ledger.py): leer el CSV con números de línea, calcular saldos y transferencias. Funciones puras: entran datos y salen datos.
3. [`src/splitbill/cli.py`](reference/src/splitbill/cli.py): el borde con el mundo (archivo, salida, códigos). Es la única capa que sabe de archivos y de `print`.
4. [`tests/`](reference/tests/): unitarias por capa. Después, [`acceptance/`](acceptance/): el contrato visto desde afuera.

## Decisiones y por qué
| Decisión | Por qué | Aprendido en |
|---|---|---|
| `Decimal` y céntimos enteros (`int(amount * 100)` y `divmod`) | Con `float`, 100/3 da partes que suman 99,99 o 100,01; con céntimos enteros, la suma es exacta siempre | 1.2 (`approx` es para medidas, no para dinero) |
| El céntimo sobrante va por orden alfabético | Es determinista y fácil de explicar; el orden del archivo dependería de cómo alguien escribió la fila | 1.2 (empates) |
| Validar con una expresión regular antes de `Decimal(...)` | `Decimal` acepta `1e3`, `NaN` o `-5`; el contrato no | 1.3 (un caso por regla) |
| `InputError` con el número de línea, convertido en código 2 solo en `cli.py` | El dominio no sabe de procesos; la CLI traduce. Las pruebas unitarias comprueban el mensaje y las de aceptación el código | 1.4 (inyectar el borde) |
| `utf-8-sig` al leer y salida forzada a UTF-8 | Excel guarda con BOM; la consola de Windows no usa UTF-8 por defecto | lecciones de entorno del camino |
| Pruebas de aceptación por subproceso, con `SPLITBILL_CMD` | Juzgan **cualquier** implementación, incluso en otro lenguaje; solo conocen el contrato | 1.1 (pirámide) |

## Trampas encontradas al construirlo
- **Mi propia prueba no distinguía el bug.** La prueba "el mayor deudor paga primero" usaba datos donde el mayor deudor también era el primero en orden alfabético, así que la mutación M07 la pasaba. Es la trampa de los empates del lab 1.2, repetida en el proyecto. Se arregló eligiendo nombres que separan los dos criterios.
- **El script de mutaciones escondía un bug de codificación.** Al principio fijaba `PYTHONIOENCODING=utf-8` para todos sus procesos, así que la mutación que quita la salida UTF-8 (M12) pasaba. Sin esa variable, en Windows, la prueba A8 la atrapa. Un entorno de pruebas "demasiado cómodo" esconde bugs.
- **`Decimal("-0.00")` existe** y se muestra como `-0.00` con el formato `+.2f`. `format_amount` trata cualquier cero como `0.00`, y hay un caso de prueba para eso.

## 🔨 Rómpelo tú
Cambia **una** cosa en una copia, corre las dos suites (`reference/` y `acceptance/`) y compara con la falla real de abajo. Cada fila se ejecutó con un script en una copia limpia (Windows, Python 3.12, pytest 9.2.0). Las cifras son "pruebas que fallan / pruebas que corrieron".

| # | Cambio | Unitarias | Aceptación | Falla real (primera) |
|---|---|---|---|---|
| M01 | `money.split`: repartir con `float` y redondear cada parte | 7/46 | 5/15 | `assert Decimal('0.01') == 0` (los saldos no suman cero) |
| M02 | El céntimo sobrante va a los **últimos** nombres | 4/46 | 1/15 | `assert ['ana -33.33'...'caro -33.34'] == ['ana -33.34'...'caro -33.33']` |
| M03 | Olvidar el céntimo sobrante | 8/46 | 6/15 | `assert Decimal('0.01') == 0` |
| M04 | La expresión regular acepta tres decimales | 2/46 | 1/15 | `Failed: DID NOT RAISE ValueError`; aceptación: `assert 0 == 2` |
| M05 | Aceptar un monto cero (`< 0` en vez de `<= 0`) | 2/46 | **0/15** | `Failed: DID NOT RAISE ValueError` |
| M06 | Repartir en el orden del archivo, no alfabético | 1/46 | 1/15 | `assert ['ana -33.33'...'caro -33.34'] == ['ana -33.34'...'caro -33.33']` |
| M07 | Que pague primero el deudor alfabético, no el mayor | 1/46 | **0/15** | `assert Transfer(debt...imal('15.00')) == Transfer(debt...imal('45.00'))` |
| M08 | Salir con código **1** ante un error de entrada | **0/46** | 5/15 | `assert 1 == 2` |
| M09 | Escribir el error en stdout en vez de stderr | 1/46 | 4/15 | `assert 'error: line ...umns, got 4\n' == ''` |
| M10 | No quitar los espacios de los nombres | 1/46 | **0/15** | `assert [Expense(paye...o ', 'caro'))] == [Expense(paye...to', 'caro'))]` |
| M11 | Leer como `utf-8` (sin aceptar el BOM) | 1/46 | 1/15 | `assert 2 == 0` |
| M12 | No forzar UTF-8 en la salida | **0/46** | 1/15 | `assert ['jos� -10.00...mar�a +10.00'] == ['josé -10.00...maría +10.00']` |
| M13 | Mostrar el cero con signo | 2/46 | **0/15** | `assert '+0.00' == '0.00'` |

**Qué enseña la tabla:**
- **Ninguna suite sola basta.** M08 y M12 solo los ve la aceptación; M05, M07, M10 y M13 solo las unitarias.
- **M08:** la prueba unitaria de la CLI compara con la constante `EXIT_INPUT_ERROR`, así que si la constante cambia, la prueba cambia con ella. La aceptación escribe el `2` literal porque el número **es** el contrato.
- **M07:** la aceptación no fija *qué* transferencias se hacen, solo que salden y sean pocas (A4). Es a propósito: otra implementación puede elegir otras, igual de válidas.
- **M12:** se midió en Windows. En Linux y macOS la salida suele ser UTF-8 por defecto (depende de la configuración regional), así que allí esta mutación podría pasar inadvertida. Por eso el contrato fija UTF-8 y la referencia lo fuerza.

## Lo que falta a propósito
- **Un modo de "previsualizar" el archivo** o mensajes con todas las líneas inválidas a la vez (hoy se detiene en la primera).
- **Persistencia y monedas:** fuera de alcance (ver [BRIEF.md](BRIEF.md)).
- **El mínimo de transferencias:** el algoritmo voraz no siempre logra el mínimo; buscarlo es mucho más caro.

## Preguntas para desafiar el diseño
1. ¿Por qué no basta con redondear cada parte a 2 decimales? Construye un ejemplo en el que la suma no cierre.
2. Si el grupo prefiere que el céntimo extra lo pague quien pagó la cuenta, ¿qué cambia en el código y qué pruebas tendrían que cambiar?
3. ¿Qué pruebas de esta suite romperías si cambias `settle` por otro algoritmo válido? ¿Cuáles deberían seguir pasando?
4. M05, M10 y M13 pasan la aceptación. ¿Agregarías criterios al contrato para cubrirlos o los dejarías como detalles internos? ¿Por qué?
5. ¿Qué pasaría con estas pruebas si un día el archivo tuviera 100 000 filas? ¿Qué medirías?
