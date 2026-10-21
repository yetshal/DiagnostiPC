# 07 · Registro de decisiones

> Índice corto de decisiones técnicas. Las mayores tienen además un ADR completo en `docs/adr/NNN-titulo.md` (plantilla en `docs/ai/templates/adr.md`).
> Antes de proponer un cambio de tecnología o patrón, revisa aquí si ya se decidió y por qué.
> Estados: **Aceptada** · **Provisional** · **Propuesta** · **Reemplazada por D-NNN** · **Rechazada**.

## Decisiones de arquitectura iniciales

| ID    | Decisión                                                                                                                               | Alternativas descartadas                    | Motivo                                                               | Estado                     | ADR |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | -------------------------------------------------------------------- | -------------------------- | --- |
| D-001 | Prolog es la única fuente de lógica; Python solo puente y consola                                                                      | Ordenar/filtrar en Python; lógica repartida | Requisito 3.4; separación conocimiento/código                        | Aceptada                   | 001 |
| D-002 | Puente con PySwip, aislado en un solo módulo, con Janus como alternativa                                                               | Janus de entrada; subproceso `swipl`        | Coherencia con el Entregable 1; costo de cambio mínimo               | Provisional (F0-02)        | 002 |
| D-003 | Respuestas como lista `Var-Valor` pasada a los predicados                                                                              | Hechos dinámicos con `assert`               | Sin estado global; cumple el requisito de listas                     | Aceptada                   | 003 |
| D-004 | Encadenamiento N1 → N2 → N3, dependencia solo descendente                                                                              | Un nivel; meta-intérprete                   | Requisito 3.1; sin ciclos por construcción                           | Aceptada                   | 004 |
| D-005 | FC enteros 0–100 con combinación MYCIN; severidad en 4 niveles con ajuste y límites                                                    | FC en coma flotante; solo conteo            | Aritmética exacta y umbrales sin error                               | Aceptada                   | 005 |
| D-006 | Solo consola, sin GUI                                                                                                                  | Tkinter                                     | Requisitos vigentes                                                  | Aceptada (confirmar F0-04) | 006 |
| D-007 | Pruebas de la base con plunit (incluido en SWI-Prolog)                                                                                 | Probar solo desde Python                    | Pruebas rápidas y sin puente                                         | Aceptada                   | —   |
| D-008 | Átomos y predicados sin tildes ni ñ; textos al usuario pueden llevar tildes si UTF-8 funciona de punta a punta                         | Tildes en todo                              | Evitar fallos de codificación en el puente y en Windows              | Aceptada                   | —   |
| D-009 | Estructura plana en la raíz (`base_conocimiento.pl`, `motor_inferencia.py`, `main.py`, `pruebas.py`)                                   | `src/` con paquetes                         | El docente ejecuta desde la raíz; nombres exigidos                   | Aceptada                   | —   |
| D-010 | `Estado` de consulta: `ok`, `no_concluyente`, `datos_insuficientes`, `entrada_invalida`, resueltos por cortes con cláusula por defecto | Excepciones o listas vacías sin significado | Cumple RF-12 y el requisito de fallback                              | Aceptada                   | —   |
| D-011 | Un solo archivo `base_conocimiento.pl` organizado en secciones                                                                         | Varios módulos Prolog                       | El requisito nombra un único archivo                                 | Aceptada                   | —   |
| D-012 | Trazabilidad del conocimiento: cada regla cita fuente (`S?`, `T?`) o `[PENDIENTE-VALIDAR]`                                             | Reglas sin fuente                           | El error principal de un sistema experto es el conocimiento erróneo  | Aceptada                   | —   |
| D-013 | Solo biblioteca estándar de Python + el puente                                                                                         | pandas, rich, colorama                      | Menos fallos de instalación                                          | Aceptada                   | —   |
| D-014 | Mínimo de síntomas para diagnosticar (`N_MIN`) = 2 respuestas de los grupos A–F                                                        | 1; 3                                        | Propuesta inicial; validar con el técnico                            | Provisional                | —   |
| D-015 | La frontera usa solo listas, átomos y enteros (sin términos compuestos)                                                                | Compuestos `dx(...)`                        | Evita incompatibilidades del puente                                  | Aceptada                   | —   |
| D-016 | Recorte de alcance por orden fijo (`04 §Regla de recorte`)                                                                             | Mover la fecha de entrega                   | La entrega es la restricción; el alcance Should/Could es la variable | Aceptada                   | —   |

## Convenciones decididas

| ID    | Decisión                                                                                          | Estado   |
| ----- | ------------------------------------------------------------------------------------------------- | -------- |
| D-017 | Código, comentarios, documentación y mensajes de commit en español, sin tildes en identificadores | Aceptada |
| D-018 | Una rama y un PR por tarea; revisión por la otra persona de la pareja                             | Aceptada |
| D-019 | Commits convencionales: `feat(kb): …`, `fix(motor): …`, `docs: …`, `test: …`                      | Aceptada |
| D-020 | Identificadores de regla `r01`… únicos y citados en comentarios, diccionario y `explicar/3`       | Aceptada |

## Decisiones tomadas durante el desarrollo

> Formato: igual que las tablas anteriores. Numerar desde D-021.

| ID  | Decisión  | Alternativas descartadas | Motivo | Estado |
| --- | --------- | ------------------------ | ------ | ------ |
| —   | _(vacío)_ |                          |        |        |
