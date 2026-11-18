# 🧩 2.2 · Archivos reales

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–1,5 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · pytest 9.2 |

## 🎯 Objetivos
- Guardar los datos de una prueba como archivos junto a las pruebas, y encontrarlos desde cualquier carpeta.
- Comparar lo que escribe tu código con un archivo esperado (*golden file*).
- Distinguir el texto de los bytes de un archivo, y fijar la codificación y los saltos de línea al leer y escribir.
- Probar los bordes del sistema de archivos: una carpeta que todavía no existe y un archivo que ya existe.

## 💡 Por qué importa
En el [lab 1.5](../../01-unit-tests/05-test-doubles/README.md) usaste `tmp_path` para que `LoanStore` escribiera en una carpeta desechable. Ahí el archivo era un detalle; aquí es **el tema**. Un CSV exportado de Excel trae comillas y tildes que nadie escribe a mano, y un reporte que se ve igual en pantalla puede tener bytes distintos en Windows y en Linux. Son errores que solo aparecen con archivos de verdad, y que una prueba con un doble nunca ve (lab [2.1](../01-what-changes/README.md)).

## 📍 Dónde correr los comandos
Con el entorno virtual activo, en la carpeta **`starter/`** de este lab.

## 🧠 Conceptos

### Datos de prueba junto a las pruebas (*test data*)
Para probar un lector de CSV podrías armar el texto dentro de la prueba, línea por línea. Con siete filas ya cuesta leerlo, y además es el CSV que **tú** imaginaste, no el que exporta una planilla. La idea es guardar un archivo real de ejemplo en la carpeta de pruebas, revisarlo una vez y usarlo desde las pruebas que lo necesiten:

```text
tests/
├── data/
│   └── orders.csv
└── test_orders.py
```

Para encontrarlo, la prueba arma la ruta desde **su propia carpeta**. En Python, `__file__` es la ruta del archivo que se está ejecutando, y `Path(__file__).parent` es la carpeta que lo contiene:

```python
from pathlib import Path

DATA = Path(__file__).parent / "data"

def test_reads_the_orders():
    orders = load_orders(DATA / "orders.csv")
    assert len(orders) == 3
```

### Archivos esperados (*golden files*)
Ahora el problema inverso: tu código **escribe** un reporte de veinte líneas. Comprobarlo con veinte `assert` es tedioso, y basta un cambio de formato para reescribirlos todos. La idea es guardar el resultado correcto como un archivo, revisado a mano una vez, y comparar el archivo completo:

```python
def test_the_invoice_matches_the_expected_one(tmp_path):
    output = tmp_path / "invoice.txt"
    write_invoice(ORDER, output)
    assert output.read_text(encoding="utf-8") == (DATA / "expected_invoice.txt").read_text(encoding="utf-8")
```

Ese archivo de referencia se llama *golden file*, y la técnica, *snapshot testing* o *approval testing*. Una sola comparación revisa todo el contenido: cualquier cambio, aunque sea un espacio, la pone en rojo.

### Texto y bytes
Un archivo en disco son **bytes**. Para leerlo como texto, Python los **decodifica** con una codificación (*encoding*), y para escribir texto los codifica. En UTF-8, la `á` de «Huánuco» ocupa dos bytes: `\xc3\xa1`.

```python
path.read_bytes()                    # los bytes tal cual: b'Hu\xc3\xa1nuco\n'
path.read_text(encoding="utf-8")     # el texto decodificado: 'Huánuco\n'
```

Hay dos decisiones que el código debe tomar a propósito, porque si no las toma, las toma el sistema:

