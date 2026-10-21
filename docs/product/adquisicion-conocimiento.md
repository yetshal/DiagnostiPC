# Adquisición de conocimiento

> Se completa en F0-05, F1-01, F1-05 y F2-11. **No es para agentes**, salvo las tareas que lo citen: es la fuente que respalda cada regla (`S?`, `T?`).
> Objetivo específico 1 del Entregable 1: adquirir el conocimiento a partir de fuentes técnicas y de la consulta con un técnico de mantenimiento.

## 1. Fuentes

| ID  | Fuente                                                                                        | Tipo          | Qué aporta                                                         | Referencia                                    |
| --- | --------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------ | --------------------------------------------- |
| S1  | Mueller, S. (2015). _Upgrading and repairing PCs_ (22.ª ed.). Que Publishing                  | Libro técnico | Diagnóstico de hardware, fuentes de poder, memoria, almacenamiento | Entregable 1                                  |
| S2  | Shortliffe, E. H. y Buchanan, B. G. (1975). A model of inexact reasoning in medicine          | Artículo      | Modelo de factores de certeza (MYCIN)                              | Entregable 1                                  |
| S3  | Tabla de códigos de pitidos del fabricante de la BIOS (AMI, Award, Phoenix u otro del equipo) | Manual        | Significado de pitidos cortos/largos                               | _(completar con la URL o documento concreto)_ |
| S4  | Manual de la placa base o del portátil de referencia                                          | Manual        | Ubicación de la pila CMOS, RAM, señales                            | _(completar)_                                 |
| S5  | Documentación de Windows (reparación de arranque, modo seguro, controladores)                 | Documentación | Pasos de las recomendaciones de software                           | _(completar)_                                 |
| S6  | Documentación de SMART / herramientas de diagnóstico de disco                                 | Documentación | Indicadores de falla de almacenamiento                             | _(completar)_                                 |
| T1  | Técnico de mantenimiento — sesiones del _(fecha 1)_ y _(fecha 2)_                             | Experto       | Validación de síntomas, FC, descartes, umbrales y severidades      | _(nombre y contacto)_                         |

> Las fuentes S3–S6 son tipos de documento a localizar; hay que **citar la edición o URL exacta** antes de usarlas como respaldo.

## 2. Guion de la entrevista con el técnico (T1)

Llevar impresa la tabla de la sección 4. Para cada diagnóstico preguntar:

1. ¿Qué síntomas hacen que usted sospeche primero de esta falla? ¿Cuáles lo descartan?
2. ¿Qué síntoma es **concluyente** y cuáles son solo indicios? (alimenta el FC: concluyente ≈ 80+, indicio fuerte ≈ 50–70, indicio débil ≈ 20–40)
3. ¿Qué otras fallas se confunden con esta? ¿Cómo las distingue?
4. ¿Qué prueba rápida haría antes de abrir el equipo?
5. ¿Qué tan grave es y en qué casos se vuelve urgente (pérdida de datos, riesgo eléctrico)?
6. ¿Qué haría el usuario por su cuenta y cuándo debe llevarlo al taller?

Umbrales de contexto a fijar con el técnico:

| Umbral                                         | Propuesta inicial (a validar)            | Valor acordado |
| ---------------------------------------------- | ---------------------------------------- | -------------- |
| Equipo «antiguo» (años)                        | 5 (del Entregable 1)                     |                |
| Sin limpieza «reciente» (meses)                | _(proponer)_                             |                |
| RAM «insuficiente» según uso (GB)              | _(proponer)_                             |                |
| Mínimo de síntomas para diagnosticar (`N_MIN`) | 2                                        |                |
| Tratamiento de `no_sabe`                       | Respuesta válida que no aporta evidencia |                |

## 3. Reglas de trabajo con las fuentes

- Todo FC es una estimación: se registra **quién lo propuso** (pareja, técnico, fuente) y si fue validado.
- Si una fuente y el técnico discrepan, se anota la discrepancia y se decide en pareja; se prefiere el criterio del técnico para el diagnóstico práctico y se deja constancia.
- Una regla sin fuente ni validación se marca `[PENDIENTE-VALIDAR]` en el `.pl` y aparece en el informe de cierre de la sesión.

## 4. Tabla de conocimiento por diagnóstico (F1-01)

Plantilla — una fila por regla candidata; copiar el bloque por cada diagnóstico (ver `docs/ai/templates/ficha-regla.md`).

| Dx                             | Regla         | Síntomas que la apoyan (átomos)                           | Condiciones de exclusión | FC propuesto | Sev. base | Recomendación                                                       | Fuente | Validación    |
| ------------------------------ | ------------- | --------------------------------------------------------- | ------------------------ | ------------ | --------- | ------------------------------------------------------------------- | ------ | ------------- |
| DX02 `falla_ram`               | r12           | `enciende-si`, `pitidos-largos`, `imagen-no`              | —                        | 80           | Alta      | Limpiar y reasentar los módulos; probar uno a la vez                | S3, T1 | _(pendiente)_ |
| DX02 `falla_ram`               | r13           | `enciende-si`, `cambio_hardware-si`, (categoría arranque) | —                        | 50           | Alta      | idem                                                                | T1     | _(pendiente)_ |
| DX01 `falla_fuente_poder`      | _(completar)_ |                                                           |                          |              | Alta      | Desconectar, probar con otro cargador o fuente                      |        |               |
| DX03 `falla_disco`             | _(completar)_ |                                                           |                          |              | Alta      | Respaldar de inmediato y reemplazar la unidad                       |        |               |
| DX04 `sobrecalentamiento`      | _(completar)_ |                                                           |                          |              | Alta      | Limpieza interna, pasta térmica, revisar ventilador                 |        |               |
| DX05 `falla_grafica`           | _(completar)_ |                                                           | `\+ pitidos-largos`      |              | Alta      | Probar otro monitor o video integrado                               |        |               |
| DX06 `corrupcion_so`           | _(completar)_ |                                                           |                          |              | Media     | Reparación de Windows o reinstalar                                  |        |               |
| DX07 `malware`                 | _(completar)_ |                                                           |                          |              | Alta      | Desconectar de internet, antivirus actualizado, cambiar contraseñas |        |               |
| DX08 `conflicto_controladores` | _(completar)_ |                                                           |                          |              | Media     | Revertir controlador o actualización desde modo seguro              |        |               |
| DX09 `pila_cmos`               | _(completar)_ |                                                           |                          |              | Baja      | Reemplazar la pila CR2032                                           |        |               |
| DX10 `recursos_insuficientes`  | _(completar)_ |                                                           |                          |              | Baja      | Ampliar RAM o cambiar HDD por SSD                                   |        |               |

Las filas de DX02 son las del ejemplo del Entregable 1 (r12 = 0,80 y r13 = 0,50, que en este plan son 80 y 50). Las recomendaciones provienen de su Tabla 3.

## 5. Registro de reuniones con el técnico

| Fecha | Tema                                             | Observaciones | Cambios a la base | Responsable |
| ----- | ------------------------------------------------ | ------------- | ----------------- | ----------- |
|       | Sesión 1 (F1-05): validar tabla de conocimiento  |               |                   |             |
|       | Sesión 2 (F2-11): validar reglas con los 5 casos |               |                   |             |
