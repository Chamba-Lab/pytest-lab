# Lecciones

Lecciones de construir y revisar los labs de este repositorio. Léelas antes de construir el siguiente lab. Las que sirven para cualquier camino de estudio se proponen a StudyForge.

Las secciones de cada lab usan los IDs de la primera versión del bloque 1: el viejo 1.3 es hoy el 1.3 y parte del 1.4, el viejo 1.4 es el 1.5 y el viejo 1.5 es el 1.6 (la inestabilidad pasó al 4.1). La reconstrucción tiene su propia sección al final.

## Entorno
- **Comprueba qué Python corre antes de confiar en un resultado.** En una máquina con Anaconda, `source .venv/Scripts/activate` en Git Bash dejó el entorno fuera del `PATH`: el `cygpath` de Anaconda convirtió la ruta a `/cygdrive/d/...`, que Git Bash no entiende, y `python` siguió siendo el de Anaconda (con otro pytest y decenas de plugins: la caza tardó 14 s en vez de 2 s). `python -c "import sys; print(sys.prefix)"` debe mostrar `.venv`; por eso está en `SETUP.md`. Para verificar desde un agente, antepón `.venv/Scripts` al `PATH` de forma explícita.

## Lab 1.2
- **La salida de un pytest hijo trae símbolos que la consola de Windows no tiene.** `approx` imprime `±`; el proceso hijo escribía en cp1252 y la caza leía UTF-8, con un `UnicodeDecodeError` en un hilo (aviso `PytestUnhandledThreadExceptionWarning`). La caza fija `PYTHONIOENCODING=utf-8` para el hijo y decodifica con `errors="replace"`. Cualquier prueba que lance pytest u otro Python como subproceso debe hacer lo mismo.
- **Los stubs con `pytest.skip` hacen posible la comprobación progresiva.** Con `skip`, el código real "pasa" desde el inicio (el guardián está en verde) y cada tarea pone en verde solo sus mutantes; se comprobó tarea por tarea en una copia limpia.
- **El guardián evita la trampa inversa.** Una prueba con una expectativa equivocada falla contra el código real y "mataría" a todos los mutantes; por eso la caza exige primero que la suite pase con el código real.
- **Los datos deciden si una prueba distingue el bug.** Con los empatados ya en orden alfabético en el diccionario, el mutante del orden de inserción sobrevive; está en el lab como trampa verificada.

## Lab 1.3
- **Los conteos de pruebas no dicen si un starter está roto.** Una solución parametrizada corre legítimamente más casos que su starter (15 frente a 18), y el verificador de StudyForge 0.1.0 avisaba en falso. La señal real son los *errors* del reporte JUnit (un módulo que no importa). Se corrigió en StudyForge y se copió a `tools/verify.py`.
- **Verifica también lo que "suena obvio".** Iba a escribir que una marca mal escrita pasa "en silencio"; al correrlo, pytest emite `PytestUnknownMarkWarning: Unknown pytest.mark.slwo - is this a typo?`. El README dice lo que pasó de verdad.
- **Una variante "bug corregido" valida un `xfail` estricto.** Con `xfail` no estricto, la suite queda en verde (`8 passed, 1 xpassed`) cuando alguien arregla el bug; la variante `f1` lo convierte en un fallo que el aprendiz ve.
- **La salida de la caza mostraba todo el objeto `CompletedProcess`.** La introspección de `assert` lo expande; asignar `exit_code = result.returncode` antes del `assert` deja el mensaje limpio.

## Lab 1.4
- **Una suite completa mata a un mutante por más de un lado.** Al aislar las pruebas resultó que el mutante del reloj real muere con la prueba del último día y también con la de recordatorios. La respuesta verificada distingue "qué prueba de esta tarea" de "qué pruebas de la suite".
- **Los stubs no deben pedir fixtures que aún no existen.** `def test_x(library)` sin la fixture da *error* en la preparación, no `skip`. El verificador lo marcaría como rojo por la razón equivocada.
- **Trampas verificadas que vale la pena reutilizar:** `scope="module"` sobre `tmp_path` da `ScopeMismatch`; una ruta fija arrastra estado entre corridas (5 fallos en la primera, 6 en la segunda); un `Mock()` sin `spec` deja vivo al mutante que llama a un método inexistente.