- **La codificación.** Sin `encoding=`, Python usa la del sistema. En Windows, con Python 3.12, es `cp1252`, y leer ese archivo UTF-8 da `'HuÃ¡nuco'`. Desde Python 3.15 la codificación por defecto es UTF-8 en todos los sistemas ([PEP 686](https://peps.python.org/pep-0686/)), pero tu código puede correr en un Python anterior: escribe siempre `encoding="utf-8"`.
- **Los saltos de línea.** Windows termina cada línea con dos caracteres, `\r\n`; Linux y macOS, con uno, `\n`. Al escribir en modo texto en Windows, Python convierte cada `\n` en `\r\n`, salvo que digas otra cosa con `newline="\n"`.

### Los bordes del disco
Como los valores límite del [lab 1.3](../../01-unit-tests/03-test-case-design/README.md), el sistema de archivos tiene sus casos especiales: la carpeta de destino **todavía no existe**, el archivo **ya existe** de una corrida anterior, el archivo está vacío. Una prueba que siempre escribe en una carpeta recién creada y vacía no pasa por ninguno.

## 📚 Documentación
- [Python · `pathlib.Path`: leer y escribir archivos](https://docs.python.org/3/library/pathlib.html#reading-and-writing-files)
- [Python · `open()`: los parámetros `encoding` y `newline`](https://docs.python.org/3/library/functions.html#open)
- [Python · `csv`: lectura con `DictReader`](https://docs.python.org/3/library/csv.html#csv.DictReader)
- [PEP 686 · UTF-8 por defecto desde Python 3.15](https://peps.python.org/pep-0686/)

## 🧭 Escenario

### El código
[`roster.py`](starter/roster.py) ya funciona: el padrón de un club. **No lo cambies.**

| Función | Promete |
|---|---|
| `load_members(path)` | Lee un CSV en UTF-8 con encabezado `name,email,city` y devuelve una lista de diccionarios, uno por miembro |
| `report(members)` | El texto del reporte: cuántos miembros hay por ciudad, en orden alfabético, y el total |
| `write_report(members, path)` | Escribe el reporte en UTF-8, con saltos de línea `\n` en todos los sistemas. Crea las carpetas que falten y reemplaza el archivo si ya existe |

En [`tests/data/`](starter/tests/data/) ya están los datos: [`members.csv`](starter/tests/data/members.csv), con siete miembros, y [`expected_report.txt`](starter/tests/data/expected_report.txt), el reporte correcto para ese CSV, revisado a mano. Tus pruebas van en [`tests/test_roster.py`](starter/tests/test_roster.py).

### Cómo se revisa tu trabajo
La caza de mutantes del [lab 1.2](../../01-unit-tests/02-first-tests/README.md):

| Mutante | Bug sembrado | Lo mata la tarea |
|---|---|---|
| `m1-header-as-member` | Lee la fila del encabezado como si fuera un miembro más | 1 |
| `m2-naive-split` | Separa las columnas en cada coma, sin respetar las comillas | 1 |
| `m3-windows-line-endings` | Escribe los saltos de línea como `\r\n` en todos los sistemas | 2 |
| `m4-cities-unsorted` | Lista las ciudades en el orden en que aparecen, no en orden alfabético | 2 |
| `m5-no-folders` | No crea las carpetas que faltan | 3 |
| `m6-appends` | Agrega el reporte al final del archivo en vez de reemplazarlo | 3 |

## ✅ Tareas

Corre todo con este comando, igual en PowerShell o Bash:

```bash
python -m pytest
```

### Tarea 1 · Datos de prueba junto a las pruebas
**Meta:** leer el CSV de ejemplo y comprobar lo que trae. **La validan:** `[m1-header-as-member]` y `[m2-naive-split]`.

- [ ] Arriba del archivo, define `DATA` con la carpeta `data` que está junto a tu archivo de pruebas.
- [ ] En `test_loads_every_member_from_the_file`: carga `members.csv` y comprueba cuántos miembros hay y que el primero es el diccionario completo de José Pérez.
- [ ] En `test_a_quoted_name_keeps_its_comma`: comprueba el segundo miembro completo. Abre el CSV y mira cómo está escrito su nombre.

🔮 **Predict first:** si escribieras `DATA = Path("tests/data")`, ¿pasarían tus pruebas al correr `python -m pytest` desde `starter/`? ¿Y desde `starter/tests/`?

### Tarea 2 · El archivo esperado
**Meta:** comparar el reporte completo con el archivo esperado. **La validan:** `[m3-windows-line-endings]` y `[m4-cities-unsorted]`.

- [ ] En `test_the_report_matches_the_expected_file`: pide `tmp_path`, escribe el reporte de los miembros de `members.csv` en un archivo dentro de esa carpeta y compáralo con `expected_report.txt`.

🔮 **Predict first:** puedes comparar los dos archivos como texto (`read_text`) o como bytes (`read_bytes`). ¿Cuál de las dos mata a los dos mutantes de esta tarea? ¿Por qué la otra no?

### Tarea 3 · Carpetas que no existen, archivos que sí
**Meta:** probar los dos bordes del disco que `write_report` promete manejar. **La validan:** `[m5-no-folders]` y `[m6-appends]`.

- [ ] En `test_the_report_creates_its_folders`: escribe el reporte en `tmp_path / "reports" / "2026" / "report.txt"`, dos carpetas que todavía no existen, y compáralo con el esperado.
- [ ] En `test_writing_twice_leaves_one_report`: escribe el reporte dos veces en el mismo archivo y compáralo con el esperado.

🔮 **Predict first:** en la segunda prueba, ¿qué pasaría si en lugar de comparar con el archivo esperado solo comprobaras que el archivo contiene `"Total: 7"`?

**Criterio de éxito:** `python -m pytest` dentro de `starter/` termina en verde: 12 pruebas pasan, ninguna se salta.

## 🔍 Command dissection
| Código | Qué hace |
|---|---|
| `Path(__file__).parent` | La carpeta del archivo `.py` que se está ejecutando |
| `path.read_bytes()` | El contenido como `bytes`, sin decodificar ni convertir nada |
| `path.read_text(encoding="utf-8")` | El contenido como texto, decodificado con UTF-8 |
| `path.write_text(texto, encoding="utf-8", newline="\n")` | Escribe el texto en UTF-8 y con `\n` como salto de línea en cualquier sistema |
| `path.parent.mkdir(parents=True, exist_ok=True)` | Crea la carpeta y las que falten antes de ella; si ya existe, no hace nada |

## 💼 En proyectos reales
- **Un archivo esperado se revisa, no se copia.** Si generas el *golden file* corriendo tu código y lo guardas sin leerlo, guardas también sus bugs, y la prueba los protege para siempre. Revísalo línea por línea la primera vez y cada vez que cambie.
- **Git también cambia los saltos de línea.** En Windows, con la opción `core.autocrlf`, Git puede convertir un archivo a `\r\n` al descargarlo, y una comparación de bytes falla en una sola máquina. Un archivo `.gitattributes` fija el formato para todo el equipo; este repositorio usa `* text=auto eol=lf`.
- **Para muchos archivos esperados hay herramientas** como [syrupy](https://pypi.org/project/syrupy/), que guardan los *snapshots* por ti y los actualizan con una opción de la línea de comandos. La idea es la misma de este lab.
- **Los datos de prueba no deben traer datos personales reales.** Usa nombres inventados y dominios reservados para ejemplos, como `example.com`.

## 🚀 Reto extra
Cuando el formato del reporte cambie a propósito, tendrás que actualizar `expected_report.txt`. Haz que tu prueba de la tarea 2, si la variable de entorno `UPDATE_GOLDEN` vale `1`, **escriba** el archivo esperado en vez de compararlo, y después se salte con `pytest.skip`. ¿Por qué conviene que se salte y no que pase?

## 🆘 Pistas
<details><summary>Pista 1 · dirección</summary>

Tarea 1: `DATA` se arma con `Path(__file__)`. Tarea 2: el reporte se escribe con `write_report(load_members(...), salida)`, y la comparación es un solo `assert`.
</details>

<details><summary>Pista 2 · más concreta</summary>

```python
DATA = Path(__file__).parent / "data"

def test_the_report_matches_the_expected_file(tmp_path):
    output = tmp_path / "report.txt"
    write_report(load_members(DATA / "members.csv"), output)
    assert output.read_bytes() == (DATA / "expected_report.txt").read_bytes()
```
</details>

## ✔️ Respuestas verificadas
<details><summary>Ábrelas solo después de terminar las tareas</summary>

Se ejecutó con pytest 9.2.0; el CI verifica cada lab en Python 3.12 y 3.15.

**Tarea 1.** Desde `starter/` pasan, porque `Path("tests/data")` se resuelve desde la carpeta donde corres el comando, y desde ahí existe. Desde `starter/tests/` fallan las cinco pruebas:

```text
E       FileNotFoundError: [Errno 2] No such file or directory: 'tests\\data\\members.csv'
```

Una ruta relativa depende de dónde estés parado; `Path(__file__).parent` depende de dónde está el archivo de pruebas, que no cambia. Con `DATA` armada así, las cinco pruebas pasan desde las dos carpetas.

Las dos pruebas de esta tarea tienen trabajo distinto: la del primer miembro mata solo a `m1`, y la del nombre con coma mata a `m1` y a `m2`. Si el CSV no tuviera un nombre entre comillas, `m2` sobreviviría: los datos de prueba deciden qué bugs puedes ver.

**Tarea 2.** `read_bytes` mata a los dos; `read_text` deja vivo a `m3`. Al leer en modo texto, Python convierte cada `\r\n` en `\n` (lo llama *universal newlines*), así que el reporte con saltos de Windows se lee igual que el correcto. Los bytes no se convierten:

```text
E       AssertionError: assert b'Members by ...nTotal: 7\r\n' == b'Members by ...3\nTotal: 7\n'
E         At index 15 diff: b'\r' != b'\n'
```

El byte 15 es el final de la primera línea, `Members by city`. Esta prueba, sola, mata también a `m1` y a `m2`: una comparación completa ve cualquier cambio en el contenido.

**Tarea 3.** Con `"Total: 7" in ...`, `m6` sobrevive: el archivo tiene el reporte dos veces, y `"Total: 7"` sigue apareciendo. Comparar contra el esperado lo mata; con `-vv`, pytest muestra la diferencia completa, con el reporte repetido:

```text
E       AssertionError: assert b'Members by city\nArequipa: 2\n...Total: 7\nMembers by city\nArequipa: 2\n...Total: 7\n' == b'Members by city\nArequipa: 2\n...Total: 7\n'
```

Y sin las carpetas, `m5` falla al escribir:

```text
E       FileNotFoundError: [Errno 2] No such file or directory: '...\\test_the_report_creates_its_fo0\\reports\\2026\\report.txt'
```
</details>

## 🎤 Autoevaluación
1. ¿Por qué `Path(__file__).parent` es más confiable que una ruta relativa como `"tests/data"`?
2. ¿Qué ventaja tiene un archivo esperado sobre una serie de `assert` línea por línea? ¿Qué riesgo tiene si lo generas con tu propio código?
3. Una prueba que compara un archivo pasa en Linux y falla solo en Windows. ¿Qué dos cosas revisarías primero?
4. ¿Por qué un lector de CSV que hace `línea.split(",")` funciona con casi todos los datos de prueba que escribirías a mano?
5. Tu prueba siempre escribe en una carpeta temporal nueva y vacía. ¿Qué bugs del sistema de archivos no puede ver nunca?

La solución completa está en [`solution/`](solution/).

**Siguiente:** 2.3 · Una base de datos real
