# 🧩 1.3 · Diseño de casos de prueba

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–1,5 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · pytest 9.2 |

## 🎯 Objetivos
- Dividir las entradas posibles en **clases de equivalencia** y elegir un caso representativo por clase.
- Encontrar los **valores límite** de una regla y probar los dos lados del límite.
- Diseñar datos que rompen **una sola regla** cada uno, para que un fallo diga qué se rompió.
- Escribir una tabla de casos como una sola prueba con `@pytest.mark.parametrize`, con un ID legible por caso.

## 💡 Por qué importa
En el lab 1.2 los casos venían dados: la tabla de `grades.py` decía qué probar. En un trabajo real nadie te da esa lista. Una función que recibe un texto tiene infinitas entradas posibles, y no puedes probarlas todas. La pregunta deja de ser «¿cómo escribo la prueba?» y pasa a ser **«¿qué casos elijo para que, con pocas pruebas, se escape la menor cantidad de bugs?»**. Hay técnicas para responderla, y son las mismas en cualquier lenguaje.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, en la carpeta **`starter/`** de este lab.

## 🧠 Conceptos
Los tres primeros conceptos son ideas de diseño: sirven con pytest, con JUnit o con una hoja de papel. El cuarto es cómo pytest escribe esas ideas.

### Clases de equivalencia (*equivalence partitioning*)
Imagina una función `can_vote(age)` que devuelve `True` desde los 18 años. Probar 19, 20, 21… 99 no aporta nada nuevo: todas esas edades **se comportan igual**, así que si 30 funciona, lo más probable es que 31 también. Un grupo de entradas que el código trata de la misma forma es una **clase de equivalencia**, y basta con un representativo por clase:

| Clase | Representativo | Resultado esperado |
|---|---|---|
| Menores de edad | 10 | `False` |
| Mayores de edad | 30 | `True` |
| Inválidas (negativas) | -1 | `ValueError` |

Para encontrar las clases, pregúntate: **¿qué entradas toman un camino distinto en la regla?** Cada regla suele partir las entradas en al menos dos clases: las que la cumplen y las que no.

### Valores límite (*boundary value analysis*)
Los bugs se esconden en el borde entre dos clases. El programador escribe `age > 18` cuando la regla decía «desde los 18», y el 30 y el 10 siguen pasando. Por eso, además del representativo, se prueba **el valor exacto del límite y el de al lado**: 17 y 18.

```python
def can_vote(age):
    return age > 18          # bug: debía ser >= 18

assert can_vote(30) is True   # pasa: el bug no se ve
assert can_vote(10) is False  # pasa: el bug no se ve
assert can_vote(18) is True   # falla: aquí aparece
```

### Un caso, una razón para fallar
Un formulario de registro rechaza un correo sin `@` y una edad menor de 18. Para probar la regla del correo, el dato debe tener una edad válida: si usas un correo inválido **y** una edad de 15, y la función solo responde «válido o no», el caso sigue dando «no válido» aunque la regla del correo esté rota, porque la edad lo tapa. Cada caso cumple todas las reglas menos la que prueba; así, cuando falla, sabes exactamente qué mirar.

### Parametrizar (*parametrize*)
Con lo anterior terminas con una tabla de casos: entrada y resultado esperado. Escribir una función de prueba por fila repite el mismo código; recorrer la tabla con un `for` dentro de una sola prueba se detiene en el primer fallo y no dice cuál fila falló. pytest resuelve las dos cosas con `@pytest.mark.parametrize`: escribes **una** función y la tabla, y pytest crea una prueba independiente por fila.

```python
import pytest

from voting import can_vote


@pytest.mark.parametrize(
    ("age", "expected"),          # los nombres de las columnas, que llegan como argumentos
    [
        pytest.param(10, False, id="minor"),
        pytest.param(17, False, id="just-below-the-limit"),
        pytest.param(18, True, id="the-limit-itself"),
        pytest.param(30, True, id="adult"),
    ],
)
def test_can_vote(age, expected):
    assert can_vote(age) is expected
```

En el reporte aparecen cuatro pruebas: `test_can_vote[minor]`, `test_can_vote[just-below-the-limit]`… El texto entre corchetes es el **ID** del caso, y `pytest.param(..., id="…")` te deja elegirlo.

