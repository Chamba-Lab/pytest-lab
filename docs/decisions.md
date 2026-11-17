# Decisiones

Solo las que alguien podría deshacer sin saber por qué. Si una cambia, se actualiza su entrada en el mismo commit.

## Stack y versiones
- **Python 3.12 o superior, verificado en 3.12 y 3.15.** 3.15 es la estable más reciente (octubre de 2026); 3.12 es lo que muchas máquinas ya tienen. El CI corre ambas para no enseñar nada que dependa de una versión.
- **pytest 9.2.0 y pytest-cov 7.1.0, fijados en `requirements.txt`.** pytest 9 trae la configuración TOML nativa (`[tool.pytest]`) y las opciones strict, que el lab 1.3 enseña como tema 🆕.
- **Solo pytest y pytest-cov.** Nada de plugins extra (por ejemplo, para el orden aleatorio): lo que enseñan se puede mostrar con pytest solo, y cada dependencia es una cosa más que instalar y actualizar.

## Dependencias
- **Estrategia `shared-parent`: un único entorno virtual en la raíz.** Todos los labs usan las mismas dos bibliotecas; quien aprende instala una vez. Cada variante tiene su `pyproject.toml` solo con la configuración de pytest.
- **El proyecto declara sus propias dependencias.** Es atómico (regla de StudyForge): su `pyproject.toml` es completo y no usa código de los labs.

## Diseño del camino
- **Labs de testing al revés, validados con una caza de mutantes.** En un curso de testing, lo que se escribe son pruebas, y una prueba vacía "pasa". Por eso cada reto exige que la suite del aprendiz pase con el código real y falle contra cada mutante. Así se enseña, dentro del propio lab, la idea central del camino: una prueba vale por los bugs que atrapa.
- **Los stubs del starter usan `pytest.skip("TODO …")`, no `pytest.fail`.** Si los stubs fallaran, el código real no pasaría hasta resolver todas las tareas y ningún mutante se podría cazar antes. Con `skip`, cada tarea resuelta pone en verde su mutante (comprobación progresiva).
- **Dinero con `Decimal` en el proyecto, nunca `float`.** Es la pregunta del dominio: la suma de los saldos tiene que ser exactamente cero.
- **Una sola app pequeña por lab** (`grades.py`, `passwords.py`, `loans.py`, `shipping.py`): ninguna crece lab tras lab.
