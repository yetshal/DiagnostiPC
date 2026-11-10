# 10 · Errores conocidos y soluciones

> Base de conocimiento de problemas ya resueltos. **Antes de depurar algo raro, busca aquí.** Al resolver un problema no obvio, agrégalo.
> Formato: síntoma → causa → solución → archivos.

## Plantilla

```markdown
### E-NNN · Título corto (componente)

- **Fecha / sesión:** AAAA-MM-DD / N
- **Síntoma:** mensaje de error o comportamiento exacto
- **Causa:** …
- **Solución:** …
- **Archivos:** …
- **Cómo evitarlo:** regla o prueba agregada
```

---

## Trampas previstas (verificar al implementar)

> Las marcadas **(verificar)** dependen de la versión de la librería o del sistema operativo: confirmar en F0-02 y anotar el resultado real.

### Lógica Prolog

| #    | Trampa                                                                                                           | Qué hacer                                                                                                                                                        |
| ---- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| T-01 | **Recursión izquierda** o dependencias circulares entre predicados provocan bucle infinito al hacer backtracking | Dependencias solo descendentes N3 → N2 → N1 (ADR-004); recursión sobre listas con caso base `[]` primero                                                         |
| T-02 | `\+ Meta` con variables **sin ligar** da resultados engañosos (no "para todo", sino "no existe")                 | Poner a la izquierda la meta que liga las variables; comentar `% NEGACION:`                                                                                      |
| T-03 | Un `!` mal ubicado (antes de las condiciones) o un "corte rojo" cambia el significado del programa               | El corte va después de las condiciones que identifican el caso; prueba que falle sin él; comentar `% CORTE:`                                                     |
| T-04 | `bagof/setof` **fallan** si no hay soluciones y tratan variables libres como agrupación                          | Usar `findall/3` (devuelve `[]`) y deduplicar con `sort/2`; si usas `setof`, cuantificar con `^`                                                                 |
| T-05 | Hechos del mismo predicado separados por otros generan la advertencia _discontiguous_                            | Mantenerlos contiguos (RF-01); no agregar la directiva para silenciarla                                                                                          |
| T-06 | Variables _singleton_ en cláusulas producen advertencias al cargar                                               | Usar `_` o nombrar con prefijo `_`; la carga debe salir limpia                                                                                                   |
| T-07 | `predsort/3` **elimina** elementos que el comparador considera iguales (`=`)                                     | Comparador total que desempata por el nombre del diagnóstico; o usar `sort/4` sobre `Clave-Item`                                                                 |
| T-08 | Aritmética con coma flotante: `0.8 + 0.5*0.2 =:= 0.9` puede ser falso                                            | FC enteros 0–100 (ADR-005); división entera `//` y prueba de redondeo                                                                                            |
| T-09 | Comparar `1` con `1.0` o un entero con un átomo `'1'` falla en silencio                                          | Valores numéricos del catálogo siempre enteros; validar el tipo en `validar_entrada/2`                                                                           |
| T-10 | Tildes y `ñ` en átomos/strings se corrompen según la codificación (Windows)                                      | Identificadores sin tildes (D-008); `:- set_prolog_flag(encoding, utf8).`; en Python `sys.stdout.reconfigure(encoding="utf-8")`; probar en F0-02 **(verificar)** |
| T-11 | Un predicado que imprime (`format`, `write`) desde la base contamina la salida de Python                         | La base no imprime; solo devuelve datos                                                                                                                          |

### Puente Python ↔ Prolog

| #    | Trampa                                                                                                                                                          | Qué hacer                                                                                                                                                                              |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| T-12 | Una consulta del puente que no se consume o no se cierra **bloquea** las siguientes ("query ya abierta" o resultados mezclados)                                 | Consumir siempre con `list(...)` o cerrar explícitamente en un `finally`; encapsular en `consultar()` **(verificar)**                                                                  |
| T-13 | Los términos compuestos (`dx(a,b)`) vuelven como objetos del puente con representación distinta según la versión; los átomos pueden llegar como `str` o `bytes` | Frontera plana: listas, átomos, enteros (D-015); normalizar `bytes → str` en un único lugar **(verificar)**                                                                            |
| T-14 | El puente no encuentra SWI-Prolog (`libswipl` no encontrada) o hay desajuste 32/64 bits                                                                         | Instalar SWI-Prolog de la misma arquitectura que Python; agregar su carpeta `bin` al `PATH` o definir las variables de entorno que indique la documentación del puente **(verificar)** |
| T-15 | `consult` con errores de sintaxis a veces solo emite mensajes y deja la base **incompleta** sin lanzar excepción                                                | `cargar_base()` comprueba que existan los predicados públicos (`current_predicate/1`) y aborta con mensaje claro                                                                       |
| T-16 | Construir consultas con texto del usuario abre la puerta a átomos mal formados o a inyección de metas                                                           | Solo átomos validados con regex y enteros; el usuario elige opciones numeradas, no escribe átomos                                                                                      |
| T-17 | Una consulta que falla (`false`) devuelve lista vacía; confundirla con `Estado = datos_insuficientes`                                                           | `diagnosticar_todos/3` **siempre** tiene éxito (último caso por defecto con corte); Python trata «sin solución» como error del motor                                                   |
| T-18 | Rutas con espacios o separadores de Windows al cargar el `.pl`                                                                                                  | Construir la ruta con `pathlib` y pasarla en forma absoluta                                                                                                                            |

