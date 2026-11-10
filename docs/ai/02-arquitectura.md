# 02 · Arquitectura de referencia

> Fuente de verdad técnica. Si el código y este documento difieren, **se detiene el trabajo y se pregunta al humano**.
> Diagramas: `docs/architecture/README.md`.
>
> **⚠ Desactualizado (detectado 2026-11-10):** §1, §2, §4, §5 y §10 describen el diseño inicial, que no se implementó así. El código real usa listas de átomos de síntoma (`diagnosticar_todos(+Sintomas, +Componente, -Pares)`), interfaz Streamlit (D-021), DCG (D-023), `assertz` en Modo Experto (D-024) y scikit-learn (D-025). Mientras no se reescriba este documento, la referencia vigente del contrato es `docs/entregables/03-diccionario-predicados.md` y las decisiones D-021…D-026 de `07`.

## 1. Vista general

Arquitectura en dos capas con un contrato estrecho entre ellas:

```
Usuario (teclado/pantalla)
   │
   ▼
main.py / pruebas.py ──► motor_inferencia.py ──► PySwip | Janus ──► SWI-Prolog
   (consola)               (puente: cargar,                          base_conocimiento.pl
                            consultar, formatear)                    (conocimiento + razonamiento)
```

- **Python** = entrada/salida y puente. No contiene conocimiento del dominio.
- **Prolog** = hechos, reglas, certeza, severidad, orden de resultados, textos de recomendación y catálogo de preguntas.

Sin base de datos, sin red, sin GUI, sin estado entre consultas (ADR-003).

## 2. Componentes

| Archivo                | Responsabilidad                                                                                                                                      |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `base_conocimiento.pl` | Todo el conocimiento y el razonamiento (un solo archivo, secciones comentadas)                                                                       |
| `motor_inferencia.py`  | `cargar_base()`, `consultar(...)`, funciones de alto nivel (`diagnosticar`, `catalogo`, `explicar`), conversión mínima de tipos, cierre de consultas |
| `main.py`              | Cuestionario por consola, impresión de resultados, manejo de Ctrl+C                                                                                  |
| `pruebas.py`           | ≥ 5 casos con objetivo, entrada, consulta, esperado y obtenido; escribe en `evidencia/`                                                              |
| `tests/tests_kb.pl`    | Pruebas unitarias en Prolog (plunit) de hechos, N1, N2, N3, certeza y severidad                                                                      |

## 3. Estructura del repositorio

```
.
├── base_conocimiento.pl
├── motor_inferencia.py
├── main.py
├── pruebas.py
├── tests/tests_kb.pl
├── evidencia/                 # salida_pruebas.txt, capturas
├── docs/                      # este paquete
├── requirements.txt           # solo el puente (pyswip o janus-swi)
├── AGENTS.md  CLAUDE.md  README.md  .gitignore
```

Estructura plana a propósito: el docente ejecuta `python main.py` y `python pruebas.py` desde la raíz (D-009).

## 4. Organización de `base_conocimiento.pl`

Primero **todos los hechos**, agrupados de forma contigua por predicado; después las reglas por nivel. No se usa `:- discontiguous`: si lo necesitas, el archivo está mal organizado.

| Sec. | Contenido                             | Predicados                                                                                                                                      | Aprox.         |
| ---- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| 0    | Cabecera, directivas, codificación    | `:- set_prolog_flag(encoding, utf8)`                                                                                                            | —              |
| 1    | Catálogo de variables                 | `pregunta/3`, `valor_permitido/2`                                                                                                               | 38 + 38 hechos |
| 2    | Catálogo de diagnósticos              | `diagnostico/2`, `severidad_base/2`, `recomendacion/2`                                                                                          | 10 + 10 + 10   |
| 3    | Escalas                               | `nivel_severidad/3`, `umbral_certeza/2`, `grupo_variable/2`                                                                                     | 4 + 3 + 38     |
| 4    | Utilidades de listas                  | `respuesta/3`, `cumple_todas/2`, `contar_cumplidas/3`, `filtrar_validas/2`, `subconjunto/2`                                                     | reglas         |
| 5    | **Nivel 1** (condiciones elementales) | `equipo_enciende/1`, `sin_imagen/1`, `pitidos_largos/1`, `equipo_antiguo/1`, `sin_limpieza_reciente/1`, `sin_respaldo/1`, `valida_respuesta/1`… | ≥ 10           |
| 6    | **Nivel 2** (categorías e indicios)   | `categoria/2`, `indicio_calor/1`, `indicio_disco/1`, `indicio_malware/1`, `recursos_limitados/1`…                                               | ≥ 10           |
| 7    | **Nivel 3** (diagnósticos)            | `evidencia/4` (una o más cláusulas por diagnóstico)                                                                                             | ≥ 15 cláusulas |
| 8    | Certeza                               | `combinar_certeza/3`, `combinar_lista/2`, `nivel_certeza/2`                                                                                     | ≈ 8            |
| 9    | Severidad                             | `severidad_ajustada/3`, `ajuste/3`                                                                                                              | ≈ 8 cláusulas  |
| 10   | API pública                           | `diagnosticar_todos/3`, `catalogo_preguntas/1`, `explicar/3`, `siguiente_pregunta/2`                                                            | 4–6            |