## Lab 1.5
- **Un exprés que termina "gratis" esconde el multiplicador.** El mutante `× 3` sobrevive con 100% de cobertura porque la única prueba de exprés cae en el caso del envío gratis. Se diseñó así a propósito y se comprobó en PowerShell, en el orden de la guía.
- **Las semillas de hash que fallan dependen de la versión de Python.** Con 3.12, `PYTHONHASHSEED=0` falla y `2` pasa; la guía lo dice y pide buscar las propias en otra versión.
- **`--durations` con `-vv` no muestra "todas":** sigue limitado a N y además incluye las fases de preparación y cierre. Se corrigió la frase después de correrlo.

## Proyecto 1.P
- **La lista de mutaciones encontró dos huecos en mi propia suite.** M07 (el deudor alfabético en vez del mayor) sobrevivía porque los datos de la prueba no separaban los dos criterios; se cambiaron los nombres. Escribir la lista mientras se diseñan las pruebas, y correrla, es lo que hace honesta la tabla de `REVIEW.md`.
- **Un entorno de pruebas demasiado cómodo esconde bugs.** El script de mutaciones fijaba `PYTHONIOENCODING=utf-8` para sus procesos y así la mutación que quita la salida UTF-8 (M12) pasaba. Sin esa variable, en Windows, la prueba A8 la atrapa. La aceptación no fija variables de entorno de Python a propósito: es de caja negra.
- **Ninguna suite sola basta.** Unitarias y aceptación ven mutaciones distintas (M08 y M12 solo la aceptación; M05, M07, M10 y M13 solo las unitarias). La tabla lo deja a la vista.
- **Una prueba unitaria que compara con la misma constante que el código no protege el valor** (M08: `EXIT_INPUT_ERROR`). Cuando el número es parte del contrato, se escribe literal en la aceptación.

## Revisión con ojos de aprendiz (bloque 1)
- **Un revisor sin el contexto de quien construyó encuentra lo que el autor ya no ve.** Un subagente leyó todo como aprendiz y encontró 22 puntos. Los conteos y los enlaces estaban bien; los problemas eran de recorrido. El ejemplo de salida del `BRIEF.md` contradecía su propio CSV, el proyecto usaba `capsys` sin haberlo enseñado, una tarea de 1.3 no se podía validar sin la siguiente, y el "rompe una copia" del `REVIEW` no funcionaba porque la aceptación siempre prueba la `reference/` vecina.
- **Las pistas al lado de "Predice primero" son respuestas.** Los avisos `[!WARNING]` que explicaban la trampa, los "Qué deberías ver" visibles en la exploración y un `skip("… with pytest.approx")` en el starter regalaban la predicción. Ahora la salida esperada de las exploraciones va en `<details>` y los avisos que revelaban algo se quitaron.
- **Ver de verdad lo que dice un revisor.** El revisor afirmó que en el orden real del starter la fuga de `os.environ` rompe la caza y no una prueba vecina. Al correrlo resultó peor de lo que decía el README: el guardián falla y bloquea a los 7 mutantes. La respuesta verificada usa ahora esa salida real.

## Reconstrucción del bloque 1 (StudyForge 1.1)
- **Un dato de otra tarea puede matar al mutante de un límite por casualidad.** Con el mínimo de 12 caracteres, `Password1234` (el caso de la regla `common`) medía justo 12 y mataba al mutante `<=` en la tarea 1. La comprobación progresiva lo mostró: la tarea 2 no tenía nada que matar. Se bajó el mínimo a 10. Al diseñar mutantes de límites, revisa qué datos de las otras tareas caen sobre el límite.
- **Una revisión de estructura puede contradecir a su propia tarea.** La primera versión de `test_structure.py` en 1.4 prohibía `Catalog(` en todo el archivo, pero la tarea 1 pide escribir ahí las fixtures. Se cambió por una revisión con `ast` que mira solo las funciones `test_*`. Corre cada tarea por separado, no solo la solución completa.
- **En modo estricto, pytest 9 también revisa las marcas del `-m`.** `-m "not slow"` con `slow` sin registrar termina con `ERROR: Unknown marker(s) in '-m' expression: slow`. La caza de 1.4 no puede filtrar con `-m` antes de la tarea 3, así que deja fuera la prueba lenta con `-k`. Y el error se volvió una trampa verificada.
- **`-o pythonpath=<ruta absoluta>` no funcionó en Windows** (las pruebas no encontraban el paquete); con una ruta relativa sí. La caza del proyecto vacía la opción (`-o pythonpath=`) y pasa la aplicación por `PYTHONPATH`, que funciona igual en los dos sistemas.
- **Las respuestas verificadas envejecen con el código de las pruebas.** El README viejo decía que una ruta fija en vez de `tmp_path` daba `5 failed, 1 passed` en la primera corrida; con las pruebas actuales da `6 failed`. Al mover un lab, vuelve a correr cada trampa en lugar de copiar su salida.
- **Explicar antes de practicar cambia qué se puede afirmar.** Al escribir los conceptos de 1.3 con un ejemplo, una frase sonaba bien y era falsa: «un caso que rompe varias reglas pasa aunque una esté rota». Con la comparación exacta de listas, no pasa. El riesgo real está en las funciones que solo responden válida o inválida. Los ejemplos de la sección 🧠 también se verifican.

