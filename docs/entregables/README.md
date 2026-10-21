# Entregables del curso

Los cuatro artefactos obligatorios (requisitos del curso §4) más la matriz que demuestra el cumplimiento total del proyecto.

| #   | Artefacto                                    | Archivo                                                             | Estado      | Verificación / Notas                                                          |
| --- | -------------------------------------------- | ------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------- |
| 1   | Ficha de definición del proyecto y la pareja | [`01-ficha-definicion.md`](01-ficha-definicion.md)                  | ✅ Completo | Datos de los integrantes, roles, justificación como SBR y alcance.            |
| 2   | Código fuente documentado                    | `base_conocimiento.pl` y `motor_inferencia.py` (raíz)               | ✅ Completo | 66 hechos aridad 2, 17 reglas en 3 niveles, clase `MotorInferencia`.          |
| 3   | Diccionario de predicados                    | [`03-diccionario-predicados.md`](03-diccionario-predicados.md)      | ✅ Completo | Aridades, modos `(+/-)`, niveles N1–N3 y mapeo con Python sincronizados.      |
| 4   | Script de pruebas por consola y evidencia    | `pruebas.py` + [`04-evidencia-pruebas.md`](04-evidencia-pruebas.md) | ✅ Completo | 5/5 casos de prueba pasando (100% PASS) y 3 capturas en carpeta `evidencia/`. |
| —   | Matriz de cumplimiento de requisitos         | [`02-matriz-cumplimiento.md`](02-matriz-cumplimiento.md)            | ✅ Completo | 100% de requisitos técnicos (RF-01 a RF-11) y artefactos certificados.        |

## Evidencias Fotográficas

Las capturas de terminal que demuestran la ejecución real del sistema se encuentran en [`evidencia/`](evidencia/):

- **`01_pruebas_consola_parte1.png`**: Casos 1 al 3 (Diagnóstico único, recolección múltiple y exclusión con `\+` y `!`).
- **`02_pruebas_consola_parte2.png`**: Casos 4 y 5 (Manejo de datos insuficientes y lista vacía + resumen 5/5 PASS).
- **`03_prolog_consulta_directa.png`**: Consulta interactiva directa ejecutada en la consola de SWI-Prolog.

> El Entregable 1 previo queda consolidado y superado por esta entrega formal, cumpliendo a cabalidad todas las especificaciones académicas de la asignatura Sistemas Expertos (FET Rivera).
