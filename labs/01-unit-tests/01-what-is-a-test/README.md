# 💭 1.1 · Qué es una prueba y sus tipos

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema |
|---|---|---|
| 45 min – 1 h | 💭 `concept` | 🎯 `core` |

## 🎯 Objetivos
- Explicar qué es una prueba automatizada y para qué sirve, más allá de «encontrar bugs».
- Distinguir una prueba unitaria, una de integración y una de aceptación, y ubicar cada una en la pirámide de pruebas.
- Reconocer las tres partes de una prueba: Arrange, Act, Assert.
- Reconocer las tres formas más comunes de una prueba que pasa por la razón equivocada.
- Explicar qué es un mutante y por qué una buena suite lo mata.

## 💡 Por qué importa
Escribir pruebas es fácil; escribir pruebas que **atrapen bugs** no lo es. Una suite llena de pruebas que no pueden fallar da una tranquilidad falsa: el CI (*continuous integration*, el servidor que corre las pruebas en cada cambio) está en verde y el bug llega igual a producción. Este lab no tiene código para correr: te da el vocabulario y el criterio que vas a usar en todos los demás, y el mapa de hacia dónde va el camino.

## 🧠 Conceptos
Lee **[CONCEPT.md](CONCEPT.md)**. Empieza por un problema (probar a mano no escala) y desde ahí cubre:
- Qué es una prueba automatizada y una suite de pruebas.
- Los tres niveles (unitaria, integración y aceptación) con un mismo ejemplo, y la pirámide de pruebas.
- Arrange-Act-Assert, la estructura de casi toda prueba.
- Qué hace buena a una prueba: rápida, aislada, repetible, autoverificable y enfocada.
- **La prueba que pasa por la razón equivocada**, y los mutantes que la delatan.
- Qué probar y qué no.

Los términos del oficio están reunidos en el [glosario](../../../GLOSSARY.md).

## 📚 Documentación
- [pytest · Get Started](https://docs.pytest.org/en/stable/getting-started.html)
- [Martin Fowler · TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)

## 🎤 Autoevaluación
Responde cada pregunta antes de abrir su respuesta.

1. **Una prueba llama a `total()` con precios escritos en la prueba. Otra abre la tienda en un navegador, agrega productos y lee el total en pantalla. ¿De qué nivel es cada una, y cuál te dice más rápido qué se rompió?**
   <details><summary>💡 Respuesta</summary>

   La primera es unitaria: prueba una función aislada, corre en milisegundos y, si falla, señala exactamente esa función. La segunda es de aceptación (de extremo a extremo): prueba todo el sistema como lo usa una persona; es lenta y, si falla, el problema puede estar en la página, en la base de datos o en el cálculo. La unitaria te dice más rápido qué se rompió; la de aceptación te dice que todo junto funciona.
   </details>
2. **Tu equipo tiene 300 pruebas de extremo a extremo que tardan 40 minutos, y casi ninguna unitaria. ¿Qué problema concreto tienen y qué harías?**
   <details><summary>💡 Respuesta</summary>

   Respuesta lenta y cara: nadie corre 40 minutos de pruebas antes de cada cambio, así que los errores se descubren tarde. Además, cuando una falla, no dice qué pieza se rompió. Movería la mayor parte de la lógica a pruebas unitarias (milisegundos, señalan la pieza exacta) y dejaría pocas de extremo a extremo para los recorridos principales.
   </details>
3. **Una prueba recorre los pedidos de un cliente con un `for` y comprueba que cada uno tenga fecha. Siempre pasa. ¿Por qué podría no valer nada?**
   <details><summary>💡 Respuesta</summary>

   Si la lista de pedidos viene vacía, el `for` no ejecuta ningún `assert` y la prueba pasa sin comprobar nada. Hay que verificar primero que la lista no está vacía (o que tiene la cantidad esperada) antes de recorrerla.
   </details>
4. **Escribiste una prueba y pasó a la primera. ¿Qué haces antes de confiar en ella, y qué tiene que ver eso con los mutantes?**
   <details><summary>💡 Respuesta</summary>

   La veo fallar: rompo a propósito el código que prueba (cambio un operador, devuelvo otro valor) y confirmo que se pone roja; luego restauro el código. Esa copia rota es un mutante: si la prueba no lo mata, no está comprobando lo que creo. La caza de mutantes de los labs siguientes hace eso mismo de forma sistemática.
   </details>
5. **pytest terminó con el código de salida 5. ¿Qué pasó y por qué debería preocuparte en un CI?**
   <details><summary>💡 Respuesta</summary>

   No se recolectó ninguna prueba (`no tests ran`): por ejemplo, archivos o funciones sin el prefijo `test_`, o una ruta equivocada. Si el CI solo mira «¿falló alguna prueba?», podría darlo por bueno sin haber probado nada; por eso conviene que el código 5 cuente como fallo.
   </details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué sigue sin estar claro?

**Siguiente:** [1.2 · Primeras pruebas con pytest](../02-first-tests/README.md)
