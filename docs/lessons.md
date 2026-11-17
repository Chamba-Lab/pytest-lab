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
