# Plantilla para agregar o dividir tareas

Copia este bloque en `04-hoja-de-ruta.md`, dentro de la fase correspondiente:

```markdown
- [ ] **Fx-NN** · Título corto en imperativo — qué se construye en una frase (predicados, archivos o pantallas clave). — _AC:_ criterio **verificable** (qué se hace y qué debe ocurrir; incluye un caso de borde). — _Dep:_ Fx-NN, Fy-NN — _Resp.:_ K | I | K+I
```

## Buenas tareas

- Caben en **una sesión** (2–3 h; ≤ ~150 líneas de Prolog o ~120 de Python).
- Tienen un **AC observable**: una consulta con su resultado, una prueba plunit o una salida de consola.
- Entregan algo **utilizable** y probado, no una pieza suelta.
- Nombran sus dependencias y a su responsable.
- Dicen qué **no** incluyen si hay riesgo de que crezcan.

## Ejemplo de división

Tarea demasiado grande:

> **F2-04** · Todos los diagnósticos de Nivel 3.

Dividida (como en la hoja de ruta):

```markdown
- [ ] **F2-04** · Nivel 3 (a) arranque, energía y video — DX01, DX02, DX05 con exclusión RAM/gráfica. — _AC:_ el caso del Entregable 1 da `falla_ram` con FC 90 y la gráfica no aparece con pitidos largos. — _Dep:_ F2-03, F2-01 — _Resp.:_ K
- [ ] **F2-05** · Nivel 3 (b) almacenamiento, calor, CMOS y recursos — DX03, DX04, DX09, DX10. — _AC:_ pruebas ✓/✗ por diagnóstico. — _Dep:_ F2-03, F2-01 — _Resp.:_ K
```
