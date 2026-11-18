# 🔍 Revisión guiada · Dividir la cuenta

Cómo leer la suite de referencia, por qué es como es, y cómo comprobar que cada prueba sirve de verdad.

## Orden de lectura
1. [`src/splitbill/money.py`](reference/src/splitbill/money.py) y su suite, [`tests/test_money.py`](reference/tests/test_money.py): **la respuesta a la pregunta del dominio.** `split` reparte en céntimos enteros, así que la suma cierra por construcción, no por redondeo. Las pruebas son casi todas tablas: montos válidos, montos inválidos, repartos con y sin céntimos sobrantes.
2. [`src/splitbill/ledger.py`](reference/src/splitbill/ledger.py) y [`tests/test_ledger.py`](reference/tests/test_ledger.py): leer el CSV con números de línea, calcular saldos y transferencias. Funciones puras (entran datos y salen datos), así que sus pruebas no necesitan archivos: pasan listas de texto.
3. [`src/splitbill/cli.py`](reference/src/splitbill/cli.py) y [`tests/test_cli.py`](reference/tests/test_cli.py): el borde con el mundo (archivo, salida, códigos). Es la única capa que necesita `tmp_path` y `capsys`, y una fixture propia, `csv_file`, que escribe el CSV de cada prueba.

## Decisiones y por qué
| Decisión | Por qué | Aprendido en |
|---|---|---|
| Comparar `Decimal` exacto, nunca con `approx` | El dominio exige que sobre o falte **cero** céntimos; una tolerancia escondería justo el bug que importa | 1.2 (`approx` es para medidas, no para dinero) |
| Una prueba parametrizada por función, con un caso por clase de entrada | Montos válidos e inválidos, repartos exactos y con sobrantes: cada fila es una clase, y su ID dice cuál falló | 1.3 |
| Los repartos con céntimos sobrantes se prueban en el límite: 1 y 2 céntimos sobrantes, y menos céntimos que personas (`0.02` entre 3) | Es donde viven los errores de redondeo y de «a quién le toca» | 1.3 (valores límite) |
| La suma de los saldos se comprueba en varios escenarios, no solo el valor de cada saldo | Es la pregunta del dominio, escrita como prueba: vale para cualquier dato | 1.1 (prueba el comportamiento) |
| Una fixture `csv_file` que devuelve una función para escribir el archivo | Cada prueba de la CLI necesita un CSV distinto; la fixture escribe el encabezado y elige la codificación | 1.4 y [BRIEF](BRIEF.md#lo-nuevo-de-este-proyecto) |
| `tmp_path` para el archivo y `capsys` para la salida | La CLI se prueba en el mismo proceso, sin ensuciar la carpeta y leyendo stdout y stderr por separado | 1.5 (`tmp_path`) y [BRIEF](BRIEF.md#lo-nuevo-de-este-proyecto) (`capsys`) |
| El código de salida escrito como `2`, no como `EXIT_INPUT_ERROR` | El número es parte del contrato. Una prueba que compara con la misma constante que usa el código cambia junto con ella y no protege nada (mutante `m08`) | 1.1 (la prueba que no puede fallar) |

## Trampas encontradas al construirla
- **Una prueba propia no distinguía el bug.** «El mayor deudor paga primero» usaba datos donde el mayor deudor también era el primero en orden alfabético, así que `m07` pasaba. Es la trampa de los empates del lab 1.2, repetida en el proyecto. Se arregló eligiendo nombres que separan los dos criterios: ver el comentario en `test_the_largest_debtor_pays_the_largest_creditor_first`.
- **Comparar con la constante.** En la primera versión, las pruebas de la CLI comparaban el código de salida con `EXIT_INPUT_ERROR`. La caza lo delató: `m08` (código 1) sobrevivía, porque la constante y la prueba cambiaban juntas. Ahora la prueba escribe `2`.
- **`Decimal("-0.00")` existe** y se muestra como `-0.00` con el formato `+.2f`. `format_amount` trata cualquier cero como `0.00`, y hay un caso de prueba para eso (`negative-zero`).

## 🔨 Rómpelo tú
Esta tabla dice qué pruebas de la referencia matan a cada mutante. Se midió corriendo la suite contra cada mutante (Python 3.13, pytest 9.2.0); las cifras son «pruebas que fallan / pruebas que corrieron».

| Mutante | Falla | Pruebas que lo matan | Fallo real (el primero) |
|---|---|---|---|
| `m01-float-split` | 7/46 | 3 casos de `test_shares_add_up_to_the_cent`, 2 de `test_balances_add_up_to_exactly_zero` y 2 más de `test_ledger.py` | `assert {'ana': Decim...mal('-33.33')} == {'ana': Decim...mal('-33.33')}` |
| `m02-leftover-to-the-last` | 4/46 | 3 casos de `test_shares_add_up_to_the_cent` y `test_the_leftover_cent_goes_to_the_first_name_in_alphabetical_order` | `assert {'ana': Decim...mal('-33.34')} == {'ana': Decim...mal('-33.33')}` |
| `m03-leftover-lost` | 8/46 | 3 de `test_shares_add_up_to_the_cent`, 3 de `test_balances_add_up_to_exactly_zero` y 2 más | `assert {'ana': Decim...mal('-33.33')} == {'ana': Decim...mal('-33.33')}` |
| `m04-three-decimals` | 2/46 | `test_invalid_amounts[three-decimals]` y `test_invalid_rows_say_which_line[three-decimals]` | `Failed: DID NOT RAISE InputError` |
| `m05-zero-accepted` | 2/46 | `test_zero_is_not_an_expense` y `test_invalid_rows_say_which_line[zero]` | `Failed: DID NOT RAISE InputError` |
| `m06-file-order` | 1/46 | Solo `test_the_leftover_cent_goes_to_the_first_name_in_alphabetical_order` | `assert {'ana': Decim...mal('-33.34')} == {'ana': Decim...mal('-33.33')}` |
| `m07-alphabetical-debtor` | 1/46 | Solo `test_the_largest_debtor_pays_the_largest_creditor_first` | `assert Transfer(debt...imal('15.00')) == Transfer(debt...imal('45.00'))` |
| `m08-exit-code-1` | 2/46 | `test_an_invalid_row_is_an_input_error_on_stderr` y `test_a_missing_file_is_an_input_error` | `assert 1 == 2` |
| `m09-error-on-stdout` | 1/46 | Solo `test_an_invalid_row_is_an_input_error_on_stderr` | `assert 'error: line ...umns, got 4\n' == ''` |
| `m10-names-not-stripped` | 1/46 | Solo `test_reads_payer_amount_and_participants` | `assert [Expense(paye...o ', 'caro'))] == [Expense(paye...to', 'caro'))]` |
| `m11-no-bom` | 1/46 | Solo `test_a_file_saved_by_excel_with_a_bom_is_accepted` | `assert 2 == 0` |
| `m12-signed-zero` | 2/46 | `test_amounts_are_shown_with_sign_and_two_decimals[settled]` y `[negative-zero]` | `assert '+0.00' == '0.00'` |

**El ejercicio:** borra (en tu rama) una de las pruebas que aparecen con «Solo» y vuelve a pasar la caza. El mutante de esa fila sobrevive. Después borra una prueba de una fila con varias: no pasa nada, porque otra la cubre. Eso responde una pregunta que la cobertura no puede responder: **¿qué prueba de tu suite es la única que protege algo?**

**Qué enseña la tabla:**
- **Las pruebas de propiedades del dominio matan mucho.** `test_balances_add_up_to_exactly_zero` no mira ningún saldo concreto, solo que sumen cero, y atrapa a los dos mutantes de redondeo.
- **Las pruebas con un solo caso protegen reglas finas.** `m06`, `m07`, `m10` y `m11` mueren con una sola prueba cada uno: si esa prueba no existiera, el bug pasaría.
- **La cobertura no lo habría dicho.** La suite tiene 100% de ramas en `money.py`, `ledger.py` y `cli.py` (lab 1.6), y eso no dice cuál de sus 46 pruebas es indispensable. La caza sí.

## Lo que falta a propósito
- **Pruebas de la aplicación como programa aparte**: correr `python -m splitbill` y mirar su salida real, su codificación y su código de salida. Son pruebas de aceptación (bloque 3). Por eso `__main__.py`, que fuerza la salida en UTF-8, no tiene pruebas aquí.
- **Mensajes con todas las líneas inválidas a la vez:** la aplicación se detiene en la primera, y la suite lo da por bueno.
- **Persistencia y monedas:** fuera de alcance (ver [BRIEF.md](BRIEF.md)).

## Preguntas para desafiar el diseño
1. ¿Por qué `test_balances_add_up_to_exactly_zero` tiene tres escenarios y no uno? ¿Qué escenario agregarías?
2. Si el grupo decide que el céntimo extra lo pague quien pagó la cuenta, ¿qué pruebas de la referencia tendrían que cambiar? ¿Cuáles deberían seguir pasando?
3. ¿Qué pruebas de esta suite romperías si cambias `settle` por otro algoritmo válido que también salda todo con pocas transferencias? ¿Están probando el comportamiento o un detalle?
4. `m09` muere con una sola prueba. ¿Escribirías otra para el error de archivo inexistente? ¿Qué mutante nuevo la justificaría?
5. Tu suite pasa la caza y la de un compañero también, pero la suya tiene la mitad de pruebas. ¿Cuál preferirías mantener, y qué mirarías para decidir?
