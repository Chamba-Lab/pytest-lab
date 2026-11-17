# 🧩 1.3 · Parametrizar y organizar

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` 🆕 `modern` | Python 3.12+ · pytest 9.2 |

## 🎯 Objetivos
- Convertir pruebas repetidas en una sola prueba con `@pytest.mark.parametrize`.
- Dar a cada caso un ID legible para que un fallo se entienda sin abrir el código.
- Documentar un bug conocido con `xfail` **estricto**, para que la suite avise cuando alguien lo arregle.
- Crear y usar una marca propia (`slow`) y elegir qué correr con `-m`.
- Configurar pytest con la tabla TOML nativa `[tool.pytest]` (pytest 9+) y activar las opciones strict.

## 💡 Por qué importa
Las suites reales tienen cientos de casos que solo cambian en los datos. Copiar y pegar pruebas las hace largas, y cuando falla una no sabes cuál de las veinte copias fue. Además, todo proyecto acumula bugs conocidos que aún no se arreglan: si la suite no los registra bien, o rompe el CI todos los días o se olvidan para siempre.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, abre una terminal **dentro de la carpeta `starter/` de este lab**:

PowerShell:

```powershell
Get-Location
```

Bash:

```bash
pwd
```

## 🧠 Conceptos
- **`@pytest.mark.parametrize`:** una función de prueba, muchos casos. Cada caso es una prueba independiente en el reporte.
- **IDs:** el nombre de cada caso entre corchetes (`test_each_rule[too-short]`). Sin `id=`, pytest los inventa a partir de los datos.
- **`xfail`:** "se espera que falle" (un bug conocido). Si pasa sin esperarlo, es un **XPASS**. Con `strict`, un XPASS hace fallar la suite.
- **Marcas propias:** etiquetas como `@pytest.mark.slow` para elegir qué correr. Con `strict_markers`, una marca no registrada es un error y no un simple aviso.
- **Configuración nativa (pytest 9):** `[tool.pytest]` en `pyproject.toml` usa tipos TOML reales (listas, booleanos). La tabla antigua `[tool.pytest.ini_options]` trata todo como texto.

## 📚 Documentación
- [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [How to use skip and xfail](https://docs.pytest.org/en/stable/how-to/skipping.html)
- [How to mark test functions with attributes](https://docs.pytest.org/en/stable/how-to/mark.html)
- [Configuration: `pyproject.toml`](https://docs.pytest.org/en/stable/reference/customize.html) y [Good practices: strict mode](https://docs.pytest.org/en/stable/explanation/goodpractices.html)

## 🧭 Escenario
[`passwords.py`](starter/passwords.py) ya funciona: `violations(password)` devuelve la lista de reglas que una contraseña rompe (`[]` si es válida). **No lo cambies.**

| Regla | Se rompe si… |
|---|---|
| `too-short` | tiene menos de 12 caracteres |
| `no-digit` / `no-upper` / `no-lower` | no tiene un dígito / una mayúscula / una minúscula |
| `whitespace` | tiene un espacio |
| `common` | está en la lista de contraseñas comunes, sin importar mayúsculas |

> [!IMPORTANT]
> **Bug conocido (issue #7):** solo el espacio cuenta como "espacio en blanco"; un tabulador o un salto de línea no se detectan. Todavía no está arreglado.

Tus pruebas están en [`tests/test_policy.py`](starter/tests/test_policy.py). Dos archivos las revisan; no los edites:
- [`tests/test_mutant_hunt.py`](starter/tests/test_mutant_hunt.py): la caza del lab 1.2, con una variante nueva.
- [`tests/test_structure.py`](starter/tests/test_structure.py): revisa la organización con `--collect-only` y lee la configuración.

| Variante | Qué cambia | La mata la tarea |
|---|---|---|
| `m1-no-lower-rule` | La regla `no-lower` nunca reporta nada | 1 |
| `m2-whitespace-rule-off` | La regla `whitespace` nunca reporta nada | 1 |
| `m3-common-case-sensitive` | `Password1234` ya no cuenta como común (solo en minúsculas) | 1 |
| `f1-tab-bug-fixed` | **No es un bug: es el arreglo del issue #7.** Tu suite debe fallar para avisarte que el `xfail` sobra | 2 |

## ✅ Tareas

```powershell
python -m pytest
```

### Tarea 1 · Una sola prueba parametrizada
**Meta:** reemplazar `test_too_short`, `test_no_digit` y `test_no_upper` por **una** prueba, `test_each_rule`, que cubra las seis reglas. **La validan:** `test_rules_are_one_parametrized_test_with_readable_ids` y la caza de `m1`, `m2` y `m3`.

- [ ] Decora `test_each_rule` con `@pytest.mark.parametrize(("password", "expected"), [...])` y dale dos parámetros.
- [ ] Escribe un caso por regla. Cada contraseña debe romper **solo** esa regla.
- [ ] Ponle a cada caso un ID con el nombre de la regla: `pytest.param("Short1A", ["too-short"], id="too-short")`.
- [ ] Borra las tres pruebas viejas.

🔮 **Predice primero:** si no pones `id=`, ¿cómo se llamará en el reporte el caso `("Short1A", ["too-short"])`? Compruébalo con:

```powershell
python -m pytest tests/test_policy.py --collect-only -q
```

### Tarea 2 · El bug conocido, documentado
**Meta:** registrar el issue #7 sin romper el CI y sin olvidarlo. **La valida:** la caza de `f1-tab-bug-fixed`.

- [ ] Agrega a `test_each_rule` un caso con tabulador (`"Tab\tSeparated12"`), cuyo resultado correcto sería `["whitespace"]`.
- [ ] Márcalo con `marks=pytest.mark.xfail(reason="issue #7: …")` e `id="tab-is-whitespace"`.

🔮 **Predice primero:** con el `xfail` tal cual, si mañana alguien arregla el bug, ¿tu suite avisa? Corre la caza y mira qué pasa con `f1`.

> [!WARNING]
> Un `xfail` que empieza a pasar no hace fallar nada por defecto: solo aparece una `X` en el reporte.

### Tarea 3 · Configuración nativa y una marca propia
**Meta:** pasar la configuración a `[tool.pytest]`, activar las opciones strict y separar las pruebas lentas. **La validan:** `test_configuration_uses_the_native_toml_table`, `test_strict_options_are_on` y `test_slow_marker_is_registered_and_used`.

- [ ] En [`pyproject.toml`](starter/pyproject.toml), cambia `[tool.pytest.ini_options]` por `[tool.pytest]` y escribe los valores con tipos TOML: `testpaths = ["tests"]`, `pythonpath = ["."]`.
- [ ] Agrega `strict_markers = true` y `strict_xfail = true`.
- [ ] Marca `test_every_common_password_is_rejected` con `@pytest.mark.slow`.
- [ ] Registra la marca: `markers = ["slow: tests that take long"]`.
- [ ] Corre solo las rápidas:

```powershell
python -m pytest -m "not slow" tests/test_policy.py
```

> [!WARNING]
> En la tabla nativa los tipos importan, y las dos tablas no pueden convivir.

**Criterio de éxito:** `python -m pytest` en `starter/` termina en verde: 17 pruebas pasan y 1 es `xfailed` (el issue #7).

## 🔍 Disección de comandos
| Comando o código | Qué hace |
|---|---|
| `@pytest.mark.parametrize(("a", "b"), [...])` | Corre la prueba una vez por cada tupla; los nombres se pasan como argumentos |
| `pytest.param(..., id="x", marks=...)` | Un caso con nombre propio y marcas solo para él |
| `--collect-only -q` | Lista las pruebas que se correrían, sin correrlas |
| `-m "not slow"` | Solo las pruebas que no tienen la marca `slow` (acepta `and`, `or`, `not`) |
| `-rxX` | Agrega al resumen los `xfailed` (x) y `xpassed` (X) con su motivo |
| `strict_markers = true` | Una marca no registrada en `markers` es un error |
| `strict_xfail = true` | Todo `xfail` se comporta como `strict=True`: un XPASS hace fallar la suite |

## 👀 Qué deberías ver
Con el starter tal cual:

```text
8 failed, 6 passed, 1 skipped
```

Fallan las 4 variantes de la caza y las 4 revisiones de estructura. Las 5 pruebas que ya existen pasan (también el guardián), y `test_each_rule` se salta. Al terminar, solo la parte rápida:

```text
7 passed, 1 deselected, 1 xfailed
```

## 💼 En proyectos reales
- **Un caso, una razón para fallar.** Si cada contraseña de prueba rompe varias reglas, un fallo no te dice cuál. Por eso los datos de la tarea 1 rompen una sola regla cada uno.
- **Los IDs son para la persona que lee el CI a las 2 de la mañana.** `test_each_rule[common]` se entiende; `test_each_rule[Password1234-expected5]` obliga a abrir el código.
- **`xfail` siempre con motivo y número de issue.** Es una deuda registrada, no un comentario olvidado. Con `strict_xfail`, el arreglo del bug te obliga a quitarlo.
- **Activa las opciones strict desde el día uno.** Sin `strict_markers`, un `@pytest.mark.slwo` mal escrito solo produce un aviso en el resumen (`PytestUnknownMarkWarning: Unknown pytest.mark.slwo - is this a typo?`), y esa prueba queda fuera de `-m slow` sin que nada falle. Con `strict_markers` es un error que no se puede pasar por alto.
- **Separa las pruebas lentas** (`-m "not slow"` en cada cambio, todas en el CI). Así la suite rápida se sigue corriendo.

## 🚀 Reto extra
Agrega un caso para una contraseña que rompe **dos** reglas a la vez (por ejemplo, corta y sin dígitos) y comprueba el orden de la lista. Luego escribe un mutante que cambie ese orden en `violations` y comprueba que tu caso lo mata.

## 🆘 Pistas
<details><summary>Pista 1 · dirección</summary>

Busca para cada regla una contraseña que cumpla todas las demás. Una buena base: 12 o más caracteres, con mayúscula, minúscula y dígito (`Correct7Horse`), y a partir de ahí quítale una cosa.
</details>

<details><summary>Pista 2 · más concreta</summary>

- `no-lower`: `"UPPERCASE1234"`. `whitespace`: `"Has Space1234"`. `common`: `"Password1234"` (que en minúsculas está en la lista).
- Tarea 2: `pytest.mark.xfail(reason="…", strict=True)`, o `strict_xfail = true` en la configuración (tarea 3) para no repetirlo.
</details>

## ✔️ Respuestas verificadas
<details><summary>Ábrelas solo después de terminar las tareas</summary>

Todo esto se ejecutó con Python 3.12 y pytest 9.2.0.

**Tarea 1.** Sin `id=`, pytest arma el ID con los valores, y a las listas les pone el nombre del parámetro más un número:

```text
tests/test_policy.py::test_each_rule[Short1A-expected0]
tests/test_policy.py::test_each_rule[UPPERCASE1234-expected1]
```

**Tarea 2.** No avisa. Con el `xfail` no estricto, la variante con el bug arreglado deja la suite en verde, con un `xpassed`:

```text
E       AssertionError: Variant 'f1-tab-bug-fixed' survived: your tests still pass with it.
E         8 passed, 1 xpassed in 0.01s
```

Con `strict=True` en la marca, o `strict_xfail = true` en la configuración, el XPASS hace fallar la suite y la variante muere.

**Tarea 3.** Tres errores reales que puedes encontrarte:

Las dos tablas a la vez (pytest no arranca, código de salida 4):

```text
ERROR: …\pyproject.toml: Cannot use both [tool.pytest] (native TOML types) and [tool.pytest.ini_options] (string-based INI format) simultaneously.
```

`pythonpath = "."` (texto) en la tabla nativa:

```text
ERROR: …\pyproject.toml: config option 'pythonpath' expects a list for type 'paths', got str: '.'
```

`strict_markers = true` sin registrar `slow`:

```text
ERROR tests/test_policy.py - Failed: 'slow' not found in `markers` configurat...
```
</details>

## 🎤 Autoevaluación
1. ¿Qué ventaja tiene una prueba parametrizada sobre un `for` dentro de una sola prueba que recorre los casos?
2. ¿Por qué cada contraseña de prueba debería romper una sola regla?
3. ¿Qué diferencia hay entre `skip` y `xfail`? ¿Cuándo usarías cada uno?
4. Tu equipo arregló un bug y nadie quitó su `xfail`. ¿Qué configuración lo habría evitado y qué habría pasado en el CI?
5. ¿Qué cambia entre `[tool.pytest.ini_options]` y `[tool.pytest]`, y por qué `pythonpath = "."` funciona en una y falla en la otra?

La solución completa está en [`solution/`](solution/).

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?
