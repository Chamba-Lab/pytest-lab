# 💭 1.1 · ¿Qué probar y por qué?

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema |
|---|---|---|
| 45 min – 1 h | 💭 `concept` | 🎯 `core` |

## 🎯 Objetivos
- Explicar para qué sirve una prueba automatizada más allá de "encontrar bugs".
- Ubicar una prueba en la pirámide (unitaria, integración, aceptación) y justificar cuántas de cada tipo conviene tener.
- Escribir mentalmente una prueba con la estructura Arrange-Act-Assert.
- Reconocer las tres formas más comunes de una prueba que pasa por la razón equivocada.
- Aplicar la regla "ve fallar cada prueba al menos una vez".

## 💡 Por qué importa
Escribir pruebas es fácil; escribir pruebas que **atrapen bugs** no lo es. Una suite llena de pruebas que no pueden fallar da una tranquilidad falsa: el CI está en verde y el bug llega igual a producción. Este lab te da el vocabulario y el criterio que usarás en todos los demás.

## 🧠 Conceptos
Lee **[CONCEPT.md](CONCEPT.md)**. Cubre:
- Para qué sirven las pruebas: feedback rápido, cambiar sin miedo, documentación, diseño.
- La pirámide de pruebas y el costo de cada nivel.
- Arrange-Act-Assert.
- Qué hace buena a una prueba (rápida, aislada, repetible, auto-verificable, enfocada).
- **La prueba que pasa por la razón equivocada**, y qué es un mutante.
- Qué probar y qué no.

## 📚 Documentación
- [pytest · Get Started](https://docs.pytest.org/en/stable/getting-started.html)
- [Martin Fowler · TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)

## 🎤 Autoevaluación
Responde cada pregunta antes de abrir su respuesta.

1. **Tu equipo tiene 300 pruebas de extremo a extremo que tardan 40 minutos, y casi ninguna unitaria. ¿Qué problema concreto tienen y qué harías?**
   <details><summary>💡 Respuesta</summary>

   Feedback lento y caro: nadie corre 40 minutos de pruebas antes de cada cambio, así que los errores se descubren tarde. Además, cuando una falla, no dice qué pieza se rompió. Movería la mayor parte de la lógica a pruebas unitarias (milisegundos, señalan la pieza exacta) y dejaría pocas de extremo a extremo para los recorridos principales.
   </details>
2. **Una prueba recorre los pedidos de un cliente con un `for` y comprueba que cada uno tenga fecha. Siempre pasa. ¿Por qué podría no valer nada?**
   <details><summary>💡 Respuesta</summary>

   Si la lista de pedidos viene vacía, el `for` no ejecuta ningún `assert` y la prueba pasa sin comprobar nada. Hay que verificar primero que la lista no está vacía (o que tiene la cantidad esperada) antes de recorrerla.
   </details>
3. **Escribiste una prueba y pasó a la primera. ¿Qué haces antes de confiar en ella?**
   <details><summary>💡 Respuesta</summary>

   La veo fallar: rompo a propósito el código que prueba (cambio un operador, devuelvo otro valor) y confirmo que se pone roja; luego restauro el código. Si no se pone roja, la prueba no está comprobando lo que creo.
   </details>
4. **¿Qué diferencia hay entre probar comportamiento y probar detalles internos? Da un ejemplo.**
   <details><summary>💡 Respuesta</summary>

   El comportamiento es lo que el código promete hacia afuera ("una compra de 100 tiene 10% de descuento"); los detalles internos son cómo lo logra ("llama a `_rule_for` con el total"). Las pruebas de comportamiento sobreviven a una reorganización del código; las de detalles se rompen aunque todo siga funcionando, y terminan estorbando.
   </details>
5. **pytest terminó con el código de salida 5. ¿Qué pasó y por qué debería preocuparte en un CI?**
   <details><summary>💡 Respuesta</summary>

   No se recolectó ninguna prueba (`no tests ran`): por ejemplo, archivos o funciones sin el prefijo `test_`, o una ruta equivocada. Si el CI solo mira "¿falló alguna prueba?", podría darlo por bueno sin haber probado nada; por eso conviene que el código 5 cuente como fallo.
   </details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué sigue sin estar claro?

**Siguiente:** [1.2 · Primeras pruebas](../02-first-tests/README.md)
