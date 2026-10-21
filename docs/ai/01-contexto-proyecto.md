# 01 · Contexto del proyecto

> Lectura para entender **qué** se construye y **por qué**. Para el **cómo**, ver `02-arquitectura.md`.
> Fuente del dominio: Entregable 1 (PDF «DiagnostiPC», Grupo 4). Fuente de los requisitos técnicos: documento «Requisitos Técnicos y Artefactos de Entrega» del curso.

## 1. Producto

**DiagnostiPC** recibe lo que una persona observa en su computador (enciende o no, pitidos, imagen, temperatura, lentitud, publicidad…) y responde: **qué le pasa probablemente, qué tan urgente es y qué hacer primero**.

Cinco capacidades:

1. **Clasificar** el problema en una categoría (energía, arranque, video, rendimiento, almacenamiento, software).
2. **Diagnosticar** hasta 10 fallas comunes con un grado de certeza.
3. **Priorizar** por severidad (4 niveles) ajustada con el contexto del equipo.
4. **Recomendar** una primera acción por diagnóstico.
5. **Explicar** qué reglas apoyan cada conclusión (Should).

**Principio de diseño:** el sistema nunca inventa. Con evidencia insuficiente responde `datos_insuficientes`; con evidencia que no alcanza ningún umbral, `no_concluyente` y recomienda revisión presencial de un técnico.

## 2. Usuarios

| Persona                                                | Necesidad                                                         |
| ------------------------------------------------------ | ----------------------------------------------------------------- |
| Usuario doméstico, estudiante, personal administrativo | Saber si puede resolverlo solo o debe llevar el equipo a revisión |
| Monitor de sala de cómputo / técnico en formación      | Ordenar su diagnóstico                                            |
| Técnico de soporte                                     | Clasificación previa antes de abrir el equipo                     |

Dentro del curso, además, el **evaluador** (docente) es un usuario: debe poder ejecutar los casos de prueba y ver trazabilidad requisito → código → evidencia.

## 3. Flujo principal (consola)

1. `python main.py` muestra el cuestionario (preguntas y opciones **leídas desde Prolog**).
2. El usuario responde; Python arma la lista `Var-Valor` y la envía.
3. Prolog valida, clasifica, infiere, calcula certeza y severidad, y devuelve `Resultados` y `Estado`.
4. Python imprime la tabla de diagnósticos ordenada y, si se pide, la explicación.

## 4. Requisitos funcionales (MoSCoW)

Origen: **REQ §n** = documento de requisitos del curso; **EP** = Entregable 1.

| ID    | Requisito                                                                                                | Prio. | Origen              |
| ----- | -------------------------------------------------------------------------------------------------------- | ----- | ------------------- |
| RF-01 | ≥ 30 hechos estructurados (aridad ≥ 2), contiguos por predicado, en secciones comentadas                 | M     | REQ §3.1            |
| RF-02 | ≥ 15 reglas con encadenamiento N1 → N2 → N3 (meta: ≥ 40 cláusulas-regla, como prometió el EP)            | M     | REQ §3.1, EP obj. 1 |
| RF-03 | Sin recursión izquierda ni bucles en el backtracking                                                     | M     | REQ §3.1            |
| RF-04 | Predicados de listas: subconjunto de requisitos, conteo de condiciones cumplidas, filtrado               | M     | REQ §3.2            |
| RF-05 | Corte `!` en reglas mutuamente excluyentes y cláusula por defecto (fallback), justificado en comentarios | M     | REQ §3.2            |
| RF-06 | Negación `\+` para exclusiones, con variables ya instanciadas                                            | M     | REQ §3.2            |
| RF-07 | Predicado principal con `findall`/`bagof`/`setof` que reúne todos los diagnósticos sin duplicados        | M     | REQ §3.3            |
| RF-08 | Severidad por diagnóstico: base + ajuste por contexto, 4 niveles, límites [1, 4]                         | M     | REQ §3.3, EP        |
| RF-09 | Resultados ordenados por severidad ajustada y luego por certeza                                          | M     | EP                  |
| RF-10 | Puente Python↔SWI-Prolog (PySwip o Janus) que carga `base_conocimiento.pl`; interacción solo por consola | M     | REQ §3.4            |
| RF-11 | Python sin lógica de dominio (inferencia, descarte, validación, severidad)                               | M     | REQ §3.4            |
| RF-12 | Lista vacía, parcial o inválida producen un `Estado`, nunca una excepción en Python                      | M     | REQ §4.4            |
| RF-13 | `main.py` interactivo: cuestionario → resultados                                                         | M     | REQ §3.4            |
| RF-14 | `pruebas.py` con ≥ 5 casos (normal 1, normal 2, exclusión, borde 1, borde 2) y salida formateada         | M     | REQ §4.4            |
| RF-15 | Diccionario de predicados (firma, modo, descripción)                                                     | M     | REQ §4.3            |
| RF-16 | Ficha de definición del proyecto y la pareja                                                             | M     | REQ §4.1            |
| RF-17 | Factor de certeza (MYCIN, enteros 0–100) con etiquetas muy probable / probable / posible                 | S     | EP                  |
| RF-18 | `explicar/3`: reglas disparadas que sustentan un diagnóstico                                             | S     | EP                  |
| RF-19 | Prueba automática de cumplimiento de mínimos (conteo de hechos, reglas, `!`, `\+`, `findall`)            | S     | —                   |
| RF-20 | Preguntas dinámicas: Prolog decide la siguiente (`siguiente_pregunta/2`); Python solo la muestra         | C     | EP                  |

