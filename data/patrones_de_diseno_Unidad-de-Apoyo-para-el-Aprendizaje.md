# Patrones de Diseño de Software: Guía y Fundamentos

En ingeniería de software, un **patrón de diseño** es un marco de referencia probado y comprobado que ha dado buenos resultados en implementaciones previas. No es una solución rígida ni código listo para copiar y pegar, sino una recomendación o modelo (*template*) de cómo resolver un problema recurrente de diseño y desarrollo de manera eficiente.

---

## 1. Elementos esenciales de un patrón de diseño
Todo patrón de diseño formal se compone de cuatro elementos clave:

1. **Nombre del patrón:** Describe el diseño del problema, su solución y sus consecuencias de manera concisa (en una o dos palabras).
2. **Problema:** Explica cuándo se debe aplicar el patrón, su contexto y las condiciones o síntomas de un diseño inflexible que se deben evitar.
3. **Solución:** Describe los elementos que forman el diseño (clases y objetos), sus relaciones, responsabilidades y colaboraciones de forma abstracta.
4. **Consecuencias:** Son las repercusiones, costos y beneficios de aplicar el patrón (impacto en la flexibilidad, extensibilidad, portabilidad y compensaciones en espacio/tiempo).

---

## 2. Tipos de patrones de software
Los patrones de software se clasifican según su nivel de abstracción:
* **Patrones arquitectónicos:** Soluciones al nivel más alto de software y hardware (ej. Modelo-Vista-Controlador).
* **Patrones de diseño:** Soluciones a nivel medio de estructuras de objetos y clases (creacionales, estructurales y de comportamiento).
* **Patrones de programación:** Soluciones de nivel bajo adaptadas a características específicas de un lenguaje de programación.

---

## 3. Patrón Arquitectónico: Modelo-Vista-Controlador (MVC)
El patrón MVC asigna objetos a tres roles fundamentales para desacoplar los datos de la interfaz de usuario:

* **Modelo:** Encapsula la información y la lógica de negocio de la aplicación. Representa el dominio del problema y notifica al controlador cuando sus datos cambian.
* **Vista:** El componente visual con el que interactúa el usuario. Su propósito es mostrar los datos del modelo y capturar las acciones del usuario.
* **Controlador:** Actúa como intermediario o conducto entre la vista y el modelo. Interpreta las acciones del usuario de la vista y actualiza el modelo, o toma los cambios del modelo para refrescar la vista.

---

## 4. Clasificación de Patrones de Diseño (GoF)

### A. Patrones Creacionales
Simplifican la instanciación de objetos, ocultando los detalles de creación y permitiendo que el sistema dependa más de la composición que de la herencia rígida.

* **Ejemplo: Singleton**
  * **Problema:** Garantizar que una clase tenga una única instancia en toda la aplicación y proveer un punto de acceso global y controlado a ella (por ejemplo, un gestor de impresiones o una única conexión a base de datos).
  * **Solución:** 
    * Mantener el constructor privado.
    * Almacenar la única instancia en un atributo privado y estático.
    * Proveer un método público y estático para acceder a dicha instancia.

### B. Patrones Estructurales
Organizan clases y objetos en estructuras más grandes y complejas manteniendo la flexibilidad y eficiencia mediante la composición o la herencia.

* **Ejemplo: Composite**
  * **Problema:** Manejar de forma uniforme objetos primitivos y objetos compuestos jerárquicamente (como componentes gráficos: botones, paneles, imágenes) bajo una misma interfaz o referencia abstracta.
  * **Solución:** Crear una clase abstracta o interfaz base (`Component`) que permita tratar tanto a elementos individuales como a colecciones de ellos de manera idéntica (recursividad estructural).

### C. Patrones de Comportamiento
Se concentran en la comunicación, el flujo de mensajes y la asignación de responsabilidades entre objetos, reduciendo el acoplamiento directo.

* **Ejemplo: Observer**
  * **Problema:** Notificar automáticamente a un grupo dinámico de objetos dependientes (observadores) cuando ocurre un cambio de estado en un objeto principal (sujeto), sin acoplar rígidamente las clases entre sí.
  * **Solución:** Implementar un mecanismo de suscripción donde el sujeto mantiene una lista de observadores y les emite una notificación ante cualquier alteración de su estado.