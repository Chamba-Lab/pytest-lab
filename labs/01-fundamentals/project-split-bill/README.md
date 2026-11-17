# 🏗️ 1.P · Proyecto: dividir la cuenta

| ⏱️ Duración | 🧪 Tipo | 🧱 Bloque | 🛠️ Stack |
|---|---|---|---|
| 4–6 h construir · 1–2 h revisar | 🏗️ `project` | 1 · Fundamentos | Python 3.12+ · pytest 9.2 · pytest-cov 7.1 |

## 🎯 Objetivos
- Consolidar todo el bloque en un programa completo: pruebas unitarias de las reglas, validación parametrizada, la CLI probada con archivos temporales y una suite de aceptación de caja negra.
- Trabajar con dinero sin perder un céntimo: `Decimal`, céntimos enteros y un reparto determinista.
- Distinguir qué protege cada nivel de la pirámide, y ver que ninguno basta solo.
- **La pregunta del dominio:** después de repartir, ¿la suma de lo que se debe es exactamente cero?

## 📍 Dónde correr los comandos
Con el entorno virtual activo (el de la raíz del repositorio ya trae pytest), cada parte se corre desde su carpeta:
- **La referencia y sus pruebas unitarias:** dentro de `reference/`.
- **Las pruebas de aceptación:** dentro de `acceptance/`.

```powershell
Get-Location
```

## 🛣️ Dos formas de usar este proyecto
| Camino | Qué haces | Tiempo |
|---|---|---|
| 🔨 **Construir y comparar** | Lee [BRIEF.md](BRIEF.md), constrúyelo a tu manera en tu rama o fork (por ejemplo en `mine/`), pásale las pruebas de `acceptance/` y después lee [REVIEW.md](REVIEW.md) para comparar tu diseño con `reference/` | 4–6 h |
| 🔍 **Solo revisar** | Corre `reference/`, léela guiado por [REVIEW.md](REVIEW.md), rómpela con la tabla de mutaciones y desafía sus decisiones | 1–2 h |

**Recomendación:** si terminaste los labs 1.2–1.4 sin mirar las soluciones, construye: es donde todo se junta. Si vas justo de tiempo, revisa, pero haz al menos tres filas de "Rómpelo tú".

### Correr la referencia
Dentro de `reference/`:

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

Y sus pruebas unitarias, con cobertura de ramas:

```powershell
python -m pytest --cov=splitbill --cov-branch --cov-report=term-missing
```

```text
src\splitbill\cli.py           30      0      8      0   100%
src\splitbill\ledger.py        67      0     24      0   100%
src\splitbill\money.py         20      0      6      0   100%
46 passed
```

`__main__.py` aparece con 0%: solo se ejecuta como proceso aparte, y eso lo cubren las pruebas de aceptación, no estas.

### Correr las pruebas de aceptación contra cualquier implementación
Dentro de `acceptance/`, contra la referencia (por defecto):

```powershell
python -m pytest
```

```text
15 passed
```

Contra **tu** implementación, nombra el comando que la arranca en `SPLITBILL_CMD`.

PowerShell:

```powershell
$env:SPLITBILL_CMD = "python -m splitbill"   # con tu paquete importable
python -m pytest
Remove-Item Env:SPLITBILL_CMD
```

Bash:

```bash
SPLITBILL_CMD="python -m splitbill" python -m pytest
```

Funciona con cualquier lenguaje: `SPLITBILL_CMD="node mine/cli.js"` también vale. Las pruebas solo miran la salida, stderr y el código de salida.

## 👥 Implementaciones de la comunidad
¿Construiste la tuya? Abre un issue con el enlace a tu fork o rama y la agregamos aquí. No se copian dentro de este repositorio: solo se mantiene una referencia.

## 🔁 Retrospectiva
- ¿Qué diseñaría distinto?
- ¿Qué mutación de [REVIEW.md](REVIEW.md) no esperaba que pasara alguna suite?
- ¿Qué lab del bloque conviene repasar?
