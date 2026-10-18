# Patrones de Diseño: Creacionales y Estructurales (con enfoque en TypeScript y Casos Reales)

Un **patrón de diseño** no es más que una receta o recomendación comprobada para resolver problemas comunes en el desarrollo de software. Ayudan a incrementar la calidad del código, haciéndolo más mantenible, desacoplado, escalable y tolerante a cambios, sirviendo como herramientas atemporales independientes de los frameworks y librerías del momento.

---

## 1. Clasificación General
* **Patrones Creacionales:** Resuelven problemas relacionados con la creación e instanciación de objetos.
* **Patrones Estructurales:** Resuelven problemas de composición y agregación de clases y objetos.
* **Patrones de Comportamiento:** Gestionan las responsabilidades y la interacción entre objetos.
* **Patrones de UI:** Enfocados en resolver problemas específicos de la capa de presentación.

---

## 2. Patrones Creacionales

### A. Factory Method
El patrón *Factory Method* permite encapsular la lógica de creación de objetos dentro de subclases (*Concrete Creators*), descargando de dependencias directas al cliente que las consume.

* **Estructura teórica:**
  * Una interfaz o clase abstracta (`Creator`) define un método de fábrica (`factoryMethod()`).
  * Las clases concretas (`ConcreteCreator`) implementan este método para devolver instancias de productos específicos (`ConcreteProduct`) que comparten una interfaz común (`Product`).
* **Ventajas:**
  * **Principio Open-Close:** Permite añadir nuevos tipos de productos sin modificar el código cliente existente.
  * **Encapsulamiento de dependencias:** Si un producto requiere configuraciones o servicios externos, su inicialización se centraliza en la fábrica.

#### Ejemplo de aplicación real (Logging por Entornos):
* **Problema:** Registrar eventos y errores en producción en una plataforma Cloud (ej. Application Insights) pero mostrarlos en la consola del navegador durante el desarrollo local (`DEV`).
* **Implementación:**
  1. Se define una interfaz `Logger` con un método `log(message: string)`.
  2. Se crean implementaciones como `AppInsightsLogger` y se aprovecha el objeto `console` global para desarrollo.
  3. Una clase factoría (`LoggerCreator`) evalúa el entorno de ejecución mediante un diccionario y retorna el creador y la instancia de logger correspondiente de forma totalmente transparente para el cliente.

---

### B. Factory Method con Parámetros
Una variante del patrón de fábrica donde un único método de creación recibe un parámetro (como un enum, identificador o modo) para decidir dinámicamente qué tipo concreto de objeto instanciar.

* **Ejemplo de aplicación real (Componentes dinámicos de formularios):**
  * **Problema:** Validar y modificar campos de formularios de manera dinámica en tiempo de ejecución (mostrando una caja de texto, un área de texto o un menú desplegable según el tipo de dato).
  * **Implementación:** Se utiliza un componente contenedor que actúa como creador y, basándose en una propiedad de entrada (`mode`), consulta un diccionario de mapeo para renderizar y enlazar dinámicamente el componente visual correcto (`TextComponent`, `TextAreaComponent`, `SelectComponent`) que implementa una interfaz común (`IComponent`).

---

### C. Singleton
Garantiza que una clase posea una única instancia en toda la aplicación y proporciona un punto de acceso global y centralizado a ella.

* **Funcionamiento:** 
  * El constructor de la clase se declara como privado.
  * La clase expone un método estático (`build()` o `getInstance()`) que comprueba si la instancia ya fue creada; si no existe, la inicializa, y en llamadas posteriores devuelve siempre la misma referencia almacenada.
* **Precaución:** Debe usarse con criterio para evitar acoplamiento excesivo o efectos colaterales inesperados si múltiples partes del sistema modifican su estado compartido de forma desordenada.