## Revisión con ojos frescos del bloque reconstruido (StudyForge 1.2)
- **Explicar antes de practicar llevó las trampas a los Conceptos.** Cinco labs respondían sus propias predicciones en la sección 🧠, que el aprendiz lee antes: que `match` es una expresión regular, qué pasa sin `conftest.py`, sin registrar una marca o con un `Mock()` sin `spec`. Los Conceptos dicen qué hace cada cosa; lo que sale mal queda para la respuesta verificada.
- **Lo que el proyecto necesita también se enseña.** `Decimal` se nombraba como «aprendido en 1.2» y no estaba; `capsys`, la fixture que devuelve una función y el archivo con BOM se daban por sabidos. Ahora `Decimal` está en 1.2 y lo demás en «Lo nuevo de este proyecto» del BRIEF.
- **Los textos que cuentan cosas envejecen.** El docstring del starter de 1.4 decía «three tests» con cuatro, y 1.3 decía «dos pruebas escritas» con cinco. Las afirmaciones sobre la configuración («todos los labs traen `strict_markers`») tampoco eran ciertas: ahora todos los `pyproject.toml` las traen.
- **El ruido venía de la plantilla.** Bloques idénticos por shell, la comprobación de carpeta en cada lab, 💼 que resumía los Conceptos y ✔️ que repetía los 👀 de la exploración. StudyForge 1.2 los vuelve opcionales o los prohíbe; aquí se quitaron.

## Lab 2.2
- **Un mutante que solo muere en Windows rompe el CI.** La primera idea era sembrar «escribe sin `newline=`», pero ese bug solo cambia los bytes en Windows; en el CI (Linux) el mutante sobreviviría y la caza de la solución fallaría. El mutante escribe `\r\n` en todos los sistemas, y el README explica que en Windows ese es el comportamiento por defecto. Los mutantes tienen que morir igual en cada sistema donde corre el verificador.
- **La codificación por defecto depende de la versión.** Con Python 3.12 en Windows, `read_text()` sin `encoding` usa `cp1252` y da `'HuÃ¡nuco'`; con 3.15 (PEP 686) da `'Huánuco'`. Por eso no hay mutante de codificación: moriría en un Python y no en otro. Se enseña en Conceptos, con las dos salidas medidas.
- **El archivo esperado va en el starter.** Si el aprendiz lo creara a mano en Windows, su editor podría guardarlo con `\r\n`, y la comparación de bytes fallaría contra el código real (el guardián en rojo) por una razón ajena al lab.

## Lab 2.3
- **El *rollback* por prueba no sirve si el código bajo prueba confirma.** El plan era enseñar «una transacción que se deshace en cada prueba», pero `add_score` confirma con `with conn:`, como haría cualquier código real, y una fila confirmada sobrevive al `rollback()` de la limpieza (comprobado en 3.12 y 3.15). El lab usa una base `:memory:` nueva por prueba y deja el *rollback* por prueba en 💼, con su trampa.
- **Una prueba que no mata a ningún mutante es una señal.** La primera prueba de la tarea 1 guardaba un solo puntaje y no mataba a nadie. Con dos puntajes y el mutante del orden (`m1`), la tarea tiene trabajo propio.
- **La predicción no puede estar en los Conceptos de otro lab.** «¿Corre la limpieza si la prueba falla?» era la predicción natural de la tarea 1, pero el 2.1 ya promete que la limpieza debe correr también al fallar. La predicción pasó a ser el `scope="module"` aplicado a la base, y la limpieza al fallar quedó como un hecho en los Conceptos.

