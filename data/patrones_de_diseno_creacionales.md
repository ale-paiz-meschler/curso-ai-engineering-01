# Patrones de Diseño de Software: Patrones Creacionales

> **Fuente original:** [Profile.es - Patrones de diseño de software](https://profile.es/blog/patrones-de-diseno-de-software/#Patrones_creacionales)
> **Propósito para el curso:** Material de apoyo teórico y conceptual para el estudio de arquitectura de software y buenas prácticas de programación.

---

## Introducción a los Patrones de Diseño

Los patrones de diseño son soluciones habituales y estandarizadas a problemas recurrentes en el desarrollo de software. No son fragmentos de código listos para copiar y pegar, sino plantillas o planos conceptuales que se pueden adaptar para resolver un problema de diseño particular en nuestro código.

### Ventajas principales de usar patrones de diseño:
- **Estandarización:** Proveen un vocabulario común y ampliamente entendido entre desarrolladores.
- **Eficiencia:** Evitan "reinventar la rueda", permitiendo aplicar soluciones ya probadas y optimizadas.
- **Mantenibilidad:** Fomentan un código más limpio, modular y fácil de escalar o refactorizar.

Los patrones de diseño clásicos (definidos originalmente por el *Gang of Four* o GoF) se dividen principalmente en tres categorías:
1. **Patrones Creacionales**
2. **Patrones Estructurales**
3. **Patrones de Comportamiento**

---

## Patrones Creacionales

Los **patrones creacionales** centran su atención en los mecanismos de creación e instanciación de objetos. Su objetivo principal es abstraer el proceso de creación de objetos para que el sistema sea independiente de cómo dichos objetos son creados, compuestos y representados.

Dentro de esta categoría se encuentran los cinco patrones principales:

### 1. Abstract Factory (Fábrica Abstracta)
- **Propósito:** Permite producir familias de objetos relacionados o dependientes (por ejemplo, componentes de interfaz de usuario de diferentes sistemas operativos) sin especificar sus clases concretas de manera directa.
- **Cuándo usarlo:** Cuando el código de la aplicación necesita trabajar con diversas familias de productos relacionados, pero no queremos que dependa de las clases concretas de dichos productos.

### 2. Builder (Constructor)
- **Propósito:** Permite crear objetos complejos paso a paso utilizando el mismo código de construcción.
- **Cuándo usarlo:** Es ideal cuando un objeto requiere un proceso de creación complejo que involucre múltiples pasos o combinaciones de parámetros opcionales (evitando los molestos constructores telescópicos con muchos argumentos).

### 3. Factory Method (Método de Fábrica)
- **Propósito:** Proporciona una interfaz para crear objetos en una superclase, pero permite a las subclases alterar el tipo de objetos que se crearán.
- **Cuándo usarlo:** Cuando una clase no puede anticipar de antemano la clase de los objetos que debe crear, delegando la responsabilidad de la instanciación en sus subclases.

### 4. Prototype (Prototipo)
- **Propósito:** Permite clonar objetos ya existentes sin acoplar el código a sus clases específicas.
- **Cuándo usarlo:** Cuando la creación directa de un objeto es costosa en términos de recursos o tiempo (por ejemplo, consultas pesadas a bases de datos o lectura de archivos) y resulta más eficiente duplicar un modelo base preexistente.

### 5. Singleton (Instancia Única)
- **Propósito:** Garantiza que una clase tenga una única instancia en toda la aplicación y proporciona un punto de acceso global a ella.
- **Cuándo usarlo:** Muy utilizado para gestionar recursos centralizados compartidos, como conexiones a bases de datos, gestores de configuración o sistemas de logging.

---
