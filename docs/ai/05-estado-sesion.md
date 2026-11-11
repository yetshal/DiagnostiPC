# 05 · Estado de la sesión (traspaso)

> Documento de estado del proyecto DiagnostiPC.

## Última actualización

- **Fecha:** 2026-11-11
- **Fase actual:** F7 / Entregable 4. Todo lo que puede hacer un agente está terminado.
- **Ramas:** F7-01…F7-06 ya fusionadas a `main` (PR #1 y PR #2). Abiertas: `fix/pyswip-linux-swipl10` (Fix E-005) y `feat/F7-08-borrar-experto` (borrar diagnósticos del Modo Experto; parte de la anterior, sin commitear).
- **Estado general:** el sistema detecta y bloquea entradas contradictorias en Prolog, lo muestra en Streamlit y está cubierto por pruebas (19/19 PASS en Linux; Windows sin reprobar tras F7-08). El informe PDF y el guion de sustentación están listos.

## Pendiente (solo humanos)

1. **F7-03:** validar con el técnico (T1) los 3 pares de `incompatible/3`, marcados `[PENDIENTE-VALIDAR]`. Si aprueba, quitar la marca y citar `T1` en el comentario.
2. Revisar y fusionar `fix/pyswip-linux-swipl10` y luego `feat/F7-08-borrar-experto` según `03 §6`; reprobar `pruebas.py` en Windows.
3. Ensayar la sustentación con `docs/entregables/05-guion-sustentacion.md`: auditoría cruzada y modificaciones A1–A5 y B1–B4.

**Lectura obligatoria para la próxima sesión con agente:** este archivo y `04` → F7-03.

## Qué se hizo en las sesiones 7 y 8

| Tarea | Resultado |
| ----- | --------- |
| F7-08 | Modo Experto puede borrar lo que registra: `eliminar_diagnostico_dinamico/1`, marcas `diagnostico_adquirido/1`/`sintoma_adquirido/1`, selector con confirmación y casos 18–19. §15 del `.pl` sin duplicados. |
| Fix E-005 | Compatibilidad PySwip ↔ SWI-Prolog 10 en Linux x86_64 System V ABI (`motor_inferencia.py`): configurado `restype = c_bool` para funciones C `PL_is_*` y `PL_get_*`. Resuelto `AttributeError: 'list' object has no attribute 'value'`. Base de conocimiento y catálogo de síntomas ahora se muestran completos en Streamlit bajo Linux. |
| Docs | Registro de error E-005 en `10-errores-conocidos.md`, decisión D-028 en `07-decisiones.md`, bitácora de sesión 7 en `06-bitacora.md`. |

## Estado del sistema

| Componente                   | Estado | Notas                                                        |
| ---------------------------- | ------ | ------------------------------------------------------------ |
| `base_conocimiento.pl`       | ✅     | Carga sin advertencias; todos los `!` comentados             |
| `tests/tests_kb.pl`          | ✅     | 16/16 plunit (consistencia + borrado experto)                    |
| `motor_inferencia.py`        | ✅     | `verificar_consistencia()`; Fix E-005 (c_bool FFI ABI)       |
| `main.py`                    | ✅     | Sidebar con 22 checkboxes y catálogo verificado con `AppTest`|
| `pruebas.py`                 | ✅     | 19/19 PASS en Linux; Windows pendiente de reprobar           |
| `docs/ai/02-arquitectura.md` | ✅     | Al día con el código                                         |
| Informe PDF y guion          | ✅     | 4 páginas; cifras tomadas de las pruebas al generarlo        |

- **SWI-Prolog:** 10.0.2 (x86_64-linux) / 10.1.14 (x64-win64).
- **Python:** `venv` funcional en Linux con Python 3.14 y Streamlit 1.67.0.

## Riesgos

- Los pares incompatibles no tienen fuente hasta que pase F7-03; dilo en la sustentación antes de que lo señalen.
- La DCG no interpreta negaciones («no se calienta»). Es una limitación declarada en el informe.
- `diagnosticar_todos/3` deja un punto de elección. Es inofensivo, y la forma de quitarlo está descrita en el guion (A5) por si piden un cambio en vivo.
