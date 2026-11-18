# Decisiones

Solo las que alguien podría deshacer sin saber por qué. Si una cambia, se actualiza su entrada en el mismo commit.

## Reconstrucción del bloque 1 (18 nov 2026, StudyForge 1.1)
- **Se rehízo el bloque 1 con IDs y carpetas nuevas** (`01-fundamentals` → `01-unit-tests`), aunque los IDs se congelan en `built`. La primera revisión, de alguien que conoce testing, encontró un sílabo difícil de leer, conceptos listados sin presentar y un bloque que mezclaba unitarias, aceptación, cobertura e inestabilidad. No había issues de feedback, forks ni labs en `done`, así que el cambio no rompía el trabajo de nadie.
- **El camino completo tiene cuatro bloques, uno por nivel de la pirámide más la calidad de la suite.** El bloque 1 se queda en las unitarias; integración y aceptación tienen sus bloques. Las pruebas inestables pasaron al 4.1, junto al CI, donde duelen en la práctica.
- **Se reutilizó el código verificado** (`grades.py`, `passwords.py`, `loans.py`, `shipping.py`, `splitbill`) y se rehicieron la explicación y el reparto de temas. Solo 1.4 tiene un dominio nuevo (`cart.py`), porque organizar la suite necesitaba pruebas que repitieran la preparación.
- **El mínimo de largo de `passwords.py` bajó de 12 a 10.** Con 12, `Password1234` (la contraseña común del caso `common`) mide justo el límite y mataba por casualidad al mutante del límite en la tarea 1; la tarea 2, que enseña los límites, no tenía nada que demostrar. El bug conocido del tabulador (y su `xfail`) se quitó: `xfail` y la configuración pasaron a «En proyectos reales» de 1.4.
- **El proyecto también va al revés:** la aplicación está terminada y el aprendiz escribe la suite. Antes pedía construir la aplicación y sus pruebas, y nada calificaba las pruebas: una suite floja «aprobaba» si la aplicación funcionaba. Ahora una caza de mutantes de toda la aplicación (`acceptance/`) acepta la suite. Las pruebas de caja negra de la CLI se quitaron; quedan en la historia de git para el bloque 3.
- **Las pruebas de la CLI de la referencia escriben el código de salida como `2`, no como `EXIT_INPUT_ERROR`.** El mutante `m08` (código 1) sobrevivía porque la prueba y la constante cambiaban juntas.

## Stack y versiones
- **Python 3.12 o superior, verificado en 3.12 y 3.15.** 3.15 es la estable más reciente (octubre de 2026); 3.12 es lo que muchas máquinas ya tienen. El CI corre ambas para no enseñar nada que dependa de una versión.
- **pytest 9.2.0 y pytest-cov 7.1.0, fijados en `requirements.txt`.** pytest 9 trae la configuración TOML nativa (`[tool.pytest]`) y las opciones strict, que todos los labs usan desde el 1.3; el 1.4 enseña a registrar marcas en ella.
- **Solo pytest y pytest-cov.** Nada de plugins extra (por ejemplo, para el orden aleatorio): lo que enseñan se puede mostrar con pytest solo, y cada dependencia es una cosa más que instalar y actualizar.

## Dependencias
- **Estrategia `shared-parent`: un único entorno virtual en la raíz.** Todos los labs usan las mismas dos bibliotecas; quien aprende instala una vez. Cada variante tiene su `pyproject.toml` solo con la configuración de pytest.
- **El proyecto declara sus propias dependencias.** Es atómico (regla de StudyForge): su `pyproject.toml` es completo y no usa código de los labs.

## Diseño del camino
- **Labs de testing al revés, validados con una caza de mutantes.** En un curso de testing, lo que se escribe son pruebas, y una prueba vacía "pasa". Por eso cada reto exige que la suite del aprendiz pase con el código real y falle contra cada mutante. Así se enseña, dentro del propio lab, la idea central del camino: una prueba vale por los bugs que atrapa.
- **Los stubs del starter usan `pytest.skip("TODO …")`, no `pytest.fail`.** Si los stubs fallaran, el código real no pasaría hasta resolver todas las tareas y ningún mutante se podría cazar antes. Con `skip`, cada tarea resuelta pone en verde su mutante (comprobación progresiva).
- **Dinero con `Decimal` en el proyecto, nunca `float`.** Es la pregunta del dominio: la suma de los saldos tiene que ser exactamente cero.
- **Una sola app pequeña por lab** (`grades.py`, `passwords.py`, `cart.py`, `loans.py`, `shipping.py`): ninguna crece lab tras lab.
