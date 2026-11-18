# 📖 Glosario · Testing en Python con pytest

Los términos del oficio, como los vas a encontrar en la documentación y en un equipo. Cada uno tiene una línea aquí y su explicación completa en el lab que lo enseña.

## Bloque 1 · Pruebas unitarias
| Término | Qué es | Se enseña en |
|---|---|---|
| Test (prueba automatizada) | Código que ejecuta tu código con datos conocidos y compara el resultado con el esperado | [1.1](labs/01-unit-tests/01-what-is-a-test/CONCEPT.md) |
| Test suite (suite) | El conjunto de pruebas de un proyecto | [1.1](labs/01-unit-tests/01-what-is-a-test/CONCEPT.md) |
| Unit test (prueba unitaria) | Prueba de una función o una clase, aislada del resto | [1.1](labs/01-unit-tests/01-what-is-a-test/CONCEPT.md) |
| Integration test (prueba de integración) | Prueba de varias piezas juntas, o de una pieza con algo real (un archivo, una base de datos) | [1.1](labs/01-unit-tests/01-what-is-a-test/CONCEPT.md) |
| Acceptance / end-to-end test (prueba de aceptación) | Prueba del sistema completo, como lo usa una persona | [1.1](labs/01-unit-tests/01-what-is-a-test/CONCEPT.md) |
| Test pyramid (pirámide de pruebas) | La recomendación de tener muchas pruebas unitarias y pocas de extremo a extremo | [1.1](labs/01-unit-tests/01-what-is-a-test/CONCEPT.md) |
| Arrange, Act, Assert (AAA) | Las tres partes de una prueba: preparar, actuar y comprobar | [1.1](labs/01-unit-tests/01-what-is-a-test/CONCEPT.md) |
| Mutant (mutante) | Una copia del código con un bug pequeño sembrado; una buena suite lo «mata» (falla contra él) | [1.1](labs/01-unit-tests/01-what-is-a-test/CONCEPT.md) |
| Test discovery / collection (recolección) | Cómo pytest encuentra las pruebas: archivos y funciones que empiezan con `test_` | [1.2](labs/01-unit-tests/02-first-tests/README.md) |
| Assertion introspection | Cuando un `assert` falla, pytest muestra los valores de cada lado | [1.2](labs/01-unit-tests/02-first-tests/README.md) |
| `pytest.approx` | Comparar decimales con una tolerancia | [1.2](labs/01-unit-tests/02-first-tests/README.md) |
| `pytest.raises` | Comprobar que el código lanza una excepción, y su mensaje | [1.2](labs/01-unit-tests/02-first-tests/README.md) |
| Equivalence partitioning (clases de equivalencia) | Agrupar las entradas que el código trata igual y probar un representativo de cada grupo | [1.3](labs/01-unit-tests/03-test-case-design/README.md) |
| Boundary value analysis (valores límite) | Probar el valor exacto de un límite y el de al lado | [1.3](labs/01-unit-tests/03-test-case-design/README.md) |
| Parametrize (parametrizar) | Escribir una prueba una vez y correrla con una tabla de casos | [1.3](labs/01-unit-tests/03-test-case-design/README.md) |
| Fixture | Una preparación que las pruebas piden por su nombre | [1.4](labs/01-unit-tests/04-organize-suite/README.md) |
| Scope | Cuánto vive una fixture: por prueba, por archivo o por toda la corrida | [1.4](labs/01-unit-tests/04-organize-suite/README.md) |
| `conftest.py` | El archivo donde viven las fixtures que comparten varios archivos de pruebas | [1.4](labs/01-unit-tests/04-organize-suite/README.md) |
| Marker (marca) | Una etiqueta sobre una prueba (por ejemplo, `slow`) para elegir qué correr con `-m` | [1.4](labs/01-unit-tests/04-organize-suite/README.md) |
| Dependency injection (inyección de dependencias) | Que el código reciba lo que necesita (reloj, archivos, servicios) en vez de crearlo | [1.5](labs/01-unit-tests/05-test-doubles/README.md) |
| Test double (doble de prueba) | Un objeto que reemplaza a una dependencia real durante una prueba | [1.5](labs/01-unit-tests/05-test-doubles/README.md) |
| Dummy · Stub · Fake · Spy · Mock | Los cinco tipos de dobles: ocupa un lugar · responde fijo · funciona simple · anota · comprueba las llamadas | [1.5](labs/01-unit-tests/05-test-doubles/README.md) |
| `monkeypatch` | Cambiar una variable de entorno o un atributo durante una prueba y restaurarlo al final | [1.5](labs/01-unit-tests/05-test-doubles/README.md) |
| `tmp_path` · `capsys` | Una carpeta temporal por prueba · capturar lo que el código imprime | [1.5](labs/01-unit-tests/05-test-doubles/README.md) |
| Line coverage (cobertura de líneas) | Qué porcentaje de las líneas ejecutaron las pruebas | [1.6](labs/01-unit-tests/06-coverage/README.md) |
| Branch coverage (cobertura de ramas) | Si cada decisión (`if`) se recorrió por sus dos caminos | [1.6](labs/01-unit-tests/06-coverage/README.md) |