## 📚 Documentación
- [pytest · How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [pytest · `pytest.param`](https://docs.pytest.org/en/stable/reference/reference.html#pytest-param)
- [Wikipedia · Equivalence partitioning](https://en.wikipedia.org/wiki/Equivalence_partitioning) y [Boundary-value analysis](https://en.wikipedia.org/wiki/Boundary-value_analysis)

## 🧭 Escenario

### El código
[`passwords.py`](starter/passwords.py) ya funciona: `violations(password)` devuelve la lista de reglas que una contraseña rompe, o `[]` si es válida. **No lo cambies.**

| Regla | Se rompe si… |
|---|---|
| `too-short` | tiene menos de 10 caracteres |
| `no-digit` / `no-upper` / `no-lower` | no tiene un dígito / una mayúscula / una minúscula |
| `whitespace` | tiene un espacio, un tabulador u otro espacio en blanco |
| `common` | está en la lista de contraseñas comunes, sin importar mayúsculas |

[`tests/test_policy.py`](starter/tests/test_policy.py) trae cinco pruebas escritas: `test_too_short`, `test_no_digit` y `test_no_upper`, que solo cambian en sus datos y que la tarea 1 reemplaza, y dos que no tocas (una contraseña válida y la lista de comunes). Además trae dos pruebas por escribir.

### Cómo se revisa tu trabajo
- [`tests/test_mutant_hunt.py`](starter/tests/test_mutant_hunt.py): la caza de mutantes del lab 1.2, con mutantes de `passwords.py`.
- [`tests/test_structure.py`](starter/tests/test_structure.py): lista tus pruebas sin correrlas (`--collect-only`) y revisa que estén organizadas como pide la tarea 1.

| Mutante | Bug sembrado | Lo mata la tarea |
|---|---|---|
| `m1-no-lower-rule` | La regla `no-lower` nunca reporta nada | 1 |
| `m2-whitespace-rule-off` | La regla `whitespace` nunca reporta nada | 1 |
| `m3-common-case-sensitive` | `Password1234` ya no cuenta como común (solo en minúsculas) | 1 |
| `m4-ten-is-too-short` | Una contraseña de 10 caracteres cuenta como corta | 2 |
| `m5-nine-is-enough` | Una contraseña de 9 caracteres ya no es corta | 2 |

## ✅ Tareas

Corre todo (tus pruebas, la caza y la revisión de estructura), en PowerShell o Bash:

```bash
python -m pytest
```

### Tarea 1 · Una clase por regla
**Meta:** una sola prueba parametrizada, `test_each_rule`, con un caso por regla. **La validan:** [`test_rules_are_one_parametrized_test_with_readable_ids`](starter/tests/test_structure.py), `test_the_copied_tests_are_gone` y la caza de `m1`, `m2` y `m3`.

- [ ] Para cada una de las seis reglas, busca una contraseña que rompa **solo** esa regla. Un buen punto de partida es una contraseña válida, como `Correct7Horse`: a partir de ella, quita una cosa por vez.
- [ ] Decora `test_each_rule` con `@pytest.mark.parametrize(("password", "expected"), [...])` y dale los parámetros `password` y `expected`.
- [ ] Escribe un `pytest.param` por regla, con el nombre de la regla como ID: `pytest.param("Short1A", ["too-short"], id="too-short")`.
- [ ] Borra `test_too_short`, `test_no_digit` y `test_no_upper`.

🔮 **Predict first:** si no pones `id=`, ¿cómo se llamará en el reporte el caso `("Short1A", ["too-short"])`? Compruébalo listando las pruebas sin correrlas (PowerShell o Bash):

```bash
python -m pytest tests/test_policy.py --collect-only -q
```

### Tarea 2 · Los dos lados del límite
**Meta:** probar el límite de largo con los valores justo a cada lado. **La validan:** la caza de `m4` y `m5`.

🔮 **Predict first:** antes de escribir esta tarea, tu suite ya tiene contraseñas de 7 caracteres (`Short1A`) y de 13 (`Correct7Horse`), una de cada lado del límite. ¿Matan a `m4` o a `m5`? Corre la caza y compruébalo.

- [ ] Encuentra el límite en la tabla del escenario: ¿cuál es el largo más corto que **no** rompe `too-short`?
- [ ] En `test_length_limit`, escribe una prueba parametrizada con dos casos: una contraseña de un carácter menos que el límite, y otra con el largo exacto. Las dos deben cumplir todas las demás reglas.
- [ ] Dale a cada caso un ID que diga su largo, por ejemplo `id="9-chars"`.

🔮 **Predict first:** si escribes solo el caso del largo exacto, ¿qué mutante sobrevive?

**Criterio de éxito:** `python -m pytest` dentro de `starter/` termina en verde: 18 pruebas pasan, ninguna se salta.

## 🔍 Command dissection
| Comando o código | Qué hace |
|---|---|
| `@pytest.mark.parametrize(("a", "b"), [...])` | Corre la prueba una vez por elemento de la lista; cada elemento da un valor a `a` y otro a `b` |
| `pytest.param(x, y, id="nombre")` | Un caso de la tabla, con su ID |
| `--collect-only` | Lista las pruebas que se correrían, sin correrlas |

## 💼 En proyectos reales
- **Las clases y los límites salen de la regla, no del código.** Si miras el código para elegir los casos, vas a probar lo que el código hace, no lo que debería hacer.
- **Los IDs son para quien lee el CI a las 2 de la mañana.** `test_each_rule[common]` se entiende; `test_each_rule[Password1234-expected5]` obliga a abrir el código.
- **Parametrizar no es gratis.** Una tabla con 40 filas casi iguales es tan difícil de mantener como 40 pruebas. Pocos casos que representen clases distintas, más los límites.
- **Las mismas técnicas valen para fechas, montos y listas:** fin de mes, cero y negativos, lista vacía, un elemento, el máximo permitido.

## 🚀 Reto extra
`test_every_common_password_is_rejected` recorre la lista con un `for`. Conviértela en una prueba parametrizada con un caso por contraseña común (`@pytest.mark.parametrize("password", sorted(COMMON))`). Después rompe a propósito una entrada de la lista en `passwords.py` y compara el reporte de las dos versiones: ¿cuál te dice más?

## 🆘 Pistas
<details><summary>Pista 1 · dirección</summary>

Parte de `Correct7Horse` (13 caracteres, con mayúscula, minúscula y dígito) y quítale una cosa por vez. Para el límite, cuenta los caracteres: el largo exacto es el mínimo de la regla.
</details>

<details><summary>Pista 2 · más concreta</summary>

- `no-lower`: `"UPPERCASE1234"`. `whitespace`: `"Has Space1234"`. `common`: `"Password1234"` (en minúsculas está en la lista).
- Tarea 2: `"Abcdefg12"` (9 caracteres) rompe solo `too-short`; `"Abcdefg123"` (10) es válida.
</details>

## ✔️ Respuestas verificadas
<details><summary>Ábrelas solo después de terminar las tareas</summary>

Se ejecutó con pytest 9.2.0; el CI verifica cada lab en Python 3.12 y 3.15.

**Tarea 1, sin `id=`.** pytest arma el ID con los valores; a las listas, que no sabe resumir, les pone el nombre del parámetro y su posición:

```text
tests/test_policy.py::test_each_rule[Short1A-expected0]
tests/test_policy.py::test_each_rule[NoDigitsHereAtAll-expected1]
tests/test_policy.py::test_each_rule[lowercase1234-expected2]
```

**Tarea 2, antes de escribirla.** No matan a ninguno. Con solo la tarea 1 resuelta, la caza termina así:

```text
FAILED tests/test_mutant_hunt.py::test_your_tests_catch[m4-ten-is-too-short]
FAILED tests/test_mutant_hunt.py::test_your_tests_catch[m5-nine-is-enough]
2 failed, 14 passed, 1 skipped
```

7 y 13 caracteres están lejos del límite: el código real y los dos mutantes dicen lo mismo de ellos. Solo los valores pegados al límite (9 y 10) separan el código correcto del que tiene el bug.

**Tarea 2, solo el largo exacto.** Sobrevive `m5-nine-is-enough`: el caso de 10 caracteres mata a `m4` (que lo llama corto), pero nada en la suite tiene 9 caracteres, que es donde `m5` se equivoca.

```text
FAILED tests/test_mutant_hunt.py::test_your_tests_catch[m5-nine-is-enough]
1 failed, 16 passed
```
</details>

## 🎤 Autoevaluación
1. Una función calcula el envío: gratis desde 100 de compra, 5 por debajo, y error con montos negativos. ¿Qué clases de equivalencia ves y qué valores probarías?
2. ¿Por qué un caso de prueba debería romper una sola regla? Da un ejemplo de un bug que un caso con varias reglas rotas dejaría pasar.
3. ¿Qué ventaja tiene una prueba parametrizada sobre un `for` dentro de una sola prueba?
4. Tu suite prueba el límite de edad con 18. ¿Qué bug se escapa y qué caso agregarías?
5. ¿Por qué conviene sacar las clases y los límites del requisito y no del código?

La solución completa está en [`solution/`](solution/).

**Siguiente:** [1.4 · Organizar la suite](../04-organize-suite/README.md)
