# Diccionario de predicados

> Documento oficial de referencia del sistema DiagnostiPC.
> Modos de instanciación: `+Arg` entrada (enviada desde Python o ligada) · `-Arg` salida (unificada hacia Python o hacia otra regla) · `?Arg` bidireccional.
> Columna **Python**: método de `motor_inferencia.py` correspondiente; `—` = predicado interno de Prolog.

---

## 1. API pública (Frontera Python ↔ Prolog)

| Firma                        | Modo                                                             | Descripción funcional                                                                                                                                                                                                                                                                                                                      | Python                                         |
| ---------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| `diagnosticar_todos/3`       | `diagnosticar_todos(+ListaSintomas, +Componente, -Diagnosticos)` | Evalúa la lista de síntomas contra los patrones de falla, verifica la cantidad suficiente de síntomas, descarta diagnósticos inhibidos por `\+` y recopila mediante `findall/3` los pares `Diag-Sev` sin duplicados (`list_to_set/2`). La segunda cláusula actúa como fallback con `\+` y `!` ante listas vacías o síntomas insuficientes. | `motor.consultar_diagnosticos(sintomas, comp)` |
| `severidad_caso/2`           | `severidad_caso(+Diagnostico, -Nivel)`                           | Consulta la severidad asignada al diagnóstico (`bajo`, `medio`, `alto`, `critico`). Usa corte `!` para fijar el primer resultado determinista y fallback a `desconocido`.                                                                                                                                                                  | Invocado internamente por el motor             |
| `componente_afectado/2`      | `componente_afectado(+ListaSintomas, -Componente)`               | Determina el componente de hardware dominante con mayor cantidad de síntomas presentes en la lista. Si no hay suficientes síntomas, retorna `desconocido`.                                                                                                                                                                                 | `motor.obtener_componente_afectado(sintomas)`  |
| `validar_sintomas/2`         | `validar_sintomas(+Lista, -Validos)`                             | Filtra la lista de entrada conservando únicamente los átomos reconocidos en el catálogo `sintoma_valido/1`.                                                                                                                                                                                                                                | `motor.validar_sintomas(sintomas)`             |
| `conteo_sintomas_criticos/2` | `conteo_sintomas_criticos(+Lista, -Conteo)`                      | Filtra mediante `include/3` los síntomas clasificados como críticos (`sintoma_critico/1`) y retorna la cantidad total con `length/2`.                                                                                                                                                                                                      | `motor.contar_sintomas_criticos(sintomas)`     |
| `todos_los_sintomas/1`       | `todos_los_sintomas(-Lista)`                                     | Recolecta con `findall/3` el universo completo de síntomas válidos reconocidos por el sistema.                                                                                                                                                                                                                                             | Invocable para catálogos                       |

---

## 2. Nivel 1 — Validación Preliminar y Condiciones Elementales

| Firma                       | Modo                                              | Descripción funcional                                                                                                            |
| --------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `sintoma_en_lista/2`        | `sintoma_en_lista(?Sintoma, +Lista)`              | Éxito si `Sintoma` es un miembro de `Lista` y pertenece al catálogo `sintoma_valido/1`.                                          |
| `lista_contiene_minimo/3`   | `lista_contiene_minimo(+Lista, +Requeridos, +N)`  | Evalúa la intersección entre `Requeridos` y `Lista` usando `include/3`. Es verdadero si la cantidad de coincidencias es $\ge N$. |
| `es_sintoma_critico/1`      | `es_sintoma_critico(+Sintoma)`                    | Verifica si el síntoma tiene asignada la categoría crítica (`sintoma_critico/1`).                                                |
| `sintomas_del_componente/2` | `sintomas_del_componente(+Componente, -Sintomas)` | Agrupa con `findall/3` todos los síntomas relacionados con un componente en `componente_sintoma/2`.                              |
| `subconjunto_valido/2`      | `subconjunto_valido(+Lista, -Validos)`            | Algoritmo recursivo con corte `!` que descarta los elementos que no sean hechos `sintoma_valido/1`.                              |
| `contiene_sintoma/2`        | `contiene_sintoma(+Lista, +Sintoma)`              | Predicado auxiliar de aridad 2 para orden superior (`include/3`).                                                                |

---

## 3. Nivel 2 — Inferencia Intermedia y Patrones

| Firma                          | Modo                                                 | Descripción funcional                                                                                                                                               |
| ------------------------------ | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `patron_presente/2`            | `patron_presente(+Patron, +ListaSintomas)`           | Verifica si una lista contiene al menos un umbral significativo (mínimo 2 o total - 1) de los síntomas del `patron_falla/2`.                                        |
| `componente_sospechoso/2`      | `componente_sospechoso(+Componente, +ListaSintomas)` | Se activa si al menos 2 síntomas del componente están presentes en la lista observada.                                                                              |
| `diagnostico_excluido/2`       | `diagnostico_excluido(+Diagnostico, +ListaSintomas)` | Evalúa si existe una relación `excluye(OtroDiag, Diagnostico)` donde el patrón de `OtroDiag` esté presente, sirviendo de premisa para la negación por fallo (`\+`). |
| `tiene_sintomas_suficientes/1` | `tiene_sintomas_suficientes(+ListaSintomas)`         | Comprueba que la lista filtrada contenga al menos 2 síntomas válidos reconocidos.                                                                                   |
| `componente_dominante/2`       | `componente_dominante(+ListaSintomas, -Componente)`  | Genera los pares `Cuenta-Componente` para los 7 subsistemas y extrae el de mayor coincidencia mediante `max_par/2`.                                                 |
| `max_par/2`                    | `max_par(+ListaPares, -MaxPar)`                      | Auxiliar de búsqueda de máximo sin recursión izquierda.                                                                                                             |

---

## 4. Nivel 3 — Conclusión Final

| Firma                    | Modo                                                        | Descripción funcional                                                                                                                                                            |
| ------------------------ | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `diagnostico_posible/3`  | `diagnostico_posible(?Patron, +ListaSintomas, ?Componente)` | Regla central de conclusión. Integra las inferencias de Nivel 2: exige `patron_presente/2`, valida `tiene_sintomas_suficientes/1` y aplica negación `\+ diagnostico_excluido/2`. |
| `diagnostico_describe/2` | `diagnostico_describe(+Diagnostico, -Descripcion)`          | Mapea el identificador de diagnóstico con un texto en lenguaje natural explicativo para el usuario.                                                                              |

---

## 5. Catálogo de Hechos Base Estructurados (Aridad $\ge 2$)

| Predicado                 | Aridad | Total Hechos | Propósito                                                                                                                                |
| ------------------------- | ------ | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `componente_sintoma/2`    | 2      | 32           | Relación física entre componente (`cpu`, `ram`, `gpu`, `disco`, `fuente`, `placa_madre`, `enfriamiento`) y sus posibles manifestaciones. |
| `patron_falla/2`          | 2      | 9            | Agrupación canónica de síntomas que configuran un diagnóstico.                                                                           |
| `severidad_diagnostico/2` | 2      | 10           | Clasificación de severidad (`bajo`, `medio`, `alto`, `critico`).                                                                         |
| `excluye/2`               | 2      | 5            | Reglas de exclusión mutua de diagnósticos concurrentes.                                                                                  |
| `diagnostico_describe/2`  | 2      | 10           | Descripciones textuales de las conclusiones.                                                                                             |
| `sintoma_valido/1`        | 1      | 20           | Catálogo cerrado de síntomas evaluables.                                                                                                 |
| `sintoma_critico/1`       | 1      | 7            | Subconjunto de síntomas de alta prioridad.                                                                                               |
