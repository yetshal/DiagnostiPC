# Matriz de cumplimiento de requisitos

> Trazabilidad requisito → dónde se cumple → cómo se verifica.
> Estado: ✅ verificado y probado en ejecución real.

---

## A. Requisitos técnicos (Documento del curso §3)

| ID        | Requisito                                                | Implementación en DiagnostiPC                                                                                                                                                                      | Verificación                                              | Estado |
| --------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | :----: |
| **RF-01** | $\ge 30$ hechos, aridad $\ge 2$, contiguos por secciones | Secciones 2 a 5 en `base_conocimiento.pl`: 32 `componente_sintoma/2`, 9 `patron_falla/2`, 10 `severidad_diagnostico/2`, 5 `excluye/2`, 10 `diagnostico_describe/2` (**Total: 66 hechos aridad 2**) | Conteo e inspección directa en `base_conocimiento.pl`     |   ✅   |
| **RF-02** | $\ge 15$ reglas con encadenamiento multinivel            | 17 reglas divididas estrictamente en: Nivel 1 (preliminar), Nivel 2 (intermedio) y Nivel 3 (conclusión final)                                                                                      | Encadenamiento validado en Casos 1, 2 y 3 de `pruebas.py` |   ✅   |
| **RF-03** | Sin recursión izquierda ni bucles                        | Descomposición por reducción de listas y metas evaluadas de izquierda a derecha                                                                                                                    | Todas las consultas y pruebas terminan en milisegundos    |   ✅   |
| **RF-04** | Procesamiento de Listas                                  | `subconjunto_valido/2`, `lista_contiene_minimo/3`, `include/3`                                                                                                                                     | Casos Borde 1 y 2 en `pruebas.py`                         |   ✅   |
| **RF-05** | Operador de Corte (`!`) en exclusión y fallback          | `subconjunto_valido/2`, `severidad_caso/2`, `componente_afectado/2`, `diagnosticar_todos/3`                                                                                                        | Evita backtracking innecesario y garantiza fallbacks      |   ✅   |
| **RF-06** | Negación por Fallo (`\+`) con variables instanciadas     | `\+ diagnostico_excluido(Patron, ListaSintomas)` y `\+ tiene_sintomas_suficientes(ListaSintomas)`                                                                                                  | Caso 3 (Exclusión) en `pruebas.py`                        |   ✅   |
| **RF-07** | Recolección sin duplicados                               | `diagnosticar_todos/3` usando `findall/3` y `list_to_set/2`                                                                                                                                        | Caso 2 (Múltiples Diagnósticos) en `pruebas.py`           |   ✅   |
| **RF-08** | Nivel de Severidad asociado a diagnósticos               | Mapeo determinista en `severidad_diagnostico/2` (`bajo`, `medio`, `alto`, `critico`)                                                                                                               | Retornado en cada par de diagnóstico en `pruebas.py`      |   ✅   |
| **RF-09** | Integración Python + SWI-Prolog                          | Clase `MotorInferencia` en `motor_inferencia.py` comunicándose vía `pyswip.Prolog()`                                                                                                               | `python3 pruebas.py` ejecuta sin errores                  |   ✅   |
| **RF-10** | Lógica 100% en Prolog (Python sin lógica)                | Python solo pasa listas de cadenas, invoca consultas y formatea strings en terminal                                                                                                                | Auditoría del código de `motor_inferencia.py`             |   ✅   |
| **RF-11** | Lista vacía o parcial sin excepciones                    | Reglas fallback y captura de datos insuficientes                                                                                                                                                   | Casos Borde 1 y 2 en `pruebas.py`                         |   ✅   |

---

## B. Artefactos de entrega (Documento del curso §4)

| Artefacto                            | Archivo oficial                                           | Verificación                                                          | Estado |
| ------------------------------------ | --------------------------------------------------------- | --------------------------------------------------------------------- | :----: |
| **1. Ficha de Definición**           | `docs/entregables/01-ficha-definicion.md`                 | Datos de la pareja, justificación como SBR y diagnósticos esperados   |   ✅   |
| **2. Código Fuente Documentado**     | `base_conocimiento.pl` y `motor_inferencia.py`            | Bloques estructurados y comentarios justificando cortes y negaciones  |   ✅   |
| **3. Diccionario de Predicados**     | `docs/entregables/03-diccionario-predicados.md`           | Firmas, aridades, modos `(+/-)` y descripción funcional               |   ✅   |
| **4. Script de Pruebas y Evidencia** | `pruebas.py` y `docs/entregables/04-evidencia-pruebas.md` | 5 casos de prueba formateados (5/5 PASS) + 3 capturas en `evidencia/` |   ✅   |

---

## C. Cifras Finales del Proyecto

| Métrica                           | Requisito Mínimo | Logrado en DiagnostiPC            |       Estado       |
| --------------------------------- | ---------------- | --------------------------------- | :----------------: |
| Hechos estructurados ($\ge 2$)    | 30               | **66**                            | Supera ampliamente |
| Total hechos (incluyendo unarios) | —                | **93**                            |      Completo      |
| Reglas de inferencia multinivel   | 15               | **17**                            |       Cumple       |
| Niveles de encadenamiento         | 3                | **3** (Nivel 1, Nivel 2, Nivel 3) |       Cumple       |
| Diagnósticos implementados        | —                | **10**                            |       Cumple       |
| Casos de prueba automatizados     | 5                | **5** (5/5 PASS)                  |       Cumple       |
