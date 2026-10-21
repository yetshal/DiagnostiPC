# Ficha de definición del proyecto y de la pareja

## 1. Integrantes

| Nombre completo                 | Código       | Correo institucional        | Rol                                                             |
| ------------------------------- | ------------ | --------------------------- | --------------------------------------------------------------- |
| Juan Carlos Bastidas Bernal     | N/A          | juan_bastidasbe@fet.edu.co  | Líder de Ingeniería del Conocimiento y Modelado Lógico (Prolog) |
| Julian Alfonso Montero Trujillo | SOF220251032 | julian_monterotr@fet.edu.co | Líder de Arquitectura de Integración e Interfaz (Python)        |

Asignatura: Sistemas Expertos · Ingeniería de Software · Fundación Escuela Tecnológica de Neiva, sede Rivera-Huila · Docente: Juan José Ramos Díaz.

## 2. Tema seleccionado

**DiagnostiPC: sistema experto para el diagnóstico de fallas de hardware y software en computadores personales.**

## 3. Descripción del problema

Cuando un computador falla, la mayoría de los usuarios no sabe interpretar lo que ve: un equipo que enciende sin imagen, pitidos al arrancar, una pantalla azul o un ventilador ruidoso. El mismo síntoma puede tener causas muy distintas (la falta de imagen puede deberse a la RAM, a la gráfica, a la fuente o a un cable). Sin guía, el usuario sigue usando un equipo que puede perder datos, compra repuestos innecesarios o paga un servicio por algo que podía resolver solo.

En Rivera y Neiva el soporte especializado no siempre está disponible de inmediato y en las salas de sistemas los monitores suelen ser estudiantes con poca experiencia. El conocimiento existe, pero está concentrado en técnicos con años de práctica y disperso en manuales, tablas de códigos de pitidos y foros. DiagnostiPC acerca ese razonamiento a quien no lo tiene: qué le pasa probablemente al equipo, qué tan urgente es y qué hacer primero.

**Alcance:** PC de escritorio y portátiles con Windows; diagnóstico a nivel de componente o causa probable. **Fuera de alcance:** servidores, Mac, periféricos, fallas de red y recuperación de datos.

## 4. Justificación: por qué un sistema basado en reglas

1. **Relación de muchos a muchos** entre síntomas y causas: las reglas se escriben de forma independiente y el motor las combina; un árbol de `if/else` sería inmanejable.
2. **Encadenamiento lógico** por etapas, como un técnico: síntomas → categoría → causa específica.
3. **Evidencia incierta:** cada regla tiene un grado de certeza y la evidencia convergente se combina (modelo MYCIN).
4. **Priorización:** no todas las fallas son igual de urgentes; la severidad se ajusta con el contexto del equipo.
5. **Explicabilidad:** se puede mostrar qué reglas sustentan una conclusión.
6. **Mantenimiento:** agregar o corregir una falla solo exige editar la base de conocimiento en Prolog, sin tocar Python.

## 5. Diagnósticos / resultados esperados (listado preliminar)

| Cód. | Diagnóstico                                              | Severidad base |
| ---- | -------------------------------------------------------- | -------------- |
| DX01 | Falla de la fuente de poder o del adaptador de corriente | Alta           |
| DX02 | Falla o mala conexión de la memoria RAM                  | Alta           |
| DX03 | Falla inminente del disco duro o SSD                     | Alta           |
| DX04 | Sobrecalentamiento (polvo, pasta térmica o ventilador)   | Alta           |
| DX05 | Falla de la tarjeta gráfica o del subsistema de video    | Alta           |
| DX06 | Corrupción del sistema operativo o del arranque          | Media          |
| DX07 | Infección por software malicioso                         | Alta           |
| DX08 | Conflicto de controladores o actualización defectuosa    | Media          |
| DX09 | Pila de la BIOS (CMOS) agotada                           | Baja           |
| DX10 | Recursos insuficientes para el uso actual                | Baja           |

Resultados adicionales: `no_concluyente` (evidencia que no alcanza ningún umbral), `datos_insuficientes` (muy pocas respuestas) y `entrada_invalida` (valor fuera del catálogo).

## 6. Cambios respecto al Entregable 1

| Aspecto           | Entregable 1                             | Versión final                                                                |
| ----------------- | ---------------------------------------- | ---------------------------------------------------------------------------- |
| Interfaz          | Tkinter                                  | **Consola** (requisito del curso)                                            |
| Reglas            | ≥ 40                                     | ≥ 15 obligatorias; meta ≥ 40 cláusulas-regla _(ajustar a lo logrado)_        |
| Factor de certeza | 0–1                                      | Entero 0–100 (misma fórmula MYCIN)                                           |
| Entrada           | Preguntas dinámicas con retorno a Python | Lista `Var-Valor` enviada a Prolog; preguntas dinámicas como mejora opcional |

_(Completar en F4-04 con las cifras reales: nº de hechos, nº de reglas por nivel, diagnósticos finales.)_
