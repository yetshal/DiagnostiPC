# Guion de sustentación — Entregable 4

> Auditoría cruzada (15 min) y modificaciones en vivo. Busca los predicados por **nombre**; los números de línea cambian con cada edición.
> Integrante A (motor simbólico): Juan Carlos Bastidas Bernal · Integrante B (integración): Julian Alfonso Montero Trujillo.

## 0. Antes de entrar (5 min)

```powershell
swipl -q -g run_tests -t halt tests/tests_kb.pl      # 11/11
.venv\Scripts\python.exe pruebas.py                 # 16/16
.venv\Scripts\streamlit.exe run main.py
```

Ten abiertos en el editor `base_conocimiento.pl` (Secciones 13 y 16) y `main.py` (bloque «Consistencia de la entrada» y la pestaña «¿Por qué?»). Haz un `git stash` o una rama nueva antes de cada cambio en vivo, para poder volver atrás.

## 1. Auditoría cruzada: qué intentarán contra nosotros

| Ataque                                               | Ejemplo                                         | Qué responde el sistema                                                       | Prueba |
| ---------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------- | ------ |
| Síntomas imposibles a la vez                         | `no_arranca` + `fps_bajos`                      | Aviso rojo con el motivo; sin dictamen                                        | Caso 12 |
| Lo mismo escrito en texto libre                      | «no enciende y tiene fps bajos»                 | La DCG extrae ambos síntomas → aviso                                          | Caso 13 |
| Texto vacío, espacios, símbolos, frases vagas        | `""`, `"!!!"`, «la compu está rara»             | Sin síntomas, sin excepción                                                   | Caso 14 |
| Mezclar telemetría con texto contradictorio          | 92 °C y 19 FPS + «no pasa del post»             | Dos conflictos detectados → aviso                                             | Caso 15 |
| Enseñar al Modo Experto una regla imposible          | patrón `[no_arranca, throttling]`               | Rechazada; el `.pl` no cambia                                                 | Caso 16 |
| Un solo síntoma o síntomas sin patrón                | `[pantalla_azul]`                               | «Evidencia insuficiente» y sugerencia de siguiente síntoma                    | Caso 4 |
| Síntomas de dos fallas que se excluyen               | sobrecalentamiento + ventilador                 | Una se descarta por exclusión mutua (`excluye/2`)                             | Caso 3 |

**Límites conocidos (dilo antes de que lo encuentren):**
- La DCG no entiende negaciones: «no se calienta» se ignora; no produce `sobrecalentamiento`.
- Solo hay 3 pares incompatibles, todos con `no_arranca`, y están pendientes de validar con el técnico.
- Un síntoma mal escrito en texto libre simplemente no se reconoce.

## 2. Qué probar al auditar a la otra pareja

1. Entrada vacía y entrada con solo espacios o símbolos (¿lanza traceback?).
2. Dos síntomas contradictorios de su dominio (¿emite diagnóstico igual?).
3. Texto libre con conectores repetidos, mayúsculas y tildes («Y Y ADEMÁS…»).
4. El mismo síntoma repetido varias veces (¿cuenta doble la evidencia?).
5. Si tienen aprendizaje en caliente: una regla con síntomas incompatibles o con ID inválido (`"; halt."`).
6. Reiniciar la app después de aprender una regla (¿persiste? ¿se duplica?).

## 3. Integrante A — modificaciones en Prolog

Para comprobar cada cambio: `swipl -q base_conocimiento.pl` y la consulta indicada; al final, `run_tests`.

**A1 · Agregar un par incompatible (1 línea, Sección 16).**
```prolog
incompatible(no_arranca, temperatura_alta_gpu,
    'Leer la temperatura de la GPU exige el sistema operativo en ejecucion').
```
Comprobar: `?- contradicciones([no_arranca, temperatura_alta_gpu], P).`

**A2 · Quitar un corte y explicar qué cambia (`severidad_caso/2`).**
Quitar el `!` de la primera cláusula. `?- severidad_caso(falla_ram, N).` devuelve primero `alto` y, al pedir más (`;`), también `desconocido`. El corte excluye el valor por defecto cuando sí hay severidad registrada.

**A3 · Corte de precedencia en `estado_consistencia/2`.**
Sin el `!`, `?- estado_consistencia([no_arranca, fps_bajos], E).` da `contradictoria` y luego `consistente`: dos respuestas incompatibles. Con el corte, solo la primera.

**A4 · Ajustar la gramática DCG (Sección 13).**
- Sinónimo nuevo: `frase_sintoma(fps_bajos) --> [juegos, lentos].`
- Conector nuevo: `conector_opcional --> [luego], !.` (antes de la cláusula vacía).

Comprobar: `?- extraer_sintomas_dcg([los, juegos, lentos, luego, no, arranca], S).` → `[fps_bajos, no_arranca]`.

**A5 (si piden mejorar el código) · Quitar el punto de elección de `diagnosticar_todos/3`.**
Mover la cláusula `\+ tiene_sintomas_suficientes(...), !` antes de la cláusula del `findall` y quitarle el `\+`. Después, la prueba `no_afecta_entrada_valida` ya no necesita `[nondet]`.

## 4. Integrante B — modificaciones en Python

Para comprobar: `.venv\Scripts\python.exe pruebas.py` y recargar Streamlit.

**B1 · Cambiar cómo se muestra el aviso de contradicción (`main.py`, bloque «Consistencia de la entrada»).**
Por ejemplo, convertirlo en una tabla:
```python
st.error("Entrada contradictoria: diagnóstico bloqueado.")
st.table([{"Síntoma A": c["a"], "Síntoma B": c["b"], "Motivo": c["motivo"]}
          for c in consistencia["conflictos"]])
```

**B2 · Cambiar la visualización de la traza de caja blanca (pestaña «¿Por qué?», «2. Reglas Disparadas»).**
Agrupar por nivel en columnas, o mostrarla como texto monoespaciado:
```python
st.code("\n".join(reglas), language="text")
```

**B3 · Ajustar la captura del texto libre (`normalizar_texto_a_tokens` en `motor_inferencia.py`).**
Por ejemplo, ignorar palabras de relleno antes de enviarlas a Prolog:
```python
RELLENO = {"el", "la", "los", "las", "mi", "un", "una"}
return [t for t in re.findall(r"[a-z0-9_]+", t_limpio) if t not in RELLENO]
```
Nota: Python solo limpia el texto; reconocer síntomas sigue siendo trabajo de la DCG.

**B4 · Mostrar en la barra lateral qué síntomas extrajo la DCG** antes de aplicarlos (`cb_interpretar_dcg` ya guarda el resultado; mostrarlo con `st.caption`).

## 5. Preguntas probables

- *¿Por qué el bloqueo está en Prolog y no en Python?* Regla de oro 1: Prolog decide. Python solo muestra el motivo (D-026).
- *¿Qué pasa si quito el corte de `diagnosticar_todos/3` de la Sección 16?* Prolog seguiría a la cláusula del `findall` y podría emitir diagnósticos sobre una entrada imposible.
- *¿Por qué `\+` es seguro en `registrar_diagnostico_dinamico/5`?* `ListaSintomas` ya está ligada al llamarlo; no hay variables libres dentro de la negación.
- *¿Cómo garantizan que no hay ciclos?* Las dependencias van de N3 a N2 a N1 a los hechos; la única recursión es sobre la cola de una lista.
