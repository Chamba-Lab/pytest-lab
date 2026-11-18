# 🏗️ 1.P · Proyecto: dividir la cuenta

| ⏱️ Duración | 🧪 Tipo | 🧱 Bloque | 🛠️ Stack |
|---|---|---|---|
| 3–4 h escribir la suite · 1–2 h revisar | 🏗️ `project` | 1 · Pruebas unitarias | Python 3.12+ · pytest 9.2 · pytest-cov 7.1 |

## 🎯 Objetivos
- Escribir desde cero la suite unitaria de una aplicación real de tres módulos, a partir de su contrato.
- Aplicar todo el bloque en un mismo lugar: casos por clase y en los límites, tablas parametrizadas, fixtures compartidas, `tmp_path` y `capsys`, y la cobertura de ramas.
- Probar dinero sin perder un céntimo: `Decimal` comparado exacto y repartos que suman cero.
- **La pregunta del dominio:** después de repartir, ¿la suma de lo que se debe es exactamente cero? Tu suite tiene que darse cuenta el día en que no lo sea.

## 📍 Dónde correr los comandos
Con el entorno virtual activo (el de la raíz del repositorio ya trae pytest y pytest-cov), cada parte se corre desde su carpeta:
- **Tu suite:** dentro de `your-suite/`.
- **La caza que acepta el proyecto:** dentro de `acceptance/`.
- **La aplicación y la suite de referencia:** dentro de `reference/`.

Comprueba dónde estás:

PowerShell:

```powershell
Get-Location
```

Bash:

```bash
pwd
```

## 🛣️ Dos formas de usar este proyecto
| Camino | Qué haces | Tiempo |
|---|---|---|
| 🔨 **Construir y comparar** | Lee [BRIEF.md](BRIEF.md), escribe tu suite en `your-suite/tests/` (en tu rama o fork), pásale la caza de `acceptance/` y después lee [REVIEW.md](REVIEW.md) para comparar tu suite con la de `reference/` | 3–4 h |
| 🔍 **Solo revisar** | Lee la suite de `reference/tests/` guiado por [REVIEW.md](REVIEW.md), pásale la caza y rómpela: borra una prueba y mira qué mutante sobrevive | 1–2 h |

**Recomendación:** si resolviste los labs 1.2 a 1.5 sin mirar las soluciones, construye: aquí nadie te dice qué casos elegir, y eso es justo lo que el bloque te enseñó. Si tienes poco tiempo, revisa, pero haz al menos tres veces el ejercicio de «borra una prueba».

### Mirar la aplicación funcionando
Antes de probarla, úsala. Dentro de `reference/`:

PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m splitbill balances examples/trip.csv
python -m splitbill settle examples/trip.csv
Remove-Item Env:PYTHONPATH
```

Bash:

```bash
PYTHONPATH=src python -m splitbill balances examples/trip.csv
PYTHONPATH=src python -m splitbill settle examples/trip.csv
```

**Qué deberías ver:**

```text
ana +51.66
beto -40.58
caro +13.92
dani -25.00
```

```text
beto -> ana: 40.58
dani -> caro: 13.92
dani -> ana: 11.08
```

Suma los saldos: 51,66 − 40,58 + 13,92 − 25,00 = 0,00.

### Escribir y correr tu suite
[`your-suite/`](your-suite/) ya trae su [`pyproject.toml`](your-suite/pyproject.toml), que importa la aplicación desde `../reference/src`, y una primera prueba de ejemplo en [`tests/test_money.py`](your-suite/tests/test_money.py). Dentro de `your-suite/`:

PowerShell:

```powershell
python -m pytest
```

Bash:

```bash
python -m pytest
```

Y con la cobertura de ramas (lab 1.6):

PowerShell:

```powershell
python -m pytest --cov=splitbill --cov-branch --cov-report=term-missing
```

Bash:

```bash
python -m pytest --cov=splitbill --cov-branch --cov-report=term-missing
```

`__main__.py` aparece con 0%: solo se ejecuta cuando la aplicación corre como un programa aparte, y eso queda para las pruebas de aceptación del bloque 3.

### Pasarle la caza a tu suite
La caza corre tu suite contra la aplicación real y contra los 12 mutantes del [BRIEF](BRIEF.md#criterios-de-aceptación). Por defecto caza con la suite de referencia; para usar la tuya, nombra su carpeta en `SPLITBILL_SUITE` (la ruta es relativa a `acceptance/`). Dentro de `acceptance/`:

PowerShell:

```powershell
$env:SPLITBILL_SUITE = "../your-suite"
python -m pytest
Remove-Item Env:SPLITBILL_SUITE
```

Bash:

```bash
SPLITBILL_SUITE=../your-suite python -m pytest
```

Con la suite de ejemplo tal cual (una sola prueba), la caza termina así:

```text
12 failed, 1 passed
```

Pasa el guardián (tu suite pasa con la aplicación real) y sobreviven los 12 mutantes. Cada prueba que escribas debería matar a alguno. Cuando tu suite esté completa:

```text
13 passed
```

### Pasarle la caza a la referencia
Sin `SPLITBILL_SUITE`, la caza usa `reference/`. Dentro de `acceptance/`:

PowerShell:

```powershell
python -m pytest
```

Bash:

```bash
python -m pytest
```

```text
13 passed
```

## 👥 Suites de la comunidad
¿Escribiste la tuya? Abre un issue con el enlace a tu fork o rama y la agregamos aquí. No se copian dentro de este repositorio: solo se mantiene una referencia.

## 🔁 Retrospectiva
- ¿Qué mutante te costó más matar, y qué caso te faltaba?
- ¿Qué prueba tuya no mata a ningún mutante? ¿Sobra, o protege algo que la caza no mide?
- ¿Qué lab del bloque conviene repasar?
