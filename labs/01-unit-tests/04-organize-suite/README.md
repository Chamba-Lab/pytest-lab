# 🧩 1.4 · Organizar la suite

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–1,5 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · pytest 9.2 |

## 🎯 Objetivos
- Escribir una preparación una sola vez, como *fixture*, y pedirla desde cada prueba que la necesita.
- Construir una fixture a partir de otra.
- Elegir cuánto vive una fixture (`scope`) según si guarda estado.
- Compartir fixtures entre archivos con `conftest.py`.
- Marcar pruebas (por ejemplo, las lentas) y elegir cuáles correr con `-m`.

## 💡 Por qué importa
En los labs anteriores cada prueba era corta y se preparaba sola. En un proyecto real, una suite tiene cientos de pruebas repartidas en muchos archivos, y casi todas empiezan igual: crear los mismos objetos, con los mismos datos. Si esa preparación se copia en cada prueba, un cambio en el constructor obliga a tocar cien lugares. Y si las pruebas lentas corren en cada cambio, el equipo deja de correr la suite.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, en la carpeta **`starter/`** de este lab.

## 🧠 Conceptos
En el [lab 1.1](../01-what-is-a-test/CONCEPT.md#anatomía-de-una-prueba-arrange-act-assert) viste que casi toda prueba tiene tres partes: preparar (*Arrange*), actuar (*Act*) y comprobar (*Assert*). Este lab trata de la primera: cómo escribir la preparación una vez y reutilizarla.

### La preparación compartida (*fixture*)
Mira estas dos pruebas de un inventario:

```python
def test_a_new_item_starts_at_zero():
    inventory = Inventory(Warehouse("lima"))   # preparar
    assert inventory.count("pen") == 0

def test_receiving_adds_stock():
    inventory = Inventory(Warehouse("lima"))   # la misma preparación, otra vez
    inventory.receive("pen", 5)
    assert inventory.count("pen") == 5
```

La primera línea se repite. La idea es sacarla a una función que prepara el escenario y que cada prueba **pide** cuando lo necesita. Casi todas las herramientas de testing tienen algo así (en JUnit se llama `@BeforeEach`); en pytest se llama **fixture**: una función decorada con `@pytest.fixture`. Una prueba la pide escribiendo su **nombre como parámetro**, y pytest la ejecuta y le pasa el resultado:

```python
import pytest


@pytest.fixture
def inventory():
    return Inventory(Warehouse("lima"))


def test_a_new_item_starts_at_zero(inventory):     # pytest llama a inventory() y pasa el resultado
    assert inventory.count("pen") == 0


def test_receiving_adds_stock(inventory):
    inventory.receive("pen", 5)
    assert inventory.count("pen") == 5
```

### Una fixture que usa otra
Una fixture también puede pedir fixtures, con el mismo mecanismo: los parámetros. Así se arman escenarios por capas:

```python
@pytest.fixture
def warehouse():
    return Warehouse("lima")


@pytest.fixture
def inventory(warehouse):              # pide la fixture warehouse
    return Inventory(warehouse)


@pytest.fixture
def stocked_inventory(inventory):      # un escenario más completo, sobre el anterior
    inventory.receive("pen", 5)
    return inventory
```

### Cuánto vive una fixture (*scope*)
Por defecto, pytest crea la fixture de nuevo **para cada prueba**: es el `scope` de función. Se puede pedir que viva más con `@pytest.fixture(scope="module")` (una vez por archivo) o `scope="session"` (una vez por corrida); entonces las pruebas de ese alcance reciben el mismo objeto.

### Fixtures para varios archivos (`conftest.py`)
Las fixtures que se escriben en un archivo especial, `conftest.py`, dentro de la carpeta de las pruebas, quedan disponibles para todos los archivos de pruebas de esa carpeta. pytest lo carga solo, sin `import`.

### Marcas (*markers*)
Una marca es una etiqueta sobre una prueba, por ejemplo `@pytest.mark.slow`, y `-m` elige qué pruebas correr según sus marcas: `-m "not slow"` deja fuera las marcadas. Las marcas propias se **registran** en la configuración, con una línea que dice qué significan:

```toml
[tool.pytest]
markers = ["slow: tests that take long"]
```

## 📚 Documentación
- [pytest · How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest · Fixture scopes](https://docs.pytest.org/en/stable/how-to/fixtures.html#scope-sharing-fixtures-across-classes-modules-packages-or-session)
- [pytest · Sharing fixtures with `conftest.py`](https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files)
- [pytest · How to mark test functions with attributes](https://docs.pytest.org/en/stable/how-to/mark.html)

## 🧭 Escenario

### El código
[`cart.py`](starter/cart.py) ya funciona: un carrito de compras con precios en céntimos (2500 son 25,00). **No lo cambies.**

| Clase o método | Promete |
|---|---|
| `Catalog(prices)` | Guarda el precio de cada producto. `price(product)` lanza `ValueError("unknown product: …")` si no existe |
| `Cart(catalog)` | Un carrito vacío que usa ese catálogo |
| `add(product, quantity=1)` | Suma unidades. Producto desconocido o cantidad menor que 1 → `ValueError` |
| `subtotal()` / `total()` | La suma de precios / el subtotal menos el descuento |
| `discount()` | **10% del subtotal desde 100,00 inclusive**, redondeado hacia abajo al céntimo; 0 por debajo |

Las pruebas están en dos archivos:
- [`tests/test_cart.py`](starter/tests/test_cart.py): cuatro pruebas que **ya funcionan**, pero cada una arma su propio catálogo y su propio carrito.
- [`tests/test_discount.py`](starter/tests/test_discount.py): tres pruebas del descuento por escribir.

[`tests/conftest.py`](starter/tests/conftest.py) solo trae la parte de la caza.

### Cómo se revisa tu trabajo
La caza de mutantes del lab 1.2 y [`tests/test_structure.py`](starter/tests/test_structure.py), que revisa la organización: dónde viven las fixtures y qué marcas hay.

| Mutante | Bug sembrado | Lo mata |
|---|---|---|
| `m1-adding-replaces` | Agregar un producto que ya estaba reemplaza la cantidad en vez de sumarla | Ya muerto |
| `m2-unknown-product-accepted` | Acepta productos que no están en el catálogo | Ya muerto |
| `m3-discount-above-100` | El descuento empieza **después** de 100,00 (`>` en vez de `>=`) | Tarea 2 |
| `m4-discount-for-everyone` | Todos los carritos tienen descuento | Tarea 2 |
| `m5-fixed-discount` | El descuento siempre es 10,00, sea cual sea el subtotal | Tarea 2 |

`m1` y `m2` ya los matan las pruebas que vienen escritas: son **guardianes**. Mientras reorganizas esas pruebas, deben seguir muertos; si uno revive, tu cambio rompió una prueba.

## ✅ Tareas

Corre todo con este comando, igual en PowerShell o Bash:

```bash
python -m pytest
```

### Tarea 1 · La preparación, escrita una vez
**Meta:** que ninguna prueba de `test_cart.py` arme su propio carrito. **La validan:** [`test_the_tests_do_not_build_their_own_cart`](starter/tests/test_structure.py), y `m1` y `m2` deben seguir muertos.

- [ ] En `test_cart.py`, escribe una fixture `catalog` que devuelva `Catalog(PRICES)`.
- [ ] Escribe una fixture `cart` que **pida** `catalog` y devuelva `Cart(catalog)`.
- [ ] En cada una de las cuatro pruebas, cambia `cart = Cart(Catalog(PRICES))` por el parámetro `cart`.

### Tarea 2 · Una fixture sobre otra, compartida
**Meta:** probar el descuento desde un escenario preparado, y compartir las fixtures entre los dos archivos. **La validan:** [`test_the_fixtures_are_shared_from_conftest`](starter/tests/test_structure.py) y la caza de `m3`, `m4` y `m5`.

- [ ] Escribe una fixture `almost_discount` en `test_discount.py` que pida `cart`, le agregue un `"voucher"` (99,99) y lo devuelva: un carrito a un céntimo del descuento.
- [ ] Escribe las dos pruebas del límite pidiendo `almost_discount`: tal cual paga 9999 céntimos; con un `"sticker"` más (0,01), paga 9000.

🔮 **Predict first:** `catalog` y `cart` siguen en `test_cart.py`. ¿Funcionan las pruebas de `test_discount.py`? Córrelas antes de seguir.

- [ ] Mueve las tres fixtures (y `PRICES`) a `tests/conftest.py`, debajo de la parte de la caza.

🔮 **Predict first:** con tus dos pruebas del límite, ¿muere `m5-fixed-discount`, el que siempre descuenta 10,00?

- [ ] Escribe la tercera prueba, `test_the_discount_is_10_percent_of_any_subtotal`, con un subtotal lejos del límite (por ejemplo, dos vouchers) y su descuento exacto.

🔮 **Predict first:** el catálogo es el mismo para todas las pruebas, así que parece razonable crearlo una sola vez por archivo. ¿Qué pasa si `cart` tiene `scope="module"`? ¿Y si además `catalog` también lo tiene? Prueba los dos casos y vuelve a dejar ambas fixtures sin `scope`.

### Tarea 3 · Marcar la prueba lenta
**Meta:** que la prueba lenta tenga su marca y que puedas dejarla fuera. **La validan:** [`test_the_slow_marker_is_registered`](starter/tests/test_structure.py) y `test_the_slow_test_is_marked`.

🔮 **Predict first:** la configuración de estos labs trae `strict_markers = true`. ¿Qué pasa si corres solo las rápidas con `-m "not slow"` cuando la marca no está registrada? ¿Y si marcas la prueba sin registrarla? Pruébalo (PowerShell o Bash):

```bash
python -m pytest tests/test_cart.py tests/test_discount.py -m "not slow"
```

- [ ] Marca `test_many_additions_add_up` con `@pytest.mark.slow`.
- [ ] Registra la marca en [`pyproject.toml`](starter/pyproject.toml), dentro de `[tool.pytest]`: `markers = ["slow: tests that take long; skip them with -m \"not slow\""]`.
- [ ] Vuelve a correr el comando de arriba: ahora la prueba lenta queda fuera.

**Criterio de éxito:** `python -m pytest` dentro de `starter/` termina en verde: 17 pruebas pasan, ninguna se salta. Y con `-m "not slow"` sobre tus dos archivos, 6 pasan y 1 queda fuera (*deselected*).

## 🔍 Command dissection
| Comando o código | Qué hace |
|---|---|
| `@pytest.fixture(scope="module")` | Una sola instancia por archivo; `"session"`, una por corrida. Por defecto, `"function"` |
| `-m "not slow"` | Elige por marcas; acepta `and`, `or` y `not` |
| `--fixtures` | Lista las fixtures disponibles y dónde están definidas |
| `--lf` (*last failed*) | Corre solo lo que falló la vez anterior |

## 💼 En proyectos reales
- **Fixtures pequeñas que se combinan** valen más que una gigante que arma todo: cada prueba pide exactamente el escenario que necesita. Nómbralas por el escenario (`almost_discount`), no por cómo se construyen.
- **`scope` amplio solo para lo caro y que nadie modifica:** una conexión a una base de datos de prueba, un servidor levantado una vez.
- **Un `conftest.py` por carpeta:** en suites grandes hay uno en la raíz de `tests/` con lo común y otros en subcarpetas con lo específico.
- **En tu máquina, `-m "not slow"` en cada cambio; en el CI, todo.** Así nadie deja de correr la suite por impaciencia.
- **Bugs conocidos:** `@pytest.mark.xfail(reason="…", strict=True)` registra una prueba que se espera que falle (un bug que aún no se arregla) sin romper la suite, y con `strict` avisa cuando alguien lo arregla. La configuración de estos labs trae `strict_xfail = true`.

## 🚀 Reto extra
Escribe una fixture `discounted_cart` que pida `almost_discount` y le agregue el `"sticker"`, y reescribe con ella la prueba del límite. Después mira la lista de fixtures con su origen (`python -m pytest --fixtures tests/test_discount.py`) y encuentra las tuyas al final.

## 🆘 Pistas
<details><summary>Pista 1 · dirección</summary>

Una fixture es una función que devuelve lo que la prueba necesita. Si necesita otra fixture, la pide como parámetro, igual que una prueba.
</details>

<details><summary>Pista 2 · más concreta</summary>

```python
@pytest.fixture
def almost_discount(cart):
    cart.add("voucher")
    return cart
```

Dos vouchers suman 19998 céntimos; el 10% redondeado hacia abajo es 1999.
</details>

## ✔️ Respuestas verificadas
<details><summary>Ábrelas solo después de terminar las tareas</summary>

Se ejecutó con pytest 9.2.0; el CI verifica cada lab en Python 3.12 y 3.15.

**Tarea 2, las fixtures en `test_cart.py`.** No funcionan. Una fixture escrita en un archivo de pruebas solo existe para ese archivo, y las tres pruebas de `test_discount.py` dan *error* de preparación:

```text
E       fixture 'cart' not found
>       available fixtures: almost_discount, capfd, capfdbinary, caplog, capsys, …
```

En la lista está `almost_discount` (definida en ese archivo) y las que trae pytest, pero no `cart`. Para eso existe `conftest.py`.

**Tarea 2, `m5` con dos pruebas.** Sobrevive. En los dos casos del límite, el descuento correcto y el fijo de 10,00 dan lo mismo: 0 con 99,99, y 10,00 con 100,00 exactos.

```text
FAILED tests/test_mutant_hunt.py::test_your_tests_catch[m5-fixed-discount]
```

Es la lección de clases del lab 1.3: los límites no reemplazan a un representativo de la clase «con descuento», lejos del borde. Con dos vouchers, el descuento correcto es 1999 y el mutante sigue diciendo 1000.

**Tarea 2, `cart` con `scope="module"`.** No arranca ninguna prueba. Una fixture que vive todo el archivo no puede usar una que vive por prueba:

```text
ScopeMismatch: You tried to access the function scoped fixture catalog with a module scoped request object.
```

Con `catalog` también por módulo, arranca, y aparece el problema de fondo: todas las pruebas de `test_discount.py` comparten **el mismo carrito**, y cada `almost_discount` le agrega otro voucher.

```text
E       assert 18000 == 9000
E       assert 3999 == 1999
```

En la segunda prueba el carrito ya tenía el voucher de la primera; en la tercera, los de las dos anteriores. Pasa o falla según qué corrió antes. En cambio, `catalog` con `scope="module"` y `cart` por prueba funciona: el catálogo nadie lo modifica.

**Tarea 3, `-m "not slow"` sin marca registrada.** pytest no corre nada y termina con error, porque en modo estricto también revisa las marcas del `-m`:

```text
ERROR: Unknown marker(s) in '-m' expression: slow. Use 'pytest --markers' to see available markers.
```

**Tarea 3, la marca sin registrar.** El archivo entero no se puede recolectar:

```text
ERROR tests/test_cart.py - Failed: 'slow' not found in `markers` configuratio...
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

Así, un error de tipeo (`@pytest.mark.slwo`) no pasa inadvertido. Con la marca registrada, `-m "not slow"` deja fuera la prueba lenta (unos 0,3 s en la máquina donde se verificó): `6 passed, 1 deselected`.
</details>

## 🎤 Autoevaluación
1. ¿Qué problema resuelve una fixture que no resuelve una función auxiliar llamada al inicio de cada prueba?
2. ¿Cuándo usarías `scope="session"` y qué riesgo tiene? Da un ejemplo de algo que sí y algo que no.
3. Una prueba pasa sola y falla cuando corres todo el archivo. ¿Qué fixture revisarías primero y qué buscarías?
4. ¿Por qué conviene registrar las marcas y activar `strict_markers`?
5. Tu suite tarda 8 minutos y el equipo dejó de correrla antes de subir cambios. ¿Qué harías con lo de este lab?

La solución completa está en [`solution/`](solution/).

**Siguiente:** [1.5 · Dobles de prueba](../05-test-doubles/README.md)
