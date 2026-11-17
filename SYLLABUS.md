# 🗺️ Sílabo · Testing en Python con pytest

**Meta:** escribir y mantener pruebas automatizadas con criterio profesional: pruebas que fallan por la razón correcta.
**Público:** sabes Python básico (funciones, clases, módulos) y escribiste pocas pruebas o ninguna → puedes probar un proyecto pequeño con criterio profesional.
**Stack:** Python 3.12+ (verificado en 3.12 y 3.15) · pytest 9.2.0 · pytest-cov 7.1.0
**Sesiones:** 1–2 h por lab

**Leyenda**
- Estado: ⬜ `pending` sin construir · 🟨 `built` construido y verificado, esperando a un aprendiz · ✅ `done` resuelto por un aprendiz y con su feedback aplicado
- Tipo de tema: 🎯 `core` el camino · 🔬 `deep-dive` más a fondo · 🔀 `alternative` otra tecnología · ➕ `elective` opcional · 🆕 `modern` pone el camino al día
- Tipo de lab: 🧩 `challenge` starter + solución · 🔭 `exploration` demo guiada · 💭 `concept` sin código · 🏗️ `project` cierra el bloque

## Reglas de diseño
1. **La app más pequeña que hace visible el tema.** Cada lab trae su propio módulo pequeño; ninguno arrastra el dominio del anterior.
2. **Ninguna aplicación crece lab tras lab:** la integración ocurre en el proyecto del bloque.
3. **Cada tema tiene un único lab dueño.**
4. **Labs de testing al revés:** el código de producción ya está terminado; tú escribes las pruebas. Tus pruebas se validan con una **caza de mutantes**: deben pasar con el código real y fallar contra versiones con bugs sembrados.

## Bloque 1 · Fundamentos
Pruebas que fallan por la razón correcta.

| ID | Tema | Tipo de tema | Tipo de lab | Qué se practica | Dueño de / se apoya en | Parte de | Estado |
|---|---|---|---|---|---|---|---|
| [1.1](labs/01-fundamentals/01-why-test/README.md) | ¿Qué probar y por qué? | 🎯 `core` | 💭 `concept` | Pirámide de pruebas, unitaria / integración / aceptación, Arrange-Act-Assert, qué hace buena a una prueba, la prueba que pasa por la razón equivocada | Dueño del vocabulario | — | 🟨 `built` |
| [1.2](labs/01-fundamentals/02-first-tests/README.md) | Primeras pruebas | 🎯 `core` | 🧩 `challenge` | Descubrimiento, `assert` e introspección, `pytest.raises`, `approx`, leer un fallo, `-k` / `-x` / `-v`, caza de mutantes | Dueño del ciclo rojo-verde | Módulo `grades.py` terminado | 🟨 `built` |
| [1.3](labs/01-fundamentals/03-parametrize/README.md) | Parametrizar y organizar | 🎯 `core` 🆕 `modern` | 🧩 `challenge` | `parametrize` e `ids`, `xfail` estricto, marcas propias, configuración nativa `[tool.pytest]` y opciones strict | Dueño de parametrización, marcas y configuración. Se apoya en 1.2 | Módulo `passwords.py` terminado | 🟨 `built` |
| 1.4 | Fixtures y dobles de prueba | 🎯 `core` | 🧩 `challenge` | Fixtures y su `scope`, `conftest.py`, `tmp_path`, `monkeypatch`, fake frente a mock, `create_autospec`, reloj inyectable | Dueño de fixtures y dobles. Se apoya en 1.2 | Módulo `loans.py` terminado | ⬜ `pending` |
| 1.5 | Cobertura y pruebas inestables | 🎯 `core` | 🔭 `exploration` | Cobertura de líneas y de ramas, 100% de cobertura con un bug vivo, pruebas que dependen del orden o del hash, `--lf` / `--sw` / `--durations` | Dueño de cobertura e inestabilidad | `demo/` terminado | ⬜ `pending` |
| 1.P | Proyecto: dividir la cuenta | 🎯 `core` | 🏗️ `project` | Una CLI que reparte gastos entre amigos con `Decimal`; pruebas unitarias y de aceptación de caja negra | Usa 1.1–1.5 | Desde cero | ⬜ `pending` |

## Notas para los siguientes labs
- El entorno es único (`.venv` en la raíz, `requirements.txt`). Cada variante tiene su `pyproject.toml` con `[tool.pytest]` y `pythonpath = ["."]`.
- La caza de mutantes vive en `tests/test_mutant_hunt.py` de cada challenge, con los mutantes en `tests/mutants/<id>/` y un `tests/conftest.py` que antepone el mutante a la ruta de importación según una variable de entorno. Los stubs del starter usan `pytest.skip("TODO …")`. Copia la caza del lab 1.2 y cambia el módulo y la variable (`GRADES_MUTANT` → la del nuevo lab); conserva `PYTHONIOENCODING=utf-8` (ver `docs/lessons.md`).
- Cada trampa del README se verifica en una copia limpia con un script que imprime cuántas pruebas corrieron; los mutantes se generan con un script que exige que cada reemplazo ocurra exactamente una vez.
- 1.3 añadió dos ideas reutilizables: una variante `f*` ("bug corregido") que la suite debe atrapar, para validar `xfail` estricto, y `tests/test_structure.py`, que revisa la organización con `--collect-only` y lee `pyproject.toml` con `tomllib`.
- 1.4 (fixtures y dobles) es dueño de `conftest.py` como lugar de fixtures compartidas; los labs anteriores solo lo usan para la caza. El código bajo prueba debe recibir sus dependencias (almacén, reloj, notificador) para que se puedan reemplazar.
