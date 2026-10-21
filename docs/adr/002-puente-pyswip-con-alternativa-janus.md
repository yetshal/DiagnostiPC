# ADR-002: Puente con PySwip, aislado para poder cambiar a Janus

- **Estado:** Aceptada (provisional: se confirma con el spike F0-02)
- **Fecha:** 2026-10-21
- **Decisores:** Pareja
- **Tarea relacionada:** F0-02, F3-01

## Contexto y problema

Los requisitos permiten **PySwip o Janus**. El Entregable 1 anunció PySwip. Ambos dependen de que Python encuentre la biblioteca de SWI-Prolog instalada en el equipo, y el desajuste de versiones o de arquitectura (32/64 bits) es una causa frecuente de fallos de instalación, sobre todo en Windows.

## Factores de decisión

- Que funcione en las máquinas reales de la pareja (probablemente Windows).
- Coherencia con lo ya entregado (PySwip).
- Poca superficie de código acoplado al puente.
- Que la lista de entrada/salida se transfiera sin trucos.

## Opciones consideradas

1. PySwip (`pip install pyswip`).
2. Janus (`janus-swi`, incluido en las versiones recientes de SWI-Prolog 9.x).
3. Invocar `swipl` por subproceso y parsear texto (descartada: no es "librería puente").

## Decisión

**Opción 1 como punto de partida**, con **toda** la comunicación concentrada en un único módulo de adaptación (funciones `cargar_base`, `consultar` y `cerrar` dentro de `motor_inferencia.py`). El spike F0-02 prueba: carga del `.pl`, envío de una lista, recepción de una lista, caracteres con tildes y cierre correcto de consultas. Si PySwip falla en el entorno de alguno de los dos, se cambia **solo ese módulo** a Janus y se registra la decisión.

## Consecuencias

- **Positivas:** cambiar de puente cuesta una tarea pequeña; el resto del código no sabe qué librería hay debajo.
- **Negativas / deuda aceptada:** hay que probar el puente en las dos máquinas antes de avanzar; los detalles de cada librería (tipos devueltos, manejo de consultas abiertas) se verifican, no se asumen.
- **Cuándo revisarla:** si el spike falla en cualquiera de los dos equipos, o si el docente indica una librería concreta.

## Pros y contras de las opciones

### Janus

- ➕ Mantenido junto a SWI-Prolog; conversión de listas nativa.
- ➖ Exige SWI-Prolog reciente; menos conocido en el curso.

### Subproceso

- ➕ Sin dependencias de Python.
- ➖ No cumple "librería puente"; frágil al parsear salidas.

## Referencias

- Documentación de PySwip y del paquete `janus-swi` (verificar versión vigente al instalar).
