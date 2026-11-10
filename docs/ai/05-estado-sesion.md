# 05 · Estado de la sesión (traspaso)

> Documento de estado del proyecto DiagnostiPC.

## Última actualización

- **Fecha:** 2026-11-10
- **Fase actual:** F7 / Entregable 4 (contradicciones, auditoría cruzada, sustentación en vivo)
- **Rama:** `feat/F7-01-contradicciones` (sin commit todavía)
- **Estado general:** F7-01 terminada. Prolog detecta y bloquea entradas contradictorias; falta mostrarlo en la interfaz (F7-02).

## Próxima tarea: F7-02 · Integración en Python y Streamlit

**Lectura obligatoria:**

- `docs/ai/04-hoja-de-ruta.md` → F7-02.
- `base_conocimiento.pl` → Sección 16 (`contradicciones/2`, `estado_consistencia/2`).
- `docs/ai/07-decisiones.md` → D-026.
- `docs/ai/10-errores-conocidos.md` → E-003 (comprobar que una consulta tuvo solución).

**AC:**

1. `motor.verificar_consistencia(sintomas)` devuelve `{'estado': ..., 'conflictos': [...]}` sin lanzar excepciones.
2. `main.py` muestra un aviso con el motivo antes de los diagnósticos, para la entrada manual, la DCG y la telemetría.
3. Casos 12+ en `pruebas.py`: contradicción directa, DCG con texto contradictorio («no enciende y tiene fps bajos»), entrada ambigua o vacía en la DCG.

## Qué se hizo en la sesión 5

1. **Sección 16 en `base_conocimiento.pl`:** `incompatible/3` (3 pares con `no_arranca`, marcados `[PENDIENTE-VALIDAR]`), `par_contradictorio/4`, `incompatible_con_lista/2`, `contradicciones/2`, `entrada_contradictoria/1` y `estado_consistencia/2`.
2. **Bloqueos:**
   - `diagnosticar_todos/3` devuelve `[]` ante una entrada contradictoria.
   - `sintoma_desempate/4` ya no sugiere síntomas incompatibles.
   - `registrar_diagnostico_dinamico/5` rechaza patrones contradictorios.
3. **`tests/tests_kb.pl`:** creado, porque no existía. Tiene 11 pruebas plunit.
4. **Error E-003 corregido:** el Modo Experto persistía en disco reglas que Prolog había rechazado.
5. **Correcciones de documentación:**
   - Capturas `01`/`02` renombradas (los nombres estaban invertidos).
   - Nota de entorno Linux en `entregables/04`.
   - Aviso de desactualización en `02-arquitectura.md`.
   - Aclaraciones en `03 §9` y `AGENTS.md` regla 2.
   - `.gitignore` con `graphify-out/`.

## Estado del sistema

| Componente                         | Estado | Notas                                                         |
| ---------------------------------- | ------ | ------------------------------------------------------------- |
| `base_conocimiento.pl`             | ✅     | Sección 16 de consistencia añadida; carga sin advertencias     |
| `tests/tests_kb.pl`                | ✅     | 11/11 plunit (solo contradicciones; faltan N1–N3 antiguos)     |
| `motor_inferencia.py`              | ✅     | E-003 corregido; falta `verificar_consistencia()` (F7-02)     |
| `main.py`                          | ⏳     | Sin aviso de contradicciones (F7-02)                          |
| `pruebas.py`                       | ✅     | 11/11 PASS                                                    |
| `docs/ai/02-arquitectura.md`       | ⚠️     | Desactualizado respecto al código; reescribir en F7-04        |

- **SWI-Prolog:** 10.1.14 (x64-win64). Las capturas de evidencia son de Linux con 10.0.2.
- **Python:** 3.14 en `.venv`, recreado esta sesión (E-004). Ejecutar con `.venv\Scripts\python.exe`.
- **PySwip / Streamlit / scikit-learn:** según `requirements.txt`.

## Riesgos y pendientes

- Los 3 pares de `incompatible/3` no tienen fuente; validar con T1 (F7-03).
- `diagnosticar_todos/3` deja un punto de elección (comportamiento previo); Python solo toma la primera solución.
- `02-arquitectura.md` no es fiable hasta F7-04; usar el diccionario de predicados como referencia.