**Fuera de alcance (W):** interfaz gráfica (Tkinter, web), servidores, equipos Mac, periféricos, fallas de red, recuperación de datos, persistencia de sesiones, aprendizaje automático.

## 5. Requisitos no funcionales

| ID     | Requisito                     | Umbral                                                                                       |
| ------ | ----------------------------- | -------------------------------------------------------------------------------------------- |
| RNF-01 | Reproducibilidad              | `python pruebas.py` corre en una máquina limpia con ≤ 3 comandos documentados                |
| RNF-02 | Separación                    | Ninguna constante de dominio (síntomas, umbrales, textos de recomendación) en archivos `.py` |
| RNF-03 | Terminación                   | Todas las consultas terminan; prueba con entradas aleatorias del catálogo sin colgarse       |
| RNF-04 | Aritmética exacta             | Certeza entera 0–100; pruebas en cada borde de umbral                                        |
| RNF-05 | Trazabilidad del conocimiento | 100 % de las reglas citan fuente o están marcadas `[PENDIENTE-VALIDAR]`                      |
| RNF-06 | Robustez                      | Cero tracebacks de Python ante entrada vacía, parcial, inválida o ante Prolog sin resultados |
| RNF-07 | Legibilidad                   | `base_conocimiento.pl` con secciones, indentación y comentarios de propósito; ≤ 100 columnas |
| RNF-08 | Tiempo de respuesta           | Una consulta completa < 1 s en un portátil estándar                                          |
| RNF-09 | Portabilidad                  | Funciona en Windows y Linux/macOS con SWI-Prolog instalado                                   |

## 6. Conciliación Entregable 1 ↔ requisitos vigentes

| Tema                     | Entregable 1 dijo              | Requisitos vigentes                                    | Decisión del plan                                                             |
| ------------------------ | ------------------------------ | ------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Interfaz                 | Tkinter                        | Solo consola                                           | Consola (ADR-006); confirmar con el docente                                   |
| Reglas                   | ≥ 40                           | ≥ 15                                                   | Mínimo 15 (obligatorio); meta 40 cláusulas-regla                              |
| Preguntas                | Dinámicas con retorno a Python | Python envía datos y recibe listas                     | Entrada por lista (ADR-003); dinámicas solo como C vía `siguiente_pregunta/2` |
| Certeza                  | FC 0–1                         | Severidad o prioridad (ponderación numérica permitida) | Se conserva con enteros 0–100 (ADR-005)                                       |
| Explicación              | Módulo de explicación          | No exigida                                             | Should (`explicar/3`)                                                         |
| Nombre del módulo Python | —                              | `motor_inferencia.py` (§3.4) y `motor.py` (§4.2)       | `motor_inferencia.py`; confirmar con el docente                               |
| Catálogo                 | 38 variables, 10 diagnósticos  | Mín. 30 hechos                                         | Se cumple de sobra (≈ 110 hechos)                                             |

## 7. Supuestos

- Pareja de estudiantes con roles del Entregable 1 (Líder de Conocimiento/Prolog y Líder de Integración/Python), apoyada por agentes de IA; ≈ 2–3 h por sesión.
- Fecha de entrega **por definir** (ver `05`); el plan se mide en sesiones y fases, no en fechas fijas.
- Entorno principal Windows; también debe correr en Linux/macOS.
- El técnico de mantenimiento está disponible para dos sesiones de validación (F1-05 y F2-11).

## 8. Criterios de éxito

| Criterio                                             | Meta                                 |
| ---------------------------------------------------- | ------------------------------------ |
| Requisitos Must cumplidos y verificados en la matriz | 16 de 16 (RF-01…RF-16)               |
| Casos de prueba por consola                          | ≥ 5 pasan; obtenido = esperado       |
| Diagnósticos validados por el técnico                | ≥ 8 de 10 sin observaciones críticas |
| Reglas con fuente citada                             | 100 %                                |
| Reproducción en una segunda máquina                  | Éxito en ≤ 15 min                    |
