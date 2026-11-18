# 💭 2.1 · Qué cambia al integrar

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema |
|---|---|---|
| 45 min – 1 h | 💭 `concept` | 🎯 `core` |

## 🎯 Objetivos
- Explicar qué puede fallar entre tu código y algo real que una prueba con dobles no puede ver.
- Distinguir el núcleo de un programa de su adaptador, y decidir qué se prueba con dobles y qué con lo real.
- Elegir, para cada dependencia, entre lo real y un doble con criterios concretos.
- Mantener aisladas las pruebas que usan algo real, con una preparación y una limpieza.
- Explicar el costo de las pruebas de integración y por qué conviene tener pocas y enfocadas.

## 💡 Por qué importa
En el bloque 1 aislaste tu código de todo lo real, y las pruebas quedaron rápidas y precisas. Pero un doble solo repite lo que tú creías sobre la dependencia: si el servicio responde con otro formato o la base rechaza tu consulta, la suite sigue en verde y el error llega a producción. Este lab no tiene código para correr: te da el criterio para decidir **qué** probar con lo real en los labs 2.2 a 2.4, y cómo hacerlo sin que las pruebas se ensucien entre sí.

## 🧠 Conceptos
Lee **[CONCEPT.md](CONCEPT.md)**. Parte de una prueba unitaria en verde que esconde un bug de producción, y desde ahí cubre:
- Qué comprueba una prueba de integración: el encaje entre tu código y lo real.
- El núcleo y el adaptador, y qué tipo de prueba va en cada uno.
- Cómo decidir entre lo real y un doble.
- La preparación y la limpieza (*setup* y *teardown*), y cuatro estrategias para aislar pruebas que comparten algo real.
- El costo de lo real.

## 📚 Documentación
- [Martin Fowler · IntegrationTest](https://martinfowler.com/bliki/IntegrationTest.html)
- [Ham Vocke · The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) (sección «Integration Tests»)

## 🎤 Autoevaluación
Responde cada pregunta antes de abrir su respuesta.

1. **Tu suite unitaria está en verde y usa un stub del cliente de pagos. En producción, cada pago falla con `KeyError`. ¿Cómo pudo pasar, y qué prueba lo habría atrapado?**
   <details><summary>💡 Respuesta</summary>

   El stub devuelve lo que quien escribió la prueba creía que devolvía el servicio. Si el servicio responde con otra estructura (otra clave, otro tipo), el código real falla al leerla, pero el stub nunca la produce. Lo habría atrapado una prueba de integración del adaptador del cliente de pagos contra el servicio real o contra su entorno de prueba: es la que confirma lo que el stub supone.
   </details>
2. **Un compañero propone probar toda la aplicación contra la base de datos real «para estar seguros», sin dobles. ¿Qué le responderías?**
   <details><summary>💡 Respuesta</summary>

   Que la seguridad sale cara: pruebas lentas, que fallan por el entorno y que, al fallar, no dicen si el error está en la lógica o en el acceso a datos. Propondría probar la lógica (el núcleo) con pruebas unitarias y dobles, y el adaptador de la base con pocas pruebas de integración contra una base de prueba real, una por cada forma en que el encaje puede fallar.
   </details>
3. **¿Usarías el servicio real de envío de SMS en tu suite? ¿Y un archivo en una carpeta temporal? Explica el criterio.**
   <details><summary>💡 Respuesta</summary>

   El SMS, no: tiene efectos que no se pueden deshacer (mensajes reales, costo) y depende de la red. En la suite va un doble; el adaptador se prueba contra el entorno de prueba del proveedor o contra un servidor local que lo imite. El archivo temporal, sí: es barato, determinista y desechable, y usarlo de verdad es más simple que escribir un doble.
   </details>
4. **Una prueba crea un cliente en la base de prueba y borra la fila en su última línea. A veces la suite falla con «el cliente ya existe». ¿Por qué?**
   <details><summary>💡 Respuesta</summary>

   Si la prueba falla antes de su última línea (en el Assert, por ejemplo), la limpieza nunca corre y la fila queda en la base. La siguiente corrida encuentra el cliente ya creado. La limpieza tiene que ejecutarse también cuando la prueba falla, o hay que usar una estrategia que no dependa de llegar al final: una base nueva por prueba o una transacción que siempre se deshace.
   </details>
5. **¿Qué diferencia hay entre «uno nuevo por prueba» y «deshacer al terminar»? Da un caso para cada uno.**
   <details><summary>💡 Respuesta</summary>

   «Uno nuevo por prueba» crea el recurso desde cero para cada prueba (una carpeta temporal, una base SQLite en memoria): no hay nada que limpiar, pero crearlo debe ser barato. «Deshacer al terminar» reutiliza el recurso y envuelve cada prueba en una transacción que se deshace al final: sirve cuando crearlo es caro, como una base de datos de un servidor con muchas tablas, y solo para lo que tiene transacciones.
   </details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué sigue sin estar claro?

**Siguiente:** [2.2 · Archivos reales](../02-real-files/README.md)