### Proceso y entorno

| #    | Trampa                                                                                            | Qué hacer                                                                                                                                                         |
| ---- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| T-19 | `swipl -g run_tests -t halt` devuelve siempre 0 en algunas versiones aunque falle una prueba      | Verificar el código de salida real en F0-03 y, si hace falta, usar `-g "run_tests -> halt(0) ; halt(1)"` **(verificar)**                                          |
| T-20 | La regla se escribe con conocimiento inventado (síntoma que no apunta a esa falla, FC arbitrario) | Fuente o `[PENDIENTE-VALIDAR]` (D-012); validación del técnico en F1-05 y F2-11                                                                                   |
| T-21 | Cambiar un FC o un umbral rompe pruebas lejanas                                                   | Los casos de `entregables/04` se comparan por **estado y orden** y por FC solo donde el valor está fijado por el Entregable 1; cada cambio de FC se anota en `06` |
| T-22 | Dos personas editan el mismo bloque del `.pl` y generan conflictos de fusión                      | Cada tarea toca una sección distinta; ramas cortas; fusionar a diario                                                                                             |

## Errores encontrados durante el desarrollo

### E-001 · Claves de widget duplicadas en Streamlit por hechos dinámicos (`main.py`)

- **Fecha / sesión:** 2026-11-05 / Sesión 4 (Entregable 3)
- **Síntoma:** `streamlit.errors.StreamlitDuplicateElementKey: There are multiple elements with the same key='chk_apagado_brusco'`.
- **Causa:** Al inyectar reglas dinámicas en caliente con persistencia, hechos `sintoma_valido(...)` ya existentes se agregaron como duplicados al archivo `.pl`. El predicado `todos_los_sintomas/1` usaba `findall/3` sin deduplicar, generando una lista con elementos repetidos para la que Streamlit intentó instanciar dos checkboxes con la misma clave.
- **Solución:**
  1. En `base_conocimiento.pl`: Usar `list_to_set/2` dentro de `todos_los_sintomas/1`.
  2. En `motor_inferencia.py`: Filtrar con `set` en `obtener_catalogo_sintomas()` y verificar idempotencia antes de escribir a disco en `adquirir_nuevo_diagnostico()`.
  3. En `main.py`: Sanitizar `todos_sintomas` y `sintomas_a_mostrar` con `list(dict.fromkeys(...))`.
- **Archivos:** `base_conocimiento.pl`, `motor_inferencia.py`, `main.py`.
- **Cómo evitarlo:** No confiar en que `findall` devuelva conjuntos únicos; siempre envolver consultas de catálogo con `list_to_set` o deduplicación explícita.

### E-002 · Mutación de estado de sesión posterior a la instanciación de widgets (`main.py`)

- **Fecha / sesión:** 2026-11-05 / Sesión 4 (Entregable 3)
- **Síntoma:** `streamlit.errors.StreamlitWidgetAlreadyInstantiatedError: st.session_state['chk_...'] cannot be modified after the widget with that key is instantiated`.
- **Causa:** Modificar valores de claves asociadas a checkboxes (`chk_...`) dentro del cuerpo de evaluación de un botón (`if st.button(...)`), cuando dichos checkboxes ya habían sido renderizados previamente en el sidebar durante esa misma pasada.
- **Solución:** Mover la lógica de mutación a callbacks nativos (`on_click=cb_interpretar_dcg` y `on_click=cb_aplicar_telemetria`). En Streamlit, las funciones conectadas con `on_click` se ejecutan antes de que cualquier widget comience su renderizado.
- **Archivos:** `main.py`.
- **Cómo evitarlo:** Toda acción que cambie el valor de un checkbox o widget controlado por clave debe ejecutarse en un callback `on_click` o `on_change`.

### E-003 · El Modo Experto persistía reglas que Prolog había rechazado (`motor_inferencia.py`)

- **Fecha / sesión:** 2026-11-10 / Sesión 5 (F7-01)
- **Síntoma:** `adquirir_nuevo_diagnostico()` devolvía `ok: True` y escribía en `base_conocimiento.pl` aunque `registrar_diagnostico_dinamico/5` fallara.
- **Causa:** `for _ in query: break` no distingue "sin soluciones" de "éxito"; un fallo de Prolog no es una excepción en PySwip.
- **Solución:** `if not list(self._prolog.query(q)):` → devolver `ok: False` sin tocar el archivo.
- **Cómo evitarlo:** toda consulta con efectos (assertz) debe comprobar que tuvo al menos una solución antes de continuar.

### E-004 · `.venv` ausente en la máquina Windows

- **Fecha / sesión:** 2026-11-10 / Sesión 5
- **Síntoma:** `python` abre el alias de Microsoft Store; ningún Python global tiene `pyswip`.
- **Solución:** `py -3.14 -m venv .venv` y `.venv\Scripts\python.exe -m pip install -r requirements.txt`; ejecutar todo con `.venv\Scripts\python.exe`.