## Lab 2.4
- **En Windows, `localhost` costaba medio segundo por petición.** `localhost` se resuelve primero como `::1` (IPv6), donde el servidor de prueba no escucha; el cliente esperaba su `timeout` (0,5 s) y recién después probaba `127.0.0.1`. La suite tardaba 3,6 s y la caza, 46 s. Con `httpserver_listen_address` en `127.0.0.1`, 1,6 s y 21 s.
- **Un puerto cerrado no se rechaza igual en cada sistema.** En Windows la conexión a un puerto cerrado de la propia máquina tarda unos 2 s en rechazarse (medido: 2,03 s), y con un `timeout` menor `requests` lanza `ConnectTimeout`; en Linux (un contenedor `python:3.12-slim`) el rechazo llega en 0,02 s. Un mutante que solo capturara `Timeout` moriría en Linux y viviría en Windows, así que el mutante de red quita todo el manejo de errores.
- **pytest-httpserver responde 500 a lo que no esperaba.** Una prueba de «el servicio responde 500» pasa sin registrar ninguna respuesta. Es la trampa de la tarea 2, y `check_assertions()` la delata.

## Lab 2.5
- **Un archivo de otra herramienta puede romper testcontainers.** En la máquina donde se construyó, un `~/.testcontainers.properties` viejo de Testcontainers Desktop traía `tc.host=tcp\://127.0.0.1\:63573` (formato de Java, con `\:`). testcontainers para Python lo usa antes que `DOCKER_HOST`, no quita las barras, y las pruebas de PostgreSQL terminaban con `DockerException: Invalid bind address format`. Como el ping de Docker sí respondía, no se saltaban: daban *error*. Se verificó con `USERPROFILE` apuntando a una carpeta vacía, sin tocar el archivo de la máquina, y la pista quedó en el 🆘 del lab.
- **`testcontainers.postgres` está obsoleto en 4.15.** El import correcto es `testcontainers.community.postgres`; el viejo emite `DeprecationWarning`. Se corrió con `-W error::DeprecationWarning` para confirmarlo.
- **El *rollback* por prueba sí funciona en la demo**, al revés que en el 2.3: `Contacts` nunca confirma, y en PostgreSQL hasta el `CREATE TABLE` es parte de la transacción, así que el `rollback()` de la limpieza borra la tabla.
- **En el CI el electivo corre con Docker de verdad.** `verify.py` lo corre sin sus librerías (las pruebas de PostgreSQL se saltan); un paso aparte instala `demo/requirements.txt` y falla si alguna prueba se salta.

## Proyecto 2.P
- **Una prueba que confirma por su cuenta esconde el bug de no confirmar.** `with sqlite3.connect(path) as conn:` confirma al salir del bloque, así que la prueba de «sobrevive al cerrar» hacía el `commit` que debía hacer `save_import`, y `m13` sobrevivía. La prueba cierra con `conn.close()`, que no confirma.
- **Compila cada mutante antes de cazar.** Un `\n` mal escapado en el generador dejó a `m05` con un error de sintaxis; la caza lo contó como muerto porque la suite «falló» al importar. El generador ahora se revisa con `ast.parse` sobre cada archivo de cada mutante. Desde Git Bash, los scripts con barras invertidas se escriben con la herramienta de archivos, no con un heredoc: la terminal las colapsa.
- **Las fallas parciales necesitan dos disparadores.** «Guarda al leer» (`m05`) y «guarda al convertir» (`m06`) son el mismo error en dos momentos; la prueba de la línea inválida solo ve al primero. Y con la línea de EUR antes que la de USD, la prueba del servicio que falla no ve a ninguno (comprobado): el orden de los datos decide.
- **El bug más callado deja algo fuera de la tabla que miras.** `m08` anota la importación antes de pedir los tipos de cambio; todas las pruebas de «no guarda nada» pasan, porque no hay gastos. Solo un reintento lo delata.
