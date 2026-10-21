# DiagnostiPC: sistema experto para el diagnóstico de fallas de hardware y software en computadores personales

**Asesor/a:** Juan J. Ramos Dias  
**Presentado por:** Julian A. Montero Trujillo & Juan C. Bastidas Bernal  
**Institución:** Fundación Escuela Tecnológica de Neiva. Jesús Oviedo Pérez - FET  
**Programa / Asignatura:** Ingeniería de Software - Sistemas Expertos  
**Ubicación y Año:** Rivera - Huila, 2026

---

## Tabla de Contenido

- [Introducción](#introducción)
- [Conformación del equipo de trabajo](#conformación-del-equipo-de-trabajo)
- [Selección del tema y planteamiento del problema](#selección-del-tema-y-planteamiento-del-problema)
  - [Título del proyecto](#título-del-proyecto)
  - [Descripción del problema](#descripción-del-problema)
  - [Usuarios finales](#usuarios-finales)
  - [Justificación como sistema experto](#justificación-como-sistema-experto)
- [Objetivos del proyecto](#objetivos-del-proyecto)
  - [Objetivo general](#objetivo-general)
  - [Objetivos específicos](#objetivos-específicos)
- [Delimitación y alcance del dominio](#delimitación-y-alcance-del-dominio)
  - [Límites del sistema](#límites-del-sistema)
  - [Entradas del sistema](#entradas-del-sistema)
  - [Salidas del sistema](#salidas-del-sistema)
  - [Escala de severidad y prioridad](#escala-de-severidad-y-prioridad)
- [Diseño conceptual del sistema experto](#diseño-conceptual-del-sistema-experto)
  - [Arquitectura general](#arquitectura-general)
  - [Representación del conocimiento](#representación-del-conocimiento)
  - [Ejemplo de razonamiento](#ejemplo-de-razonamiento)
- [Conclusiones](#conclusiones)
- [Referencias](#referencias)

---

## Introducción

Para la asignatura, el grupo debe construir un sistema experto que combine una base de conocimiento escrita en Prolog con una aplicación en Python. Antes de escribir código, este primer entregable define el problema, delimita el dominio y plantea el modelo conceptual con el que el sistema va a razonar, de modo que la implementación de las siguientes etapas tenga un plano claro sobre el cual apoyarse.

Elegimos el diagnóstico de fallas de computadores personales porque es un problema que conocemos de cerca como estudiantes de Ingeniería de Software: compañeros, familiares y personal administrativo nos piden ayuda constantemente cuando su equipo no enciende, se pone lento o muestra una pantalla azul. En este documento presentamos la conformación del equipo, el planteamiento del problema, la justificación de por qué requiere un motor de inferencia, el alcance del dominio con sus entradas, salidas y escala de severidad, y un primer diseño de cómo se representará el conocimiento.

---

## Conformación del equipo de trabajo

El proyecto se desarrollará en pareja. Aunque ambos integrantes trabajaremos con Prolog y con Python, definimos un líder para cada frente con el fin de repartir responsabilidades y tener un responsable claro de cada componente.

### Tabla 1

_Ficha de identificación del equipo_

| Integrante                      | Código       | Correo institucional        | Rol preliminar                                                  |
| :------------------------------ | :----------- | :-------------------------- | :-------------------------------------------------------------- |
| Juan Carlos Bastidas Bernal     | N/A          | juan_bastidasbe@fet.edu.co  | Líder de Ingeniería del Conocimiento y Modelado Lógico (Prolog) |
| Julian Alfonso Montero Trujillo | SOF220251032 | julian_monterotr@fet.edu.co | Líder de Arquitectura de Integración e Interfaz (Python)        |

El líder de Ingeniería del Conocimiento se encargará de recopilar las fuentes, construir la tabla de síntomas y diagnósticos, escribir las reglas en Prolog y validar con casos de prueba que el sistema llegue a conclusiones correctas. El líder de Integración se encargará de la conexión entre Python y SWI-Prolog, la interfaz de preguntas y resultados, el registro de las sesiones y la presentación de la explicación al usuario. Las decisiones sobre las reglas y la escala de severidad se tomarán en conjunto.

---

## Selección del tema y planteamiento del problema

### Título del proyecto

**DiagnostiPC: sistema experto para el diagnóstico de fallas de hardware y software en computadores personales.**

### Descripción del problema

Cuando un computador falla, la mayoría de los usuarios no sabe interpretar lo que ve: un equipo que enciende pero no muestra imagen, una serie de pitidos al arrancar, una pantalla azul con un código o un ventilador que suena más de lo normal. El mismo síntoma puede tener causas muy distintas; por ejemplo, la ausencia de imagen puede deberse a la memoria RAM, a la tarjeta gráfica, a la fuente de poder o simplemente a un cable suelto. Sin una guía, el usuario suele tomar una de tres decisiones poco convenientes: seguir usando un equipo que está a punto de perder sus datos, comprar repuestos que no necesitaba o pagar un servicio técnico por un problema que podía resolver reiniciando un controlador.

En entornos como el nuestro, en Rivera y Neiva, el soporte técnico especializado no siempre está disponible de inmediato, y en las instituciones educativas los monitores de las salas de sistemas suelen ser estudiantes con poca experiencia. El conocimiento para diagnosticar estas fallas existe, pero está concentrado en técnicos con años de práctica y disperso en manuales de fabricantes, tablas de códigos de pitidos y foros. El problema que buscamos resolver es acercar ese razonamiento de diagnóstico a personas que no lo tienen, para que sepan qué le pasa probablemente a su equipo, qué tan urgente es y qué hacer primero.

### Usuarios finales

El sistema está pensado para tres tipos de usuario:

1. **Usuarios domésticos, estudiantes y personal administrativo sin formación técnica**, que necesitan saber si pueden resolver el problema por su cuenta o si deben llevar el equipo a revisión.
2. **Monitores de salas de cómputo y técnicos en formación**, que pueden usar el sistema como apoyo para ordenar su diagnóstico.
3. **Técnicos de soporte**, que quieran una primera clasificación del caso antes de abrir el equipo.

### Justificación como sistema experto

Este problema no se resuelve bien con un software convencional ni con un formulario condicional, por las siguientes razones:

a) **Relación de muchos a muchos:** Un mismo síntoma apunta a varias causas y una misma causa produce varios síntomas. Un árbol de `if/else` fijo se vuelve inmanejable y difícil de mantener; en cambio, las reglas en Prolog se escriben de forma independiente y el motor se encarga de combinarlas.

b) **Encadenamiento lógico:** El diagnóstico se hace por etapas, como lo haría un técnico: primero se identifica la categoría del problema (energía, arranque, video, rendimiento o software) y, a partir de esa conclusión intermedia, se exploran las causas específicas. Esto exige reglas que usen como premisa la conclusión de otras reglas.

c) **Preguntas dinámicas:** Con encadenamiento hacia atrás, el sistema solo pregunta lo necesario para confirmar o descartar la hipótesis que está evaluando. Si el equipo no enciende, no tiene sentido preguntar por ventanas emergentes; un formulario tradicional obligaría a responder todas las preguntas.

d) **Manejo de incertidumbre:** Los síntomas rara vez son concluyentes. El sistema asignará un factor de certeza a cada regla y combinará la evidencia de varias reglas que apoyan el mismo diagnóstico, de modo que el resultado no sea "sí o no", sino "muy probable", "probable" o "posible".

e) **Priorización:** No todas las fallas tienen la misma urgencia. Un disco que empieza a fallar sin copia de seguridad exige acción inmediata, mientras que una pila CMOS agotada puede esperar. El sistema debe ordenar los diagnósticos por severidad y ajustar esa severidad según el contexto.

f) **Explicación:** El usuario podrá preguntar por qué el sistema llegó a una conclusión y verá qué reglas y qué respuestas la sustentan, algo que un software transaccional no ofrece.

Además, el conocimiento queda separado del código de la aplicación: para agregar una nueva falla o corregir una regla basta con modificar la base de conocimiento en Prolog, sin tocar la interfaz en Python.

---

## Objetivos del proyecto

### Objetivo general

Desarrollar un sistema experto basado en reglas, implementado en Prolog e integrado con una aplicación en Python, que diagnostique las fallas más comunes de hardware y software en computadores personales a partir de los síntomas reportados por el usuario, asigne a cada diagnóstico un grado de certeza y un nivel de prioridad, y explique el razonamiento que lo sustenta.

### Objetivos específicos

1. Adquirir el conocimiento de diagnóstico a partir de fuentes técnicas y de la consulta con un técnico de mantenimiento, y representarlo en Prolog mediante hechos y al menos 40 reglas organizadas por categorías de falla.
2. Implementar un mecanismo de inferencia con encadenamiento hacia atrás, factores de certeza y una escala de severidad de cuatro niveles que permita ordenar los diagnósticos por prioridad y ajustar esa prioridad según el contexto del equipo.
3. Integrar la base de conocimiento con una aplicación en Python, mediante la librería PySwip y una interfaz gráfica en Tkinter, que formule las preguntas de forma dinámica, muestre los diagnósticos con sus recomendaciones y presente la explicación del razonamiento.

---

## Delimitación y alcance del dominio

### Límites del sistema

El sistema cubrirá computadores personales de escritorio y portátiles con Windows, que son los más comunes entre nuestros usuarios. Diagnosticará fallas a nivel de componente o de causa probable (por ejemplo, "falla de memoria RAM"), no a nivel de reparación electrónica de la placa.

Quedan fuera del alcance los servidores, los equipos Mac, los periféricos como impresoras, las fallas de red e internet y la recuperación de datos. Cuando la evidencia no alcance para ningún diagnóstico, el sistema lo indicará como "caso no concluyente" y recomendará la revisión de un técnico.

### Entradas del sistema

Las entradas son las respuestas del usuario a preguntas sobre lo que observa en el equipo. Las organizamos en siete grupos lógicos, que además sirven para el encadenamiento por categorías. La Tabla 2 presenta el listado preliminar de 38 variables.

### Tabla 2

_Variables de entrada del sistema agrupadas por categoría_

| Código      | Variable o pregunta al usuario                                                 | Tipo de valor                      |
| :---------- | :----------------------------------------------------------------------------- | :--------------------------------- |
| **Grupo A** | **Energía y encendido**                                                        |                                    |
| A1          | ¿El equipo enciende (luces, ventiladores)?                                     | Sí/No                              |
| A2          | ¿Se apaga de forma repentina, sin aviso?                                       | Sí/No                              |
| A3          | ¿Se reinicia solo de forma inesperada?                                         | Sí/No                              |
| A4          | ¿Percibe olor a quemado o vio chispas?                                         | Sí/No                              |
| A5          | ¿Solo enciende con el cargador conectado? (portátil)                           | Sí / No / No aplica                |
| A6          | ¿Hubo un corte de energía o tormenta eléctrica reciente?                       | Sí/No                              |
| **Grupo B** | **Arranque del equipo**                                                        |                                    |
| B1          | ¿Emite pitidos al encender?                                                    | No / Cortos repetidos / Largos     |
| B2          | ¿Aparece imagen en pantalla al encender?                                       | Sí/No                              |
| B3          | ¿Aparece un mensaje de «disco no detectado» o «No boot device»?                | Sí/No                              |
| B4          | ¿Se queda en el logo del fabricante o en «Reparación automática»?              | Sí/No                              |
| B5          | ¿Aparece pantalla azul (BSOD)?                                                 | No / Al arrancar / Durante el uso  |
| B6          | ¿La fecha y la hora se desconfiguran al desconectar el equipo?                 | Sí/No                              |
| **Grupo C** | **Video y pantalla**                                                           |                                    |
| C1          | ¿Aparecen líneas, cuadros o colores extraños en la imagen?                     | Sí/No                              |
| C2          | ¿La pantalla queda negra aunque el equipo está encendido?                      | Sí/No                              |
| C3          | ¿Las fallas de imagen aparecen al jugar o usar programas gráficos?             | Sí/No                              |
| C4          | ¿La imagen parpadea o se pierde la señal por momentos?                         | Sí/No                              |
| **Grupo D** | **Rendimiento y temperatura**                                                  |                                    |
| D1          | ¿El equipo está lento en general?                                              | Sí/No                              |
| D2          | ¿El ventilador suena fuerte o de forma constante?                              | Sí/No                              |
| D3          | ¿La carcasa o la base se siente muy caliente al tacto?                         | Sí/No                              |
| D4          | ¿Se congela o se apaga al realizar tareas pesadas?                             | Sí/No                              |
| D5          | ¿El disco aparece al 100% en el Administrador de tareas?                       | Sí / No / No sabe                  |
| D6          | ¿El procesador aparece muy ocupado sin programas abiertos?                     | Sí / No / No sabe                  |
| **Grupo E** | **Almacenamiento**                                                             |                                    |
| E1          | ¿Escucha clics o ruidos de rasgueo en el disco?                                | Sí/No                              |
| E2          | ¿Hay archivos dañados o que desaparecen?                                       | Sí/No                              |
| E3          | ¿Alguna herramienta mostró una advertencia de estado del disco (SMART)?        | Sí / No / No sabe                  |
| **Grupo F** | **Software y seguridad**                                                       |                                    |
| F1          | ¿Aparecen ventanas emergentes o publicidad no solicitada?                      | Sí/No                              |
| F2          | ¿Hay programas o extensiones que no recuerda haber instalado?                  | Sí/No                              |
| F3          | ¿El navegador lo redirige a páginas extrañas o cambió su página de inicio?     | Sí/No                              |
| F4          | ¿El antivirus está desactivado o no se puede activar?                          | Sí/No                              |
| F5          | ¿El problema empezó después de una actualización o de instalar un controlador? | Sí/No                              |
| **Grupo G** | **Contexto del equipo y del uso**                                              |                                    |
| G1          | Tipo de equipo                                                                 | Portátil / Escritorio              |
| G2          | Antigüedad del equipo                                                          | Número (años)                      |
| G3          | Tiempo desde la última limpieza interna                                        | Número (meses) / Nunca             |
| G4          | ¿Cambió o agregó algún componente recientemente?                               | Sí/No                              |
| G5          | Frecuencia del problema                                                        | Ocasional / Frecuente / Permanente |
| G6          | ¿Tiene copia de seguridad de su información?                                   | Sí/No                              |
| G7          | Memoria RAM instalada                                                          | Número (GB) / No sabe              |
| G8          | Tipo de unidad de almacenamiento                                               | HDD / SSD / No sabe                |

_Nota._ Las preguntas del grupo G no apuntan a un diagnóstico por sí solas; se usan para ajustar la certeza y la prioridad de los resultados.

### Salidas del sistema

El sistema entregará uno o varios diagnósticos ordenados por prioridad. Cada diagnóstico irá acompañado de su factor de certeza, su nivel de severidad, una recomendación inicial y la explicación de las reglas que lo sustentan. La Tabla 3 presenta el catálogo preliminar de diez diagnósticos con su severidad base.

### Tabla 3

_Catálogo preliminar de diagnósticos_

| Código | Diagnóstico                                              | Recomendación inicial                                                                 | Severidad base |
| :----- | :------------------------------------------------------- | :------------------------------------------------------------------------------------ | :------------- |
| DX01   | Falla de la fuente de poder o del adaptador de corriente | Desconectar el equipo, probar con otro cargador o fuente y no insistir en encenderlo. | Alta           |
| DX02   | Falla o mala conexión de la memoria RAM                  | Limpiar y reasentar los módulos; probar un módulo a la vez.                           | Alta           |
| DX03   | Falla inminente del disco duro o SSD                     | Respaldar la información de inmediato y reemplazar la unidad.                         | Alta           |
| DX04   | Sobrecalentamiento (polvo, pasta térmica o ventilador)   | Hacer limpieza interna, cambiar la pasta térmica y revisar el ventilador.             | Alta           |
| DX05   | Falla de la tarjeta gráfica o del subsistema de video    | Probar con otro monitor o con el video integrado; revisar temperatura de la tarjeta.  | Alta           |
| DX06   | Corrupción del sistema operativo o del arranque          | Usar las herramientas de reparación de Windows o reinstalar el sistema.               | Media          |
| DX07   | Infección por software malicioso                         | Desconectar de internet, analizar con un antivirus actualizado y cambiar contraseñas. | Alta           |
| DX08   | Conflicto de controladores o actualización defectuosa    | Revertir el controlador o la actualización desde el modo seguro.                      | Media          |
| DX09   | Pila de la BIOS (CMOS) agotada                           | Reemplazar la pila CR2032 de la placa base.                                           | Baja           |
| DX10   | Recursos insuficientes para el uso actual                | Ampliar la RAM o cambiar el disco mecánico por un SSD.                                | Baja           |

_Nota._ Si ninguna regla alcanza la certeza mínima, el sistema responde "caso no concluyente" y recomienda la revisión presencial de un técnico.

### Escala de severidad y prioridad

Cada diagnóstico tiene una severidad base que refleja el daño que puede causar si no se atiende. La Tabla 4 describe los cuatro niveles que usará el sistema.

### Tabla 4

_Escala de severidad de los diagnósticos_

| Nivel           | Criterio                                                                      | Acción sugerida al usuario                                                             |
| :-------------- | :---------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| **4 - Crítica** | Riesgo de daño físico, incendio o pérdida irreversible de información.        | Dejar de usar el equipo, desconectarlo y respaldar o acudir a un técnico de inmediato. |
| **3 - Alta**    | Falla de hardware que deja el equipo inutilizable o que tiende a empeorar.    | Atender en uno o dos días; puede requerir repuesto.                                    |
| **2 - Media**   | El equipo funciona con fallas y la causa probable se corrige con software.    | El usuario puede intentar la solución siguiendo la guía del sistema.                   |
| **1 - Baja**    | Afecta el rendimiento o la comodidad, sin riesgo para el equipo ni los datos. | Programar mantenimiento o mejora cuando sea conveniente.                               |

La severidad base se ajusta con la información de contexto, siguiendo estos criterios generales:

- **Sube a Crítica:** cuando el usuario reporta olor a quemado o chispas (A4), o cuando hay un diagnóstico de falla de almacenamiento y el usuario no tiene copia de seguridad (G6 = No).
- **Sube un nivel:** cuando el problema es permanente (G5) y deja el equipo inutilizable; cuando hay infección por malware con el antivirus desactivado (F4); o cuando el sobrecalentamiento ya provoca apagados bajo carga (D4).
- **Baja un nivel:** cuando el problema apareció justo después de cambiar un componente o de una actualización (G4 o F5), porque suele ser reversible; o cuando el problema es ocasional.
- **Límites:** ningún diagnóstico baja de Baja ni sube de Crítica.

Para manejar la incertidumbre usaremos factores de certeza ($FC$) entre 0 y 1, siguiendo el modelo propuesto para el sistema MYCIN (Shortliffe y Buchanan, 1975). Cada regla tiene un $FC$ que indica qué tanto apoya la conclusión, y si varias reglas apoyan el mismo diagnóstico se combinan con la fórmula:

$$FC = FC_1 + FC_2 \times (1 - FC_1)$$

Además, el contexto modifica la certeza: por ejemplo, un equipo con más de cinco años de uso aumenta la certeza de las fallas de hardware y un equipo que nunca ha recibido limpieza interna aumenta la del sobrecalentamiento. El resultado se presenta como:

- **Muy probable:** ($FC \ge 0{,}70$)
- **Probable:** ($0{,}40 \le FC \le 0{,}69$)
- **Posible:** ($0{,}20 \le FC \le 0{,}39$)
- Por debajo de $0{,}20$ el diagnóstico se descarta.

Finalmente, la lista de resultados se ordena primero por severidad ajustada y, a igual severidad, por factor de certeza. De esta forma, el usuario ve primero lo más urgente y no solo lo más probable.

---

## Diseño conceptual del sistema experto

### Arquitectura general

Siguiendo la estructura clásica de un sistema experto (Giarratano y Riley, 2005), el sistema tendrá cinco componentes:

a) **Base de conocimiento (Prolog):** reglas de diagnóstico, severidades base, modificadores de contexto y textos de recomendación.  
b) **Base de hechos (Prolog):** respuestas del usuario en la sesión actual, almacenadas de forma dinámica con `assert`.  
c) **Motor de inferencia (Prolog):** usa el encadenamiento hacia atrás propio de Prolog para evaluar hipótesis, pregunta solo lo que necesita, combina factores de certeza y calcula la prioridad.  
d) **Módulo de explicación (Prolog y Python):** guarda qué reglas se dispararon y con qué respuestas, para responder "¿por qué?" y "¿cómo llegaste a esta conclusión?".  
e) **Interfaz (Python):** aplicación en Tkinter que se comunica con SWI-Prolog mediante PySwip, muestra las preguntas, recibe las respuestas y presenta los resultados.

### Representación del conocimiento

El conocimiento se organiza en dos niveles. En el primero, los síntomas permiten concluir una categoría de problema (energía, arranque, video, rendimiento, almacenamiento o software). En el segundo, cada categoría activa las reglas de los diagnósticos que le corresponden. La Figura 1 muestra un borrador de cómo se escribirían algunas reglas.

#### Figura 1

_Borrador de reglas en Prolog para el diagnóstico de falla de memoria RAM_

```prolog
% Nivel 1: síntomas -> categoría del problema
categoria(arranque) :-
    respuesta(enciende, si),
    (respuesta(imagen, no) ; respuesta(pitidos, largos)).

% Nivel 2: categoría + síntomas -> diagnóstico
% regla(Id, Diagnostico, FC) :- premisas.
regla(r12, falla_ram, 0.80) :-
    categoria(arranque),
    respuesta(pitidos, largos),
    respuesta(imagen, no).

regla(r13, falla_ram, 0.50) :-
    categoria(arranque),
    respuesta(cambio_hardware, si).

severidad_base(falla_ram, alta).

% Combinación de factores de certeza (modelo MYCIN)
combinar(FC1, FC2, FC) :-
    FC is FC1 + FC2 * (1 - FC1).
```

El predicado `respuesta/2` no se consulta como un hecho fijo: si el valor todavía no se conoce, el motor le pide a Python que formule la pregunta al usuario y guarda la respuesta. Así se consigue el comportamiento de preguntas dinámicas descrito en la justificación.

### Ejemplo de razonamiento

Supongamos que un usuario reporta que su equipo de escritorio enciende, emite pitidos largos y no muestra imagen, y que la semana pasada le agregó un módulo de memoria. El sistema concluye primero la categoría "arranque". Luego se disparan las reglas r12 ($FC = 0{,}80$) y r13 ($FC = 0{,}50$), que combinadas dan:

$$FC = 0{,}80 + 0{,}50 \times 0{,}20 = 0{,}90$$

es decir, falla de RAM "muy probable". Su severidad base es Alta, pero baja a Media porque el problema apareció tras un cambio de hardware y lo más probable es que el módulo esté mal instalado. El sistema recomienda reasentar los módulos de memoria y, si el usuario pide la explicación, muestra las dos reglas y las respuestas que las activaron.

---

## Conclusiones

El diagnóstico de fallas de computadores es un dominio adecuado para un sistema experto porque combina síntomas que apuntan a varias causas, exige un razonamiento por etapas, trabaja con evidencia incierta y necesita priorizar los resultados según el riesgo. Ninguna de estas características se resuelve bien con un formulario o con un sistema transaccional.

Con este entregable dejamos definido el alcance del proyecto: 38 variables de entrada en siete grupos, diez diagnósticos con su severidad base, una escala de cuatro niveles con criterios claros para ajustar la prioridad y un modelo de certeza basado en MYCIN. También dejamos un primer borrador de la representación en Prolog y de la arquitectura de integración con Python. El siguiente paso será completar la tabla de conocimiento con las fuentes y la consulta a un técnico, y traducirla a la base de reglas.

---

## Referencias

- Bratko, I. (2012). _Prolog programming for artificial intelligence_ (4.ª ed.). Addison-Wesley. [https://www.pearson.com/store/en-ca/p/prolog-programming-for-artificial-intelligence/P200000003804/9780321417466](https://www.pearson.com/store/en-ca/p/prolog-programming-for-artificial-intelligence/P200000003804/9780321417466)
- Giarratano, J. C., & Riley, G. D. (2005). _Expert systems: Principles and programming_ (4.ª ed.). Thomson Course Technology. [https://www.goodreads.com/work/editions/455002-expert-systems-principles-and-programming](https://www.goodreads.com/work/editions/455002-expert-systems-principles-and-programming)
- Mueller, S. (2015). _Upgrading and repairing PCs_ (22.ª ed.). Que Publishing. [https://eu.pearson.com/upgrading-and-repairing-pcs/9780134057699](https://eu.pearson.com/upgrading-and-repairing-pcs/9780134057699)
- Russell, S., & Norvig, P. (2021). _Artificial intelligence: A modern approach_ (4.ª ed.). Pearson. [https://aima.cs.berkeley.edu/](https://aima.cs.berkeley.edu/)
- Shortliffe, E. H., & Buchanan, B. G. (1975). A model of inexact reasoning in medicine. _Mathematical Biosciences_, 23(3-4), 351-379. [https://doi.org/10.1016/0025-5564(75)90047-4](<https://doi.org/10.1016/0025-5564(75)90047-4>)
