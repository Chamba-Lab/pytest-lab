# Lecciones

Lecciones de construir y revisar los labs de este repositorio. Léelas antes de construir el siguiente lab. Las que sirven para cualquier camino de estudio se proponen a StudyForge.

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
