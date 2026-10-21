# Producto — Alcance, Cronograma y Resultados

> Resumen de producto y estado de entrega. Requisitos completos y trazabilidad: [`docs/entregables/02-matriz-cumplimiento.md`](../entregables/02-matriz-cumplimiento.md).

## Problema y Propuesta de Valor

> «Dime qué observas en tu computador y te digo qué le pasa probablemente, qué componente está afectado, qué tan urgente es y qué acciones tomar.»

## Alcance Implementado

- **Componentes analizados:** CPU, RAM, GPU, Almacenamiento, Fuente de Poder, Placa Base, Refrigeración.
- **Base de Conocimiento:** 66 hechos estructurados de aridad 2 y 17 reglas encadenadas en 3 niveles lógicos (N1: validación, N2: patrones, N3: conclusión).
- **Mecanismos de inferencia:** Encadenamiento hacia adelante con corte (`!`), negación por fallo (`\+`), agregación sin duplicados (`findall/3` + `list_to_set/2`) y clasificación de severidad (`bajo`, `medio`, `alto`, `critico`).
- **Módulo puente:** Python ↔ SWI-Prolog mediante `PySwip`, garantizando que la lógica de inferencia resida 100% en Prolog.
- **Pruebas y robustez:** Suite de 5 casos automatizados cubriendo casos normales, exclusión mutua y casos borde (datos insuficientes y lista vacía sin excepciones).
- **Fuera de alcance:** Interfaz gráfica (GUI/Tkinter), servidores, Mac/Apple, periféricos externos, diagnóstico de redes y recuperación física de datos.

---

## Estado del Cronograma por Fases

| Fase                         | Estado       | Resultado Logrado                                                                                   |
| ---------------------------- | ------------ | --------------------------------------------------------------------------------------------------- |
| **F0 · Preparación**         | ✅ Concluida | Entorno configurado (SWI-Prolog 10.0.2 + Python 3.14 + PySwip 0.3.3) y arquitectura definida.       |
| **F1 · Hechos y Catálogo**   | ✅ Concluida | 66 hechos de aridad 2 (síntomas, componentes, severidades, exclusiones y descripciones).            |
| **F2 · Motor Lógico**        | ✅ Concluida | 17 reglas encadenadas en 3 niveles sin bucles, cortes justificados y negación por fallo segura.     |
| **F3 · Integración Consola** | ✅ Concluida | `motor_inferencia.py` y `pruebas.py` ejecutando 5 casos de prueba con 100% PASS.                    |
| **F4 · Entrega y Cierre**    | ✅ Concluida | Ficha, Diccionario de predicados sincronizado, Matriz de cumplimiento 100% y capturas de evidencia. |

---

## Principales Riesgos y su Resolución

| Riesgo inicial                                          | Nivel inicial | Resolución final                                                                                         |
| ------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------- |
| Compatibilidad de PySwip con versiones recientes        | Alto          | Resuelto: PySwip 0.3.3 cargando `base_conocimiento.pl` por ruta absoluta limpia sin errores.             |
| Falta de encadenamiento o salto de niveles en reglas    | Alto          | Resuelto: Separación estricta Nivel 1 → Nivel 2 → Nivel 3 verificada en matriz y pruebas.                |
| Lógica lógica filtrada a Python                         | Alto          | Resuelto: Python únicamente realiza conversión de tipos y presentación en consola; inferencia en Prolog. |
| Inestabilidad ante listas vacías o valores desconocidos | Medio         | Resuelto: Reglas de fallback y predicados de suficiencia en Prolog garantizan terminación limpia.        |
