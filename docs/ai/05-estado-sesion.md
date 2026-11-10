# 05 · Estado de la sesión (traspaso)

> Documento de estado del proyecto DiagnostiPC.

## Última actualización

- **Fecha:** 2026-11-10
- **Fase actual:** F7 / Entregable 4. Todo lo que puede hacer un agente está terminado.
- **Ramas (apiladas, sin `push` ni fusión a `main`):** `feat/F7-01-contradicciones` → `feat/F7-02-ui-contradicciones` → `docs/F7-04-arquitectura` (contiene también F7-05 y el cierre).
- **Estado general:** el sistema detecta y bloquea entradas contradictorias en Prolog, lo muestra en Streamlit y está cubierto por pruebas. El informe PDF y el guion de sustentación están listos.

## Pendiente (solo humanos)

1. **F7-03:** validar con el técnico (T1) los 3 pares de `incompatible/3`, marcados `[PENDIENTE-VALIDAR]`. Si aprueba, quitar la marca y citar `T1` en el comentario.
2. Revisar las tres ramas y fusionarlas a `main` en orden, según `03 §6`. Revisa la otra persona de la pareja.
3. Ensayar la sustentación con `docs/entregables/05-guion-sustentacion.md`: auditoría cruzada y modificaciones A1–A5 y B1–B4.
4. Opcional: borrar la carpeta `venv/`, que está rota (E-004).

**Lectura obligatoria para la próxima sesión con agente:** este archivo y `04` → F7-03.

## Qué se hizo en la sesión 5

| Tarea | Resultado |
| ----- | --------- |
| F7-01 | Sección 16 (`incompatible/3`, `par_contradictorio/4`, `contradicciones/2`, `estado_consistencia/2`). Bloqueo en `diagnosticar_todos/3`, `sintoma_desempate/4` y `registrar_diagnostico_dinamico/5`. `tests/tests_kb.pl` creado. Fix E-003. |
| F7-02 | `motor.verificar_consistencia()`; aviso con el motivo en `main.py` para las tres vías de entrada; casos 12–16 en `pruebas.py`. |
| F7-04 | `02-arquitectura.md` reescrito según el código real. |
| F7-05 | `docs/entregables/informe_tecnico_entregable4.pdf` (se genera con `uv run --no-project --with reportlab python docs/entregables/informe/generar_informe.py`) y `05-guion-sustentacion.md`. |
| Extra | Comentarios `CORTE` en todos los cortes antiguos (regla 5); capturas `01`/`02` renombradas; enlaces del README relativos; regla 11 de `AGENTS.md`: commits sin atribución a IA. |

## Estado del sistema

| Componente                   | Estado | Notas                                                        |
| ---------------------------- | ------ | ------------------------------------------------------------ |
| `base_conocimiento.pl`       | ✅     | Carga sin advertencias; todos los `!` comentados             |
| `tests/tests_kb.pl`          | ✅     | 11/11 plunit (consistencia de la entrada)                    |
| `motor_inferencia.py`        | ✅     | `verificar_consistencia()`; E-003 corregido                  |
| `main.py`                    | ✅     | Aviso de contradicción verificado con `AppTest`              |
| `pruebas.py`                 | ✅     | 16/16 PASS                                                   |
| `docs/ai/02-arquitectura.md` | ✅     | Al día con el código                                         |
| Informe PDF y guion          | ✅     | 4 páginas; cifras tomadas de las pruebas al generarlo        |

- **SWI-Prolog:** 10.1.14 (x64-win64). Las capturas de evidencia son de Linux con 10.0.2.
- **Python:** 3.14 en `.venv` (recreado esta sesión, E-004). Ejecutar con `.venv\Scripts\python.exe`.

## Riesgos

- Los pares incompatibles no tienen fuente hasta que pase F7-03; dilo en la sustentación antes de que lo señalen.
- La DCG no interpreta negaciones («no se calienta»). Es una limitación declarada en el informe.
- `diagnosticar_todos/3` deja un punto de elección. Es inofensivo, y la forma de quitarlo está descrita en el guion (A5) por si piden un cambio en vivo.