Total orientativo: ≈ 110 hechos y ≥ 50 cláusulas de regla (mínimos del curso: 30 y 15).

## 5. Contrato Python ↔ Prolog (fronteras planas)

Para evitar sorpresas del puente con términos compuestos, **la frontera solo usa listas, átomos y enteros**.

**Entrada** — `Respuestas`: lista de pares `Var-Valor`.

```prolog
[enciende-si, imagen-no, pitidos-largos, cambio_hardware-si, tipo_equipo-escritorio, antiguedad_anios-3]
```

Variables y valores válidos: `docs/ai/08-glosario.md` §Variables. Los números son enteros (`antiguedad_anios-3`, `ram_gb-8`, `meses_desde_limpieza-18`); `meses_desde_limpieza-nunca` es válido.

**Salida de `diagnosticar_todos(+Respuestas, -Resultados, -Estado)`**

```prolog
Resultados = [[falla_ram, 90, muy_probable, 2, media, 'Limpiar y reasentar los modulos; probar uno a la vez.'], ...]
Estado     = ok | no_concluyente | datos_insuficientes | entrada_invalida
```

Cada elemento: `[Dx, FC, EtiquetaCerteza, SevNumero, SevNombre, Recomendacion]`. La lista viene **ya ordenada** por prioridad.

| Estado                | Cuándo                                                                              | Resultados                                                 |
| --------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `entrada_invalida`    | Alguna variable o valor fuera del catálogo                                          | `[]` (y `validar_entrada/2` entrega la lista de inválidas) |
| `datos_insuficientes` | Menos de `N_MIN` síntomas (grupos A–F) respondidos (provisional `N_MIN = 2`, D-014) | `[]`                                                       |
| `no_concluyente`      | Hay datos suficientes pero ningún diagnóstico llega a FC ≥ 20                       | `[]`                                                       |
| `ok`                  | Al menos un diagnóstico                                                             | lista ordenada                                             |

La precedencia se implementa con cortes (RF-05): una cláusula por estado, de la más específica a la cláusula por defecto.

**Reglas del puente (Python):**

1. Python construye el texto de la consulta con átomos validados por expresión regular (`^[a-z][a-z0-9_]*$`) o enteros; **nunca** inserta texto libre del usuario.
2. Cada consulta se consume por completo o se cierra (`list(...)`/cierre explícito) antes de abrir otra.
3. Cualquier excepción del puente se captura en `motor_inferencia.py` y se traduce a un mensaje claro; el usuario nunca ve un traceback.
4. Prolog **no imprime** nada (sin `format`/`print` en la base); solo devuelve datos.

## 6. Razonamiento en tres niveles (ejemplo del Entregable 1, adaptado)

```prolog
% --- Nivel 1: condiciones elementales sobre la lista R ---------------------
equipo_enciende(R) :- respuesta(R, enciende, si).
sin_imagen(R)      :- respuesta(R, imagen, no).
pitidos_largos(R)  :- respuesta(R, pitidos, largos).

% --- Nivel 2: categoría (usa Nivel 1) --------------------------------------
categoria(R, arranque) :-
    equipo_enciende(R),
    ( sin_imagen(R) ; pitidos_largos(R) ).

% --- Nivel 3: diagnóstico (usa Nivel 2 y Nivel 1) --------------------------
% Fuente: S3 (tabla de pitidos), T1.  FC por validar con el técnico.
evidencia(R, falla_ram, r12, 80) :-
    categoria(R, arranque), pitidos_largos(R), sin_imagen(R).
evidencia(R, falla_ram, r13, 50) :-
    categoria(R, arranque), respuesta(R, cambio_hardware, si).
```

Dependencias estrictamente descendentes (N3 → N2 → N1 → hechos). Ningún predicado se llama a sí mismo.

## 7. Certeza y severidad

**Certeza (ADR-005):** enteros 0–100. `combinar_certeza(A, B, C) :- C is A + (B * (100 - A)) // 100.` y `combinar_lista/2` pliega una lista de FC (ej. `[80, 50] → 90`). Etiquetas con `nivel_certeza/2` (cortes por umbral: ≥ 70 / ≥ 40 / ≥ 20 / descartado).

**Severidad:** `severidad_base/2` (hecho) → `severidad_ajustada/3`:

| Condición de contexto                                               | Efecto                                   |
| ------------------------------------------------------------------- | ---------------------------------------- |
| Olor a quemado/chispas (`olor_quemado-si`)                          | Sube a crítica                           |
| Diagnóstico de almacenamiento y `tiene_respaldo-no`                 | Sube a crítica                           |
| Problema permanente que deja el equipo inutilizable                 | Sube un nivel                            |
| Malware con antivirus inactivo                                      | Sube un nivel                            |
| Sobrecalentamiento con apagados bajo carga (`congela_con_carga-si`) | Sube un nivel                            |
| Problema tras cambio de componente o actualización                  | Baja un nivel                            |
| Problema ocasional                                                  | Baja un nivel                            |
| Límites                                                             | Nunca por debajo de 1 ni por encima de 4 |

Precedencia por cortes: «sube a crítica» prevalece sobre «sube un nivel», y los ajustes de subida prevalecen sobre los de bajada. **Los umbrales numéricos (p. ej. «antigüedad > 5 años», «sin limpieza > N meses») se validan con el técnico (T1) antes de fijarse.**

**Orden final:** severidad ajustada ↓, certeza ↓. La clave de orden es total (incluye el nombre del diagnóstico para desempatar), porque `predsort/3` elimina elementos que compara como iguales.

## 8. Dónde aparece cada requisito técnico

| Requisito (REQ)  | Mecanismo                                                                                                                                                                     |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Listas (§3.2)    | `respuesta/3` (`member`), `cumple_todas/2` y `subconjunto/2` (requisitos ⊆ respuestas), `contar_cumplidas/3`, `filtrar_validas/2`, `combinar_lista/2`, `diagnosticar_todos/3` |
| Corte (§3.2)     | `nivel_certeza/2`, `severidad_ajustada/3` (precedencia), `estado_consulta/3` (fallback por defecto), exclusiones mutuas entre RAM y gráfica                                   |
| `\+` (§3.2)      | RAM vs. gráfica (`\+ pitidos_largos(R)`), malware vs. actualización defectuosa, validación de «no está presente la condición excluyente»                                      |
| `findall` (§3.3) | `findall(Dx-FC, ..., Candidatos)` + agrupación sin duplicados con `sort/2`/`setof/3`                                                                                          |
| Severidad (§3.3) | `severidad_base/2`, `severidad_ajustada/3`, `nivel_severidad/3`                                                                                                               |
| Puente (§3.4)    | `motor_inferencia.py`                                                                                                                                                         |

## 9. Estados de error y manejo

| Situación                                      | Dónde se detecta                                               | Resultado                                                  |
| ---------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------- |
| SWI-Prolog no instalado o no encontrado        | `cargar_base()`                                                | Mensaje con instrucciones; salida controlada               |
| `base_conocimiento.pl` con errores de sintaxis | `cargar_base()` (verifica que existan los predicados públicos) | Mensaje; no se continúa                                    |
| Respuesta fuera de catálogo                    | Prolog (`validar_entrada/2`)                                   | `Estado = entrada_invalida`                                |
| Lista vacía                                    | Prolog                                                         | `datos_insuficientes`                                      |
| Excepción inesperada del puente                | `motor_inferencia.py`                                          | Mensaje genérico + detalle técnico solo en modo depuración |

## 10. Stack aprobado (no agregar fuera de esto sin decisión registrada)

| Capa                 | Tecnología                                   | Nota                                       |
| -------------------- | -------------------------------------------- | ------------------------------------------ |
| Motor lógico         | **SWI-Prolog** (versión estable 9.x)         | Anotar versión exacta en `05`              |
| Lenguaje puente      | **Python 3.11+** (anotar versión)            | Solo biblioteca estándar + puente          |
| Puente               | **PySwip** (o **Janus**, ADR-002)            | Una sola de las dos                        |
| Pruebas Prolog       | **plunit** (incluida en SWI-Prolog)          | `tests/tests_kb.pl`                        |
| Pruebas Python       | Script propio `pruebas.py`                   | Sin pytest                                 |
| Calidad Python       | `python -m compileall .` y, opcional, `ruff` | `ruff` solo como herramienta de desarrollo |
| Control de versiones | Git + GitHub                                 | Una rama por tarea                         |

**No usar:** Tkinter u otra GUI, frameworks web, bases de datos, bibliotecas de IA/ML, pandas/numpy, ORMs, `assert`/`retract` para la base de hechos de la sesión.

## 11. Entorno local

Requisitos: SWI-Prolog instalado y en el `PATH`, Python 3.11+, pip, Git. En Windows, la arquitectura (64 bits) de Python y de SWI-Prolog debe coincidir.

```bash
swipl --version
python --version
python -m pip install -r requirements.txt
swipl -q -g run_tests -t halt tests/tests_kb.pl
python pruebas.py
python main.py
```

Codificación: UTF-8 en archivos y en consola (`sys.stdout.reconfigure(encoding="utf-8")` en Python; ver `10` T-10).

## 12. Convenciones de nombres

- Predicados, átomos y funciones: **español, minúsculas, `snake_case`, sin tildes ni ñ** (`falla_ram`, `catalogo_preguntas`).
- Los textos para el usuario (recomendaciones, preguntas) van como átomos entre comillas simples; pueden tener tildes si UTF-8 funciona de punta a punta (se prueba en F0-02); si no, se escriben sin tildes.
- Identificadores de regla: `r01`, `r02`… únicos y citados en comentarios, en el diccionario y en `explicar/3`.